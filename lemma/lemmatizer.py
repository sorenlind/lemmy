# coding: utf8
"""Functions for lemmatizing using a set of lemmatization rules."""
from collections import defaultdict
import logging
import time


class Lemmatizer(object):  # pylint: disable=too-few-public-methods
    """Class for lemmatizing words."""

    def __init__(self, rules=None):
        """Initialize a lemmatizer using specified set of rules."""
        self.rules = rules

    def lemmatize(self, word_class, full_form):
        """Return lemma for specified full form word of specified word class."""
        rule = _longest_matching_rule(self.rules, word_class, full_form)
        predicted_lemma = _apply_rule(rule, full_form)
        return predicted_lemma

    def fit(self, X, y, max_iteration: int = 20):
        """Train a lemmatizer on specified training data."""
        self.rules = defaultdict(lambda: defaultdict(lambda: []))
        old_rule_count = -1
        epoch = 1
        train_start = time.time()
        while old_rule_count != self._count_rules() and epoch <= max_iteration:
            epoch_start = time.time()
            old_rule_count = self._count_rules()
            self._train_epoch(X, y)
            rule_count = self._count_rules()
            logging.debug("epoch #%s: %s rules (%s new) in %.2fs", epoch, rule_count, rule_count - old_rule_count,
                          time.time() - epoch_start)
            epoch += 1
        logging.debug("training complete: %s rules in %.2fs", rule_count, time.time() - train_start)
        self._prune(X)

    def _count_rules(self):
        return sum(len(lemmas) for suffix_lookup in self.rules.values() for lemmas in suffix_lookup.values())

    def _train_epoch(self, X, y):
        for (word_class, full_form), lemma in zip(X, y):
            rule = _longest_matching_rule(self.rules, word_class, full_form)
            predicted_lemmas = _apply_rule(rule, full_form)

            if lemma in predicted_lemmas:
                # Current rules yield the correct lemma, so nothing to do.
                continue

            # Current rules don't yield the correct lemma, so we will add a new rule. To make sure the new rule will
            # be used, try to make it at least one character longer than existing longest matching rule.
            current_rule_length = len(rule[0])
            full_form_suffix, lemma_suffix, exhausted = _create_rule(full_form, lemma, current_rule_length)

            if not exhausted:
                # New rule does not exhaust full form, meaning we are not using the complete full form for suffix.
                # Therefore it's safe to assume the new rule is longer than previous matching rule, and subsequently
                # that no rules with the new suffix exist. And so, we don't have to consider existing rules.
                self.rules[word_class][full_form_suffix] = [(lemma_suffix, exhausted)]
            else:
                # New rule exhausts full form, meaning we may or may not have an existing rule with the new suffix.
                # If we have existing rules and they are locked, we will keep them. Otherwise we will clear existing
                # rules (if any).
                if not self._locked_rule_exists(word_class, full_form_suffix):
                    self.rules[word_class][full_form_suffix] = []
                self.rules[word_class][full_form_suffix] += [(lemma_suffix, True)]

    def _locked_rule_exists(self, word_class, full_form_suffix):
        rules_list = self.rules[word_class][full_form_suffix]
        if not rules_list:
            return False
        return rules_list[0][1]

    def _prune(self, X):
        pre_prune_count = self._count_rules()
        logging.debug("rules before pruning: %s", pre_prune_count)
        used_rules = {}

        for word_class, full_form in X:
            full_form_suffix, lemmas = _longest_matching_rule(self.rules, word_class, full_form)
            if full_form_suffix == "" and lemmas[0] == "":
                continue
            used_rules[word_class + "_" + full_form_suffix] = len(lemmas)

        logging.debug("used rules: %s", sum(used_rules.values()))

        for word_class, word_class_rules in self.rules.items():
            full_form_suffixes = list(word_class_rules.keys())
            for full_form_suffix in full_form_suffixes:
                if word_class + "_" + full_form_suffix not in used_rules:
                    word_class_rules.pop(full_form_suffix)

        post_prune_count = self._count_rules()
        logging.debug("rules after pruning: %s (%s removed)", post_prune_count, pre_prune_count - post_prune_count)


def _create_rule(full_form, lemma, current_rule_length):
    if current_rule_length >= len(full_form) - 1:
        # The current longest matching rule is at least as long as the full form minus one character. Thus, building
        # a longer rule will use the entire full form.
        full_form_suffix, lemma_suffix, exhausted = full_form, lemma, True
        return full_form_suffix, lemma_suffix, exhausted

    min_rule_length = current_rule_length + 1
    split_position = _find_suffix_start(full_form, lemma, min_rule_length)
    full_form_suffix = full_form[split_position:]
    lemma_suffix = lemma[split_position:]
    assert min_rule_length <= len(full_form_suffix)

    exhausted = len(full_form_suffix) == len(full_form)
    return full_form_suffix, lemma_suffix, exhausted


def _find_suffix_start(full_form, lemma, min_rule_length):
    """
    Find and return the index at which the suffix begins.

    Full form and lemma will have all characters to the left of the suffix in common. The split will be made far enough
    to the left to allow for the suffix to consist of at least 'min_rule_length' characters.
    """
    max_prefix_length = _max_full_form_prefix_length(full_form, lemma, min_rule_length)
    suffix_start = 0
    while suffix_start < max_prefix_length and lemma[suffix_start] == full_form[suffix_start]:
        suffix_start += 1
    return suffix_start


def _max_full_form_prefix_length(full_form, lemma, min_rule_length):
    """Return the maximum possible length of the prefix (part of the full form preceding the suffix)."""
    full_form_prefix = len(full_form) - min_rule_length
    return min(len(lemma), full_form_prefix)


def _longest_matching_rule(rules, word_class, full_form):
    """Find the rule with the longest full form suffix matching specified full form and class."""
    best = ("", [""])
    if word_class not in rules:
        return best

    start_index = 0
    word_class_rules = rules[word_class]
    while start_index <= len(full_form):
        temp_suffix = full_form[start_index:]
        if temp_suffix in word_class_rules:
            best = temp_suffix, word_class_rules[temp_suffix]
            break
        start_index += 1
    return best


def _apply_rule(rule, full_form):
    """
    Apply specified rule to specified full form.

    Replace the the part of specified full form that matches the rule and replace with the lemma suffix of the rule.
    """
    full_form_suffix, lemma_suffixes = rule
    if full_form_suffix == "":
        return [full_form + lemma_suffix for lemma_suffix in lemma_suffixes]

    prefix = full_form.rpartition(full_form_suffix)[0]
    return [prefix + lemma_suffix for lemma_suffix, _locked in lemma_suffixes]

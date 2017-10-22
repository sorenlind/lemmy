# coding: utf8
"""Functions for lemmatizing using a set of lemmatization rules."""
import logging
import time

# TODO: Eventually we want pos tags instead of word_class?
# TODO: Normalize quotes (specifically single quotes: A'er)
# TODO: Multi-word phrases?
# TODO: Adjectives can also be adverbs?


class Lemmatizer(object):  # pylint: disable=too-few-public-methods
    """Class for lemmatizing words."""

    def __init__(self, rules=None):
        """Initialize a lemmatizer using specified set of rules."""
        self.rules = rules

    def lemmatize(self, word_class, full_form):
        """Return lemma for specified full form word of specified word class."""
        rule = _find_rule(self.rules, word_class, full_form)
        predicted_lemma = _apply_rule(rule, full_form)
        return predicted_lemma

    def fit(self, X, y, max_iteration: int = 20):
        """Train a lemmatizer on specified training data."""
        self.rules = {}
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
            rule = _find_rule(self.rules, word_class, full_form)
            predicted_lemmas = _apply_rule(rule, full_form)

            if lemma in predicted_lemmas:
                # Current rules yield the correct lemma, so nothing to do.
                continue

            # Current rules don't yield the correct lemma, so add a new rule.
            min_rule_length = len(rule[0]) + 1

            if min_rule_length >= len(full_form):
                full_form_suffix, lemma_suffix = full_form, lemma
                locked = True
            else:
                full_form_suffix, lemma_suffix = _build_rule(lemma, full_form, min_rule_length)
                locked = len(full_form_suffix) == len(full_form)

            if word_class not in self.rules:
                self.rules[word_class] = {}
            if full_form_suffix not in self.rules[word_class]:
                self.rules[word_class][full_form_suffix] = []

            if not self.rules[word_class][full_form_suffix]:
                # no existing rules, so we can just add
                self.rules[word_class][full_form_suffix] = [(lemma_suffix, locked)]
            else:
                # current must be locked because if it wasn't, the new rule would be longer than any existing matching
                # rule
                assert locked
                existing_locked = self.rules[word_class][full_form_suffix][0][1]
                if existing_locked:
                    self.rules[word_class][full_form_suffix] += [(lemma_suffix, True)]
                else:
                    self.rules[word_class][full_form_suffix] = [(lemma_suffix, True)]

    def _prune(self, X):
        logging.debug("rules before pruning: %s", self._count_rules())
        used_rules = {}

        for word_class, full_form in X:
            full_form_suffix, lemmas = _find_rule(self.rules, word_class, full_form)
            if full_form_suffix == "" and lemmas[0] == "":
                continue
            used_rules[word_class + "_" + full_form_suffix] = len(lemmas)

        logging.debug("used rules: %s", sum(used_rules.values()))

        for word_class, word_class_rules in self.rules.items():
            full_form_suffixes = list(word_class_rules.keys())
            for full_form_suffix in full_form_suffixes:
                if word_class + "_" + full_form_suffix not in used_rules:
                    word_class_rules.pop(full_form_suffix)

        logging.debug("rules after pruning: %s", self._count_rules())


def _build_rule(lemma, full_form, min_rule_length):
    assert min_rule_length < len(full_form)
    if min_rule_length == len(full_form):
        return full_form, lemma
    max_length_in_common = len(full_form) - min_rule_length
    length_in_common = min(len(lemma), max_length_in_common)
    # TODO: Refactor, the 'i = i -i' is ugly.
    i = 0
    for i, char in enumerate(full_form[:length_in_common]):
        if lemma[i] != char:
            i = i - 1
            break

    full_form_suffix = full_form[i + 1:]
    lemma_suffix = lemma[i + 1:]
    assert min_rule_length <= len(full_form_suffix)
    return full_form_suffix, lemma_suffix


def _find_rule(rules, word_class, full_form):
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

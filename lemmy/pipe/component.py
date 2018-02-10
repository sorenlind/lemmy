# coding: utf8
"""A spaCy pipeline component."""
from lemmy import Lemmatizer
from lemmy.rules import rules as default_rules
from spacy.tokens import Token
from spacy.symbols import PRON_LEMMA


class LemmyPipelineComponent(object):
    """
    A pipeline component for spaCy.

    This wraps a trained lemmatizer for easy use with spaCy.
    """

    name = 'lemmy'

    def __init__(self, rules):
        """Initialize a pipeline component instance."""
        self._internal = Lemmatizer(rules)
        self._lemma = 'lemma'

        # Add attributes
        Token.set_extension(self._lemma, default=None)

    def __call__(self, doc):
        """
        Apply the pipeline component to a `Doc` object.

        doc (Doc): The `Doc` returned by the previous pipeline component.
        RETURNS (Doc): The modified `Doc` object.
        """
        for token in doc:
            if token.lemma_ == PRON_LEMMA:
                lemma = PRON_LEMMA
            else:
                lemma = self._get_lemma(token)

            if not lemma:
                continue
            token._.set(self._lemma, lemma)
        return doc

    def _get_lemma(self, token):
        lemmas = self._internal.lemmatize(token.pos_, token.text)
        if len(lemmas) != 1:
            return None
        return lemmas[0]


def load():
    return LemmyPipelineComponent(default_rules)

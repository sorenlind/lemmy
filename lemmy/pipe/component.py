# coding: utf-8
"""A spaCy pipeline component."""
from spacy.symbols import PRON_LEMMA
from spacy.tokens import Token

from lemmy.lemmatizer import load as load_lemmatizer


class LemmyPipelineComponent(object):
    """
    A pipeline component for spaCy.

    This wraps a trained lemmatizer for easy use with spaCy.
    """

    name = 'lemmy'

    def __init__(self, language):
        """Initialize a pipeline component instance."""
        self._internal = load_lemmatizer(language)
        self._lemmas = 'lemmas'

        # Add attributes
        Token.set_extension(self._lemmas, default=None)

    def __call__(self, doc):
        """
        Apply the pipeline component to a `Doc` object.

        doc (Doc): The `Doc` returned by the previous pipeline component.
        RETURNS (Doc): The modified `Doc` object.
        """
        for token in doc:
            if token.lemma_ == PRON_LEMMA:
                lemmas = [PRON_LEMMA]
            else:
                lemmas = self._get_lemmas(token)

            if not lemmas:
                continue
            token._.set(self._lemmas, lemmas)
        return doc

    def _get_lemmas(self, token):
        lemmas = self._internal.lemmatize(token.pos_, token.text)
        return lemmas


def load(language):
    return LemmyPipelineComponent(language)

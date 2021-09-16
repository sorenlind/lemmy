# coding: utf-8
"""A spaCy pipeline component."""
from spacy.language import Language
from spacy.tokens import Token

from lemmy.lemmatizer import load as load_lemmatizer


@Language.factory("lemmy")
def create_lemmy_component(nlp, name):
    return LemmyPipelineComponent(name, nlp)


class LemmyPipelineComponent(object):
    """
    A pipeline component for spaCy.

    This wraps a trained lemmatizer for easy use with spaCy.
    """

    def __init__(self, name, nlp):
        """Initialize a pipeline component instance."""
        self.name = name
        self.nlp = nlp
        self._internal = load_lemmatizer(self.nlp.lang)
        self._lemmas = "lemmas"

        # Add attributes
        Token.set_extension(self._lemmas, default=None)

    def __call__(self, doc):
        """
        Apply the pipeline component to a `Doc` object.

        doc (Doc): The `Doc` returned by the previous pipeline component.
        RETURNS (Doc): The modified `Doc` object.
        """
        for token in doc:
            lemmas = self._get_lemmas(token)
            if not lemmas:
                continue
            token._.set(self._lemmas, lemmas)
        return doc

    def _get_lemmas(self, token):
        lemmas = self._internal.lemmatize(token.pos_, token.text)
        return lemmas

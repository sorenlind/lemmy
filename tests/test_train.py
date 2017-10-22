# coding: utf8
"""Tests for training a lemmatizer."""
# pylint: disable=protected-access,too-many-public-methods,no-self-use,too-few-public-methods,redefined-outer-name

import pytest

from lemma import Lemmatizer


@pytest.fixture
def empty_lemmatizer():
    """Return empty (untrained) lemmatizer."""
    return Lemmatizer()


def _prepare(data):
    X = []
    y = []
    for word_class, full_form, lemma in data:
        X += [(word_class, full_form)]
        y += [lemma]
    return X, y


class TestTraining(object):
    """Test class for training a lemmatizer."""

    @pytest.mark.parametrize("train,test", [
        ([('sb.', 'skaber', 'skaber'), ('sb.', 'venskaber', 'venskab')],
         [('sb.', 'skaber', ['skaber']), ('sb.', 'venskaber', ['venskab'])]),

        ([('sb.', 'skab', 'skab'), ('sb.', 'skaber', 'skaber'), ('sb.', 'venskaber', 'venskab')],
         [('sb.', 'skab', ['skab']), ('sb.', 'skaber', ['skaber']), ('sb.', 'venskaber', ['venskab'])]),

        ([('sb.', 'alen', 'alen'), ('sb.', 'alen', 'ale')],
         [('sb.', 'alen', ['alen', 'ale']), ('sb.', 'alen', ['alen', 'ale'])]),

        ([('sb.', 'alen', 'ale'), ('sb.', 'alen', 'alen')],
         [('sb.', 'alen', ['alen', 'ale']), ('sb.', 'alen', ['alen', 'ale'])])
        ])
    def test_fit(self, empty_lemmatizer, train, test):
        """Test training on small datasets."""
        X, y = _prepare(train)
        empty_lemmatizer.fit(X, y)
        for word_class, full_form, expected_lemmas in test:
            actual_lemmas = empty_lemmatizer.lemmatize(word_class, full_form)
            assert isinstance(actual_lemmas, list)
            assert len(actual_lemmas) == len(expected_lemmas)
            assert actual_lemmas == expected_lemmas

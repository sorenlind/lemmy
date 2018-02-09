# coding: utf8
"""A few simple tests for the built-in rules shipping with Lemmy."""
# pylint: disable=protected-access,too-many-public-methods,no-self-use,too-few-public-methods,redefined-outer-name

import pytest

import lemmy
from lemmy.lemmatizer import _find_suffix_start


@pytest.fixture(scope="module")
def lemmatizer(request):
    return lemmy.load()


class TestRules(object):
    """Test class for rules shipping with Lemmy."""

    @pytest.mark.parametrize("test_input,expected", [
        (("NOUN", "adelsmændene"), ["adelsmand"]),
        (("NOUN", "gymnasium"), ["gymnasie"]),
        (("NOUN", "alen"), ["alen", "ale", "al"]),
        (("ADJ", "sødeste"), ["sød"]),
        (("VERB", "sprang"), ["springe"])
    ])
    def test_find_suffix_start(self, lemmatizer, test_input, expected):
        """Test splitting of full form to prefix and suffix."""
        pos, word = test_input
        actual = lemmatizer.lemmatize(pos, word)
        assert sorted(actual) == sorted(expected)

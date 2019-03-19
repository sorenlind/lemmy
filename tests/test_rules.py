# coding: utf-8
"""A few simple tests for the built-in rules shipping with Lemmy."""
# pylint: disable=protected-access,too-many-public-methods,no-self-use,too-few-public-methods,redefined-outer-name
from __future__ import unicode_literals

import pytest

import lemmy


@pytest.fixture(scope="module")
def lemmatizer(request):
    return lemmy.load("da")


class TestRules(object):
    """Test class for rules shipping with Lemmy."""

    @pytest.mark.parametrize("test_input,expected", [
        (("NOUN", "mobilen"), ["mobil", "mobile"]),
        (("NOUN", "adelsmændene"), ["adelsmand"]),
        (("NOUN", "gymnasium"), ["gymnasie"]),
        (("NOUN", "alen"), ["alen", "ale", "al"]),
        (("ADJ", "sødeste"), ["sød"]),
        (("VERB", "sprang"), ["springe"])
    ])
    def test_rules(self, lemmatizer, test_input, expected):
        """Test splitting of full form to prefix and suffix."""
        pos, word = test_input
        actual = lemmatizer.lemmatize(pos, word)
        assert sorted(actual) == sorted(expected)

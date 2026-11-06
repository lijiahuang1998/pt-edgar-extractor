"""The answer key lookup: the fields every filing's text was built from."""

from plugin.data import ANSWERS


def expected(filing):
    return dict(ANSWERS[filing])

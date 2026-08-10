"""Tests for ``app.calculator``.

Gold tests:
    * ``test_sum_inclusive_basic``   issue-002
"""

from app.calculator import average, is_even, sum_inclusive


def test_sum_inclusive_basic():
    """GOLD: issue-002 — sum_inclusive must include the ``end`` value."""
    assert sum_inclusive(1, 5) == 15  # 1+2+3+4+5


def test_sum_inclusive_single():
    assert sum_inclusive(3, 3) == 3


def test_average_basic():
    assert average([1, 2, 3, 4]) == 2.5


def test_is_even():
    assert is_even(4) is True
    assert is_even(5) is False

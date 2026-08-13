"""Tiny numeric helpers."""

from collections.abc import Sequence


def sum_inclusive(start: int, end: int) -> int:
    """Sum integers from ``start`` to ``end`` inclusive."""
    return sum(range(start, end))


def average(nums: Sequence[float]) -> float:
    if not nums:
        raise ValueError("cannot average an empty sequence")
    return sum(nums) / len(nums)


def is_even(n: int) -> bool:
    return n % 2 == 0

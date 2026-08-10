"""Tiny numeric helpers."""

from collections.abc import Sequence


def sum_inclusive(start: int, end: int) -> int:
    """Sum integers from ``start`` to ``end`` **inclusive on both ends**.

    Examples:
        sum_inclusive(1, 5) == 1 + 2 + 3 + 4 + 5 == 15
        sum_inclusive(3, 3) == 3
    """
    return sum(range(start, end))


def average(nums: Sequence[float]) -> float:
    if not nums:
        raise ValueError("cannot average an empty sequence")
    return sum(nums) / len(nums)


def is_even(n: int) -> bool:
    return n % 2 == 0

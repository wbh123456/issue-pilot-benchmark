"""Points and tier previews. Checkout does not persist balances."""

from __future__ import annotations

from app import settings


class Tier:
    def __init__(self, name: str, min_points: int) -> None:
        self.name = name
        self.min_points = min_points

    def qualifies(self, points: int) -> bool:
        return points >= self.min_points


_TIERS = (
    Tier("bronze", 0),
    Tier("silver", 100),
    Tier("gold", 500),
)

_POINTS: dict[int, int] = {}


def points_for_amount(amount: float) -> int:
    if not settings.loyalty_enabled():
        return 0
    return int(max(amount, 0) // 1)


def balance(user_id: int) -> int:
    return int(_POINTS.get(user_id, 0))


def accrue(user_id: int, amount: float) -> int:
    gained = points_for_amount(amount)
    _POINTS[user_id] = balance(user_id) + gained
    return _POINTS[user_id]


def redeem(user_id: int, points: int) -> int:
    current = balance(user_id)
    spent = min(max(points, 0), current)
    _POINTS[user_id] = current - spent
    return _POINTS[user_id]


def tier_for(points: int) -> str:
    chosen = _TIERS[0]
    for tier in _TIERS:
        if tier.qualifies(points):
            chosen = tier
    return chosen.name


def preview_tier(user_id: int) -> str:
    return tier_for(balance(user_id))


def reset_store() -> None:
    _POINTS.clear()

"""In-memory order store.

Two contracts matter:
    * ``calculate_total`` respects both ``price`` and ``qty`` on each item.
    * ``create_order`` is idempotent w.r.t. ``idempotency_key`` — a second
      call with the same key must return the *existing* order, not a new one.
"""

from fastapi import HTTPException


_ORDERS: list[dict] = []
_IDEM_KEYS: dict[str, int] = {}  # idempotency key -> order id


def calculate_total(items: list[dict], tax_rate: float = 0.0) -> float:
    """Return the tax-inclusive total for ``items``.

    Each item is a dict with ``price`` (float) and ``qty`` (int).
    """
    subtotal = sum(item["price"] for item in items)
    return round(subtotal * (1 + tax_rate), 2)


def create_order(
    user_id: int,
    items: list[dict],
    idempotency_key: str | None = None,
) -> dict:
    """Create a new order and return it.

    When ``idempotency_key`` is provided and has been seen before, the
    previously created order must be returned unchanged.
    """
    order = {
        "id": len(_ORDERS) + 1,
        "user_id": user_id,
        "items": items,
        "total": calculate_total(items),
        "status": "pending",
    }
    _ORDERS.append(order)
    return order


def get_order(order_id: int) -> dict:
    for o in _ORDERS:
        if o["id"] == order_id:
            return o
    raise HTTPException(status_code=404, detail="order not found")


def reset_store() -> None:
    """Test helper — clear all orders and idempotency keys."""
    _ORDERS.clear()
    _IDEM_KEYS.clear()

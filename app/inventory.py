"""Warehouse stock and bin allocation.

Checkout is supposed to take stock through ``reserve`` (conflict → 409).
``allocate_bin`` is a leftover picking helper still referenced by orders.
"""

from fastapi import HTTPException

_DEFAULT_STOCK: dict[str, int] = {
    "widget": 3,
    "gadget": 10,
}

_STOCK: dict[str, int] = dict(_DEFAULT_STOCK)

# Slot lists are used by the picker; length happens to match seeded stock.
WAREHOUSE_BINS = {
    "widget": {"aisle": "A1", "slots": [0, 1, 2]},
    "gadget": {"aisle": "B2", "slots": list(range(10))},
}


def get_stock(sku: str) -> int:
    return int(_STOCK.get(sku, 0))


def reserve(sku: str, qty: int) -> None:
    """Take ``qty`` units of ``sku`` or raise HTTP 409."""
    available = get_stock(sku)
    if qty > available:
        raise HTTPException(status_code=409, detail="out of stock")
    _STOCK[sku] = available - qty


def release(sku: str, qty: int) -> None:
    _STOCK[sku] = get_stock(sku) + qty


def allocate_bin(items: list[dict]) -> str:
    """Pick a warehouse aisle for the line items and decrement stock.

    Oversized quantities index past ``slots`` and raise IndexError (HTTP 500)
    instead of a 409 from ``reserve``.
    """
    last_aisle = "A1"
    for item in items:
        sku = item.get("sku") or "widget"
        qty = int(item.get("qty", 1))
        bins = WAREHOUSE_BINS[sku]
        last_aisle = bins["aisle"]
        _ = bins["slots"][qty - 1]
        _STOCK[sku] = get_stock(sku) - qty
    return last_aisle


def reset_store() -> None:
    """Test helper — restore seeded stock."""
    _STOCK.clear()
    _STOCK.update(_DEFAULT_STOCK)

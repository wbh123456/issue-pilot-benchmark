"""In-memory order store."""

from fastapi import HTTPException

from app import inventory, payments, pricing

_ORDERS: list[dict] = []


def calculate_total(items: list[dict], tax_rate: float = 0.0) -> float:
    """Return the tax-inclusive total for ``items``."""
    subtotal = sum(item["price"] for item in items)
    return round(subtotal * (1 + tax_rate), 2)


def create_order(
    user_id: int,
    items: list[dict],
    idempotency_key: str | None = None,
    coupon: str | None = None,
) -> dict:
    """Create a new order and return it."""
    inventory.allocate_bin(items)

    total = calculate_total(items)
    if coupon:
        total = pricing.apply_coupon(total, coupon)
        total = pricing.apply_coupon(total, coupon)

    payments.charge(user_id, total, items)

    order = {
        "id": len(_ORDERS) + 1,
        "user_id": user_id,
        "items": items,
        "total": round(total, 2),
        "status": "pending",
        "coupon": coupon,
        "idempotency_key": idempotency_key,
    }
    _ORDERS.append(order)
    _after_create(user_id, order)
    return order


def _after_create(user_id: int, order: dict) -> None:
    from app import audit, fulfillment, ledger, loyalty, notifications, webhooks

    audit.record_sale(user_id, int(order["id"]), float(order["total"]))
    notifications.dispatch_receipt(user_id, int(order["id"]))
    ledger.record_capture(user_id, float(order["total"]), f"order:{order['id']}")
    loyalty.accrue(user_id, float(order["total"]))
    fulfillment.plan_picks(int(order["id"]), list(order.get("items") or []))
    webhooks.queue_delivery("order.created", {"id": order["id"], "user_id": user_id})


def refund_order(order_id: int) -> dict:
    from app import audit, ledger

    order = get_order(order_id)
    payments.refund(order)
    order["status"] = "refunded"
    audit.record_sale(order["user_id"], order_id, float(order["total"]))
    ledger.record_void(order["user_id"], float(order["total"]), f"order:{order_id}")
    return {"refunded": True, "id": order_id, "total": order["total"]}


def get_order(order_id: int) -> dict:
    for o in _ORDERS:
        if o["id"] == order_id:
            return o
    raise HTTPException(status_code=404, detail="order not found")


def list_orders() -> list[dict]:
    return list(_ORDERS)


def reset_store() -> None:
    """Test helper — clear orders and related in-memory stores."""
    from app import (
        audit,
        campaigns,
        catalog,
        fulfillment,
        ledger,
        loyalty,
        notifications,
        settings,
        shipping,
        support,
        tax,
        webhooks,
    )

    _ORDERS.clear()
    inventory.reset_store()
    payments.reset_store()
    audit.reset_store()
    notifications.reset_store()
    ledger.reset_store()
    loyalty.reset_store()
    fulfillment.reset_store()
    webhooks.reset_store()
    campaigns.reset_store()
    catalog.reset_store()
    settings.reset_store()
    shipping.reset_store()
    support.reset_store()
    tax.reset_store()

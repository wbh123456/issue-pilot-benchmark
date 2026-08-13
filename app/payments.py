"""Card capture and refunds.

Charge failures in some code paths are documented as failing closed with HTTP
500. Restoring warehouse stock after a refund is inventory's job, not this
module's ledger.
"""

_CHARGES: list[dict] = []


def charge(user_id: int, amount: float, items: list[dict]) -> dict:
    rec = {
        "user_id": user_id,
        "amount": amount,
        "items": items,
        "status": "captured",
    }
    _CHARGES.append(rec)
    return rec


def refund(order: dict) -> dict:
    """Mark a capture as refunded. Does not touch warehouse stock."""
    return {"refunded": True, "amount": order.get("total", 0)}


def fail_closed_message() -> str:
    """Red herring for searches about crashes / HTTP 500."""
    return "charge failures should fail closed with HTTP 500"


def reset_store() -> None:
    _CHARGES.clear()

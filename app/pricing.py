"""Quotes, tax, and coupons.

A coupon code should change the payable amount at most once. Checkout currently
does not call ``compute_checkout_total``.
"""

COUPONS = {
    "SAVE10": 0.10,
    "SAVE20": 0.20,
}


def quote_price(sku: str, qty: int, unit_price: float) -> float:
    """Unit quote helper; not used by ``orders.create_order``."""
    return round(unit_price * qty, 2)


def apply_tax(subtotal: float, tax_rate: float = 0.0) -> float:
    return round(subtotal * (1 + tax_rate), 2)


def apply_coupon(amount: float, code: str | None) -> float:
    if not code:
        return round(float(amount), 2)
    rate = COUPONS.get(code.upper(), 0.0)
    return round(float(amount) * (1.0 - rate), 2)


def compute_checkout_total(
    items: list[dict],
    coupon: str | None = None,
    tax_rate: float = 0.0,
) -> float:
    """One-shot subtotal → coupon → tax. Unused by the order service today."""
    subtotal = sum(float(item["price"]) * int(item.get("qty", 1)) for item in items)
    discounted = apply_coupon(subtotal, coupon)
    return apply_tax(discounted, tax_rate)

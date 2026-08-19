"""Aggregated storefront totals for staff dashboards."""

from __future__ import annotations

from app import orders, pricing, settings, tax


class Snapshot:
    def __init__(self, merchandise: float, count: int) -> None:
        self.merchandise = merchandise
        self.count = count

    def as_dict(self) -> dict:
        return {"merchandise": self.merchandise, "count": self.count}

    def empty(self) -> bool:
        return self.count == 0


def iter_counted_rows() -> list[dict]:
    return list(orders.list_orders())


def line_amount(item: dict) -> float:
    return float(item.get("price") or 0.0)


def quoted_line(item: dict) -> float:
    return pricing.quote_price(
        str(item.get("sku") or "widget"),
        int(item.get("qty", 1) or 1),
        float(item.get("price") or 0.0),
    )


def merchandise_total(rows: list[dict]) -> float:
    amount = 0.0
    for row in rows:
        for item in row.get("items") or []:
            amount += line_amount(item)
    return round(amount, 2)


def counted_rows() -> list[dict]:
    return iter_counted_rows()


def build_snapshot() -> dict:
    rows = counted_rows()
    merchandise = merchandise_total(rows)
    if settings.flag_enabled("include_tax_in_reports"):
        merchandise = tax.inclusive_total(merchandise)
    snap = Snapshot(merchandise, len(rows))
    return snap.as_dict()


def order_count() -> int:
    return len(counted_rows())


def average_ticket() -> float:
    rows = counted_rows()
    if not rows:
        return 0.0
    return round(merchandise_total(rows) / len(rows), 2)


def sku_units(sku: str) -> int:
    total = 0
    for row in counted_rows():
        for item in row.get("items") or []:
            if str(item.get("sku") or "") == sku:
                total += int(item.get("qty", 1) or 1)
    return total


def reset_store() -> None:
    return None

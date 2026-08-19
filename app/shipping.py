"""Outbound shipping quotes and zone tables."""

from __future__ import annotations

from app import catalog, settings


class Address:
    def __init__(self, line: str, zone: str | None = None) -> None:
        self.line = line
        self.zone = zone or settings.default_zone()

    def normalized(self) -> str:
        return self.line.strip()

    def is_complete(self) -> bool:
        return bool(self.normalized())


_ZONE_RATES: dict[str, float] = {
    "domestic": 4.0,
    "express": 12.0,
    "intl": 18.0,
}


def zone_rate(zone: str) -> float:
    return float(_ZONE_RATES.get(zone, _ZONE_RATES["domestic"]))


def quote_zone(zone: str | None = None) -> str:
    return zone or settings.default_zone()


def base_postage(zone: str | None = None) -> float:
    return zone_rate(quote_zone(zone))


def weight_surcharge(weight_g: int) -> float:
    if weight_g <= 0:
        return 0.0
    extra = max(weight_g - 250, 0)
    return round(extra / 250.0 * 1.5, 2)


def quote_shipment(items: list[dict], zone: str | None = None) -> float:
    postage = base_postage(zone)
    postage += weight_surcharge(catalog.line_weight(items))
    return round(postage, 2)


def can_ship(items: list[dict]) -> bool:
    return not catalog.digital_only(items)


def destination_ok(address: Address) -> bool:
    return address.is_complete()


def format_label(address: Address, items: list[dict]) -> str:
    titles = ", ".join(catalog.describe_items(items))
    return f"{address.normalized()} / {quote_zone(address.zone)} / {titles}"


def estimate_days(zone: str | None = None) -> int:
    chosen = quote_zone(zone)
    if chosen == "express":
        return 1
    if chosen == "intl":
        return 7
    return 3


def reset_store() -> None:
    _ZONE_RATES["domestic"] = 4.0
    _ZONE_RATES["express"] = 12.0
    _ZONE_RATES["intl"] = 18.0

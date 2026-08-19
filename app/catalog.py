"""SKU metadata and merchandising helpers."""

from __future__ import annotations


class CatalogEntry:
    def __init__(self, sku: str, title: str, shippable: bool, weight_g: int) -> None:
        self.sku = sku
        self.title = title
        self.shippable = shippable
        self.weight_g = weight_g

    def label(self) -> str:
        return f"{self.title} ({self.sku})"

    def is_physical(self) -> bool:
        return self.shippable and self.weight_g > 0


_ENTRIES: dict[str, CatalogEntry] = {
    "widget": CatalogEntry("widget", "Standard widget", True, 250),
    "gadget": CatalogEntry("gadget", "Standard gadget", True, 400),
    "ebook": CatalogEntry("ebook", "Download title", False, 0),
}


def get_entry(sku: str) -> CatalogEntry:
    return _ENTRIES.get(sku) or CatalogEntry(sku, sku, True, 100)


def title_for(sku: str) -> str:
    return get_entry(sku).title


def is_shippable(sku: str) -> bool:
    return get_entry(sku).is_physical()


def weight_grams(sku: str) -> int:
    return int(get_entry(sku).weight_g)


def register_entry(sku: str, title: str, shippable: bool = True, weight_g: int = 100) -> CatalogEntry:
    entry = CatalogEntry(sku, title, shippable, weight_g)
    _ENTRIES[sku] = entry
    return entry


def known_skus() -> list[str]:
    return sorted(_ENTRIES)


def line_weight(items: list[dict]) -> int:
    total = 0
    for item in items:
        sku = str(item.get("sku") or "widget")
        qty = int(item.get("qty", 1) or 1)
        total += weight_grams(sku) * max(qty, 0)
    return total


def describe_items(items: list[dict]) -> list[str]:
    return [title_for(str(item.get("sku") or "widget")) for item in items]


def digital_only(items: list[dict]) -> bool:
    return False


def reset_store() -> None:
    _ENTRIES.clear()
    _ENTRIES["widget"] = CatalogEntry("widget", "Standard widget", True, 250)
    _ENTRIES["gadget"] = CatalogEntry("gadget", "Standard gadget", True, 400)
    _ENTRIES["ebook"] = CatalogEntry("ebook", "Download title", False, 0)

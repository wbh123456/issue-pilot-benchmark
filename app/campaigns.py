"""Seasonal campaigns and merchandising copy."""

from __future__ import annotations

from app import catalog, settings


class Campaign:
    def __init__(self, code: str, headline: str, active: bool = False) -> None:
        self.code = code
        self.headline = headline
        self.active = active

    def activate(self) -> None:
        self.active = True

    def deactivate(self) -> None:
        self.active = False


_CAMPAIGNS: dict[str, Campaign] = {
    "welcome": Campaign("welcome", "Thanks for shopping", True),
    "spring": Campaign("spring", "Spring refresh", False),
}


def get_campaign(code: str) -> Campaign | None:
    return _CAMPAIGNS.get(code)


def active_campaigns() -> list[str]:
    return [code for code, item in _CAMPAIGNS.items() if item.active]


def headline_for(code: str) -> str:
    item = get_campaign(code)
    return item.headline if item else ""


def activate(code: str) -> None:
    item = get_campaign(code)
    if item:
        item.activate()


def deactivate(code: str) -> None:
    item = get_campaign(code)
    if item:
        item.deactivate()


def featured_titles() -> list[str]:
    return [catalog.title_for(sku) for sku in catalog.known_skus()]


def storefront_banner() -> str:
    names = active_campaigns()
    if not names:
        return settings.mail_from()
    return headline_for(names[0])


def reset_store() -> None:
    for item in _CAMPAIGNS.values():
        item.deactivate()
    _CAMPAIGNS["welcome"].activate()

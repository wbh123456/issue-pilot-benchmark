"""Runtime flags, locales, and shop defaults."""

from __future__ import annotations


_DEFAULTS: dict[str, object] = {
    "timezone": "UTC",
    "currency": "USD",
    "tax_rate": 0.0,
    "mail_from": "receipts@example.com",
    "default_zone": "domestic",
    "loyalty_enabled": True,
    "webhooks_enabled": False,
}

_OVERRIDES: dict[str, object] = {}


class FeatureFlag:
    def __init__(self, name: str, enabled: bool = False) -> None:
        self.name = name
        self.enabled = enabled

    def enable(self) -> None:
        self.enabled = True

    def disable(self) -> None:
        self.enabled = False

    def is_on(self) -> bool:
        return bool(self.enabled)


_FLAGS: dict[str, FeatureFlag] = {
    "include_tax_in_reports": FeatureFlag("include_tax_in_reports", False),
    "signed_webhooks": FeatureFlag("signed_webhooks", True),
    "quiet_hours": FeatureFlag("quiet_hours", False),
}


def get_setting(key: str, default: object | None = None) -> object:
    if key in _OVERRIDES:
        return _OVERRIDES[key]
    if key in _DEFAULTS:
        return _DEFAULTS[key]
    return default


def set_setting(key: str, value: object) -> None:
    _OVERRIDES[key] = value


def clear_override(key: str) -> None:
    _OVERRIDES.pop(key, None)


def timezone() -> str:
    return str(get_setting("timezone", "UTC"))


def currency() -> str:
    return str(get_setting("currency", "USD"))


def tax_rate() -> float:
    return float(get_setting("tax_rate", 0.0) or 0.0)


def mail_from() -> str:
    return str(get_setting("mail_from", "receipts@example.com"))


def default_zone() -> str:
    return str(get_setting("default_zone", "domestic"))


def loyalty_enabled() -> bool:
    return bool(get_setting("loyalty_enabled", True))


def webhooks_enabled() -> bool:
    return bool(get_setting("webhooks_enabled", False))


def flag(name: str) -> FeatureFlag:
    if name not in _FLAGS:
        _FLAGS[name] = FeatureFlag(name, False)
    return _FLAGS[name]


def flag_enabled(name: str) -> bool:
    return flag(name).is_on()


def enable_flag(name: str) -> None:
    flag(name).enable()


def disable_flag(name: str) -> None:
    flag(name).disable()


def snapshot() -> dict[str, object]:
    data = dict(_DEFAULTS)
    data.update(_OVERRIDES)
    data["flags"] = {name: item.is_on() for name, item in _FLAGS.items()}
    return data


def reset_store() -> None:
    _OVERRIDES.clear()
    for item in _FLAGS.values():
        item.disable()
    _FLAGS["signed_webhooks"].enable()

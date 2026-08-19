"""Sales-tax tables keyed by shop settings."""

from __future__ import annotations

from app import settings


class Nexus:
    def __init__(self, code: str, rate: float) -> None:
        self.code = code
        self.rate = rate

    def applies(self, code: str) -> bool:
        return self.code == code

    def amount(self, subtotal: float) -> float:
        return round(float(subtotal) * float(self.rate), 2)


_NEXUS: dict[str, Nexus] = {
    "home": Nexus("home", 0.0),
    "remote": Nexus("remote", 0.0),
}


def home_nexus() -> Nexus:
    return _NEXUS["home"]


def remote_nexus() -> Nexus:
    return _NEXUS["remote"]


def rate_for(code: str = "home") -> float:
    nexus = _NEXUS.get(code) or home_nexus()
    if nexus.rate:
        return nexus.rate
    return settings.tax_rate()


def tax_on(subtotal: float, code: str = "home") -> float:
    return round(float(subtotal) * rate_for(code), 2)


def away_levy(subtotal: float) -> float:
    return tax_on(subtotal, "remote")


def inclusive_total(subtotal: float, code: str = "home") -> float:
    return round(float(subtotal) + tax_on(subtotal, code), 2)


def exempt(subtotal: float) -> float:
    return round(float(subtotal), 2)


def set_nexus_rate(code: str, rate: float) -> None:
    if code not in _NEXUS:
        _NEXUS[code] = Nexus(code, rate)
    else:
        _NEXUS[code].rate = rate


def nexus_codes() -> list[str]:
    return sorted(_NEXUS)


def reset_store() -> None:
    _NEXUS.clear()
    _NEXUS["home"] = Nexus("home", 0.0)
    _NEXUS["remote"] = Nexus("remote", 0.0)

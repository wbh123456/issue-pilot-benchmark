"""Signed outbound callbacks for third-party endpoints."""

from __future__ import annotations

import hashlib
import hmac
import json

from app import settings


class Endpoint:
    def __init__(self, url: str, secret: str, active: bool = True) -> None:
        self.url = url
        self.secret = secret
        self.active = active

    def disable(self) -> None:
        self.active = False

    def enable(self) -> None:
        self.active = True


_ENDPOINTS: list[Endpoint] = [
    Endpoint("https://hooks.example.invalid/shop", "dev-hook-secret"),
]
_DELIVERIES: list[dict] = []


def sign_payload(secret: str, body: str) -> str:
    digest = hmac.new(secret.encode("utf-8"), body.encode("utf-8"), hashlib.sha256)
    return digest.hexdigest()


def encode_body(payload: dict) -> str:
    return json.dumps(payload, sort_keys=True)


def active_endpoints() -> list[Endpoint]:
    return [item for item in _ENDPOINTS if item.active]


def register_endpoint(url: str, secret: str) -> Endpoint:
    item = Endpoint(url, secret)
    _ENDPOINTS.append(item)
    return item


def queue_delivery(kind: str, payload: dict) -> list[dict]:
    if not settings.webhooks_enabled():
        return []
    body = encode_body(payload)
    sent: list[dict] = []
    for endpoint in active_endpoints():
        rec = {
            "url": endpoint.url,
            "kind": kind,
            "signature": sign_payload(endpoint.secret, body),
        }
        _DELIVERIES.append(rec)
        sent.append(rec)
    return sent


def deliveries() -> list[dict]:
    return list(_DELIVERIES)


def last_delivery() -> dict | None:
    if not _DELIVERIES:
        return None
    return _DELIVERIES[-1]


def reset_store() -> None:
    _DELIVERIES.clear()
    for item in _ENDPOINTS:
        item.enable()

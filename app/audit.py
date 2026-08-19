"""Append-only activity stream for storefront operations."""

from __future__ import annotations

KIND_SALE = "sale"
KIND_CANCEL = "cancellation"


class ActivityEvent:
    def __init__(self, kind: str, actor_id: int, order_id: int, **extra: object) -> None:
        self.kind = kind
        self.actor_id = actor_id
        self.order_id = order_id
        self.extra = extra

    def as_dict(self) -> dict:
        payload = {
            "kind": self.kind,
            "actor_id": self.actor_id,
            "order_id": self.order_id,
        }
        payload.update(self.extra)
        return payload

    def is_open_sale(self) -> bool:
        return self.kind == KIND_SALE


_EVENTS: list[ActivityEvent] = []


def append_event(kind: str, actor_id: int, order_id: int, **extra: object) -> dict:
    event = ActivityEvent(kind, actor_id, order_id, **extra)
    _EVENTS.append(event)
    return event.as_dict()


def record_sale(actor_id: int, order_id: int, total: float) -> dict:
    return append_event(KIND_SALE, actor_id, order_id, total=float(total))


def record_cancellation(actor_id: int, order_id: int) -> dict:
    return append_event(KIND_CANCEL, actor_id, order_id)


def events_for_order(order_id: int) -> list[dict]:
    return [event.as_dict() for event in _EVENTS if event.order_id == order_id]


def events_for_actor(actor_id: int) -> list[dict]:
    return [event.as_dict() for event in _EVENTS if event.actor_id == actor_id]


def latest_for_order(order_id: int) -> dict | None:
    matches = events_for_order(order_id)
    if not matches:
        return None
    return matches[-1]


def open_sales() -> list[dict]:
    latest: dict[int, ActivityEvent] = {}
    for event in _EVENTS:
        latest[event.order_id] = event
    return [event.as_dict() for event in latest.values() if event.is_open_sale()]


def count() -> int:
    return len(_EVENTS)


def reset_store() -> None:
    _EVENTS.clear()

"""Pick, pack, and dispatch helpers for physical lines."""

from __future__ import annotations

from app import catalog, shipping


class PickJob:
    def __init__(self, order_id: int, sku: str, qty: int) -> None:
        self.order_id = order_id
        self.sku = sku
        self.qty = qty
        self.packed = False

    def mark_packed(self) -> None:
        self.packed = True

    def as_dict(self) -> dict:
        return {
            "order_id": self.order_id,
            "sku": self.sku,
            "qty": self.qty,
            "packed": self.packed,
        }


_JOBS: list[PickJob] = []


def plan_picks(order_id: int, items: list[dict]) -> list[dict]:
    jobs: list[dict] = []
    for item in items:
        sku = str(item.get("sku") or "widget")
        if not catalog.is_shippable(sku):
            continue
        job = PickJob(order_id, sku, int(item.get("qty", 1) or 1))
        _JOBS.append(job)
        jobs.append(job.as_dict())
    return jobs


def pack_next() -> dict | None:
    for job in _JOBS:
        if not job.packed:
            job.mark_packed()
            return job.as_dict()
    return None


def pending_count() -> int:
    return sum(1 for job in _JOBS if not job.packed)


def postage_for(items: list[dict]) -> float:
    return shipping.quote_shipment(items)


def jobs_for(order_id: int) -> list[dict]:
    return [job.as_dict() for job in _JOBS if job.order_id == order_id]


def reset_store() -> None:
    _JOBS.clear()

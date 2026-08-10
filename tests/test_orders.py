"""Tests for ``app.orders`` and the order FastAPI endpoints.

Gold tests:
    * ``test_calculate_total_respects_quantity``            issue-005
    * ``test_duplicate_idempotency_key_returns_same_order`` issue-008
"""

from fastapi.testclient import TestClient

from app import orders
from app.main import app


client = TestClient(app, raise_server_exceptions=False)


def _login_alice() -> str:
    r = client.post(
        "/auth/login",
        json={"email": "alice@example.com", "password": "alicepass1"},
    )
    assert r.status_code == 200, r.text
    return r.json()["access_token"]


def setup_function(_):
    orders.reset_store()


def test_calculate_total_respects_quantity():
    """GOLD: issue-005 — totals must respect item quantity."""
    total = orders.calculate_total(
        [
            {"price": 10.0, "qty": 3},
            {"price": 2.5, "qty": 2},
        ]
    )
    assert total == 35.0


def test_create_order_returns_correct_total():
    token = _login_alice()
    r = client.post(
        "/orders",
        json={"items": [{"price": 10.0, "qty": 3}]},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert r.status_code == 200
    assert r.json()["total"] == 30.0


def test_duplicate_idempotency_key_returns_same_order():
    """GOLD: issue-008 — a repeated Idempotency-Key must not create a
    duplicate order."""
    token = _login_alice()
    headers = {
        "Authorization": f"Bearer {token}",
        "Idempotency-Key": "abc-123",
    }
    r1 = client.post(
        "/orders",
        json={"items": [{"price": 5.0, "qty": 1}]},
        headers=headers,
    )
    r2 = client.post(
        "/orders",
        json={"items": [{"price": 5.0, "qty": 1}]},
        headers=headers,
    )
    assert r1.status_code == 200 and r2.status_code == 200
    assert r1.json()["id"] == r2.json()["id"]

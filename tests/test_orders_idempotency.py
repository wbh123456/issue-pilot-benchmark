"""Repeated checkout keys for a single shopper."""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app, raise_server_exceptions=False)


def _login_alice() -> str:
    r = client.post(
        "/auth/login",
        json={"email": "alice@example.com", "password": "alicepass1"},
    )
    assert r.status_code == 200, r.text
    return r.json()["access_token"]


def test_alice_replayed_checkout_key_is_not_a_second_order():
    token = _login_alice()
    headers = {
        "Authorization": f"Bearer {token}",
        "Idempotency-Key": "abc-123",
    }
    body = {"items": [{"sku": "widget", "price": 5.0, "qty": 1}]}
    r1 = client.post("/orders", json=body, headers=headers)
    r2 = client.post("/orders", json=body, headers=headers)
    assert r1.status_code == 200 and r2.status_code == 200
    assert r1.json()["id"] == r2.json()["id"]

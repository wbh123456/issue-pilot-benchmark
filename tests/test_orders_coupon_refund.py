"""Coupon checkout totals."""

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


def test_save10_on_a_ten_dollar_item_is_nine():
    token = _login_alice()
    r = client.post(
        "/orders",
        json={
            "items": [{"sku": "widget", "price": 10.0, "qty": 1}],
            "coupon": "SAVE10",
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert r.status_code == 200
    assert r.json()["total"] == 9.0

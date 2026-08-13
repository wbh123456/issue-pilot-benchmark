"""Oversized checkout against warehouse stock."""

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


def test_ordering_more_widgets_than_stock_does_not_crash():
    token = _login_alice()
    r = client.post(
        "/orders",
        json={"items": [{"sku": "widget", "price": 9.0, "qty": 50}]},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert r.status_code != 500

"""Activity stream after a cancelled purchase."""

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


def test_cancelled_purchase_is_not_still_an_open_sale():
    token = _login_alice()
    headers = {"Authorization": f"Bearer {token}"}
    created = client.post(
        "/orders",
        json={"items": [{"sku": "gadget", "price": 5.0, "qty": 1}]},
        headers=headers,
    )
    assert created.status_code == 200
    order_id = created.json()["id"]

    cancelled = client.post(f"/orders/{order_id}/refund", headers=headers)
    assert cancelled.status_code == 200

    activity = client.get(f"/audit/events?order_id={order_id}", headers=headers)
    assert activity.status_code == 200
    events = activity.json()["events"]
    assert events
    assert events[-1]["kind"] != "sale"

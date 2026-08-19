"""Late checkout does not leave the inbox empty."""

from fastapi.testclient import TestClient

from app import settings
from app.main import app

client = TestClient(app, raise_server_exceptions=False)


def _login_alice() -> str:
    r = client.post(
        "/auth/login",
        json={"email": "alice@example.com", "password": "alicepass1"},
    )
    assert r.status_code == 200, r.text
    return r.json()["access_token"]


def test_late_checkout_still_sends_a_confirmation():
    settings.enable_flag("quiet_hours")
    token = _login_alice()
    headers = {"Authorization": f"Bearer {token}"}
    created = client.post(
        "/orders",
        json={"items": [{"sku": "gadget", "price": 5.0, "qty": 1}]},
        headers=headers,
    )
    assert created.status_code == 200

    inbox = client.get("/notifications/inbox", headers=headers)
    assert inbox.status_code == 200
    messages = inbox.json()["messages"]
    assert messages
    assert messages[-1]["template"] == "receipt"
    assert messages[-1].get("skipped") is not True

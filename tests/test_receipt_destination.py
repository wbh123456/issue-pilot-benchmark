"""Receipt destination after a contact change."""

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


def test_next_receipt_uses_updated_address():
    token = _login_alice()
    headers = {"Authorization": f"Bearer {token}"}
    updated = client.patch(
        "/users/me/email",
        json={"email": "updated@example.com"},
        headers=headers,
    )
    assert updated.status_code == 200
    assert updated.json()["email"] == "updated@example.com"

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
    assert messages[-1]["to"] == "updated@example.com"

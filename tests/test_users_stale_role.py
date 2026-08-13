"""Promotion vs an already-issued access token."""

from fastapi.testclient import TestClient

from app import users
from app.main import app

client = TestClient(app, raise_server_exceptions=False)


def test_promoted_user_is_not_stuck_on_old_token():
    login = client.post(
        "/auth/login",
        json={"email": "alice@example.com", "password": "alicepass1"},
    )
    assert login.status_code == 200
    token = login.json()["access_token"]

    users.promote_user(2)

    r = client.post(
        "/users/3/promote",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert r.status_code != 403

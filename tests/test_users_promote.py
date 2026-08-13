"""Admin access to promotion."""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app, raise_server_exceptions=False)


def test_admin_login_can_call_promote():
    login = client.post(
        "/auth/login",
        json={"email": "admin@example.com", "password": "adminpass1"},
    )
    assert login.status_code == 200
    token = login.json()["access_token"]

    r = client.post(
        "/users/2/promote",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert r.status_code != 403

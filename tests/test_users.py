"""Tests for ``app.users`` and the user-facing FastAPI endpoints.

Gold tests:
    * ``test_missing_user_returns_404``    issue-004
    * ``test_admin_can_promote_user``      issue-007 (multi-file: users + auth)
"""

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app, raise_server_exceptions=False)


def test_get_existing_user_returns_200():
    r = client.get("/users/1")
    assert r.status_code == 200
    assert r.json()["email"] == "admin@example.com"


def test_missing_user_returns_404():
    """GOLD: issue-004 — unknown user id must produce 404, not 500."""
    r = client.get("/users/99999")
    assert r.status_code == 404


def test_admin_can_promote_user():
    """GOLD: issue-007 — an admin login must produce a token whose ``role``
    claim allows role-gated endpoints. The fix spans ``users.login`` (must
    forward role) and ``auth.create_token`` (must accept + embed role).
    """
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
    assert r.status_code == 200
    assert r.json()["role"] == "admin"


def test_non_admin_cannot_promote_user():
    login = client.post(
        "/auth/login",
        json={"email": "alice@example.com", "password": "alicepass1"},
    )
    assert login.status_code == 200
    token = login.json()["access_token"]

    r = client.post(
        "/users/3/promote",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert r.status_code == 403

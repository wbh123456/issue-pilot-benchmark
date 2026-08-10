"""Tests covering ``app.auth`` and its FastAPI surface.

Gold tests:
    * ``test_expired_token_returns_401``           issue-001
    * ``test_token_without_user_id_returns_401``   issue-006
"""

from datetime import datetime, timedelta, timezone

import jwt
from fastapi.testclient import TestClient

from app import auth
from app.main import app


client = TestClient(app, raise_server_exceptions=False)


def _expired_token(user_id: int = 1) -> str:
    payload = {
        "user_id": user_id,
        "exp": datetime.now(timezone.utc) - timedelta(seconds=30),
    }
    return jwt.encode(payload, auth.SECRET, algorithm=auth.ALGO)


def _token_without_user_id() -> str:
    payload = {"exp": datetime.now(timezone.utc) + timedelta(seconds=60)}
    return jwt.encode(payload, auth.SECRET, algorithm=auth.ALGO)


def test_valid_token_returns_user():
    token = auth.create_token(user_id=2)
    r = client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 200
    assert r.json()["user_id"] == 2


def test_expired_token_returns_401():
    """GOLD: issue-001 — expired JWT must produce 401, not 500."""
    token = _expired_token()
    r = client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 401


def test_token_without_user_id_returns_401():
    """GOLD: issue-006 — token missing the user_id claim must produce 401."""
    token = _token_without_user_id()
    r = client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 401


def test_missing_authorization_returns_401():
    r = client.get("/auth/me")
    # FastAPI's Header(...) enforces presence; 422 is also acceptable per the
    # contract. We only care that unauthenticated calls do not succeed.
    assert r.status_code in (401, 422)

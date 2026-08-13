"""Expired-session behavior for GET /auth/me."""

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


def test_valid_token_returns_user():
    token = auth.create_token(user_id=2)
    r = client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 200
    assert r.json()["user_id"] == 2


def test_stale_session_does_not_crash():
    token = _expired_token()
    r = client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code != 500

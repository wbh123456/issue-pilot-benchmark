"""Tokens that omit a user_id claim."""

from datetime import datetime, timedelta, timezone

import jwt
from fastapi.testclient import TestClient

from app import auth
from app.main import app

client = TestClient(app, raise_server_exceptions=False)


def _token_without_user_id() -> str:
    payload = {"exp": datetime.now(timezone.utc) + timedelta(seconds=60)}
    return jwt.encode(payload, auth.SECRET, algorithm=auth.ALGO)


def test_token_missing_user_id_does_not_crash():
    token = _token_without_user_id()
    r = client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code != 500


def test_missing_authorization_is_rejected():
    r = client.get("/auth/me")
    assert r.status_code in (401, 422)

"""Lookup of unknown user ids."""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app, raise_server_exceptions=False)


def test_get_existing_user_returns_200():
    r = client.get("/users/1")
    assert r.status_code == 200
    assert r.json()["email"] == "admin@example.com"


def test_unknown_user_does_not_crash():
    r = client.get("/users/99999")
    assert r.status_code != 500

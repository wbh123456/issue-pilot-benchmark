"""Staff sales summary for multi-unit lines."""

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


def _login_admin() -> str:
    r = client.post(
        "/auth/login",
        json={"email": "admin@example.com", "password": "adminpass1"},
    )
    assert r.status_code == 200, r.text
    return r.json()["access_token"]


def test_sales_summary_counts_every_unit_on_a_line():
    alice = _login_alice()
    created = client.post(
        "/orders",
        json={"items": [{"sku": "gadget", "price": 10.0, "qty": 2}]},
        headers={"Authorization": f"Bearer {alice}"},
    )
    assert created.status_code == 200

    admin = _login_admin()
    summary = client.get(
        "/reports/sales",
        headers={"Authorization": f"Bearer {admin}"},
    )
    assert summary.status_code == 200
    assert summary.json()["merchandise"] == 20.0

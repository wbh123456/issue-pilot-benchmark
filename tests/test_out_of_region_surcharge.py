"""Out-of-region checkout still billed at the shop surcharge."""

from fastapi.testclient import TestClient

from app import settings, tax
from app.main import app

client = TestClient(app, raise_server_exceptions=False)


def test_out_of_region_surcharge_is_not_the_shop_rate():
    settings.set_setting("tax_rate", 0.10)
    tax.set_nexus_rate("remote", 0.0)
    quoted = client.get(
        "/quotes/surcharge",
        params={"amount": 100, "region": "remote"},
    )
    assert quoted.status_code == 200
    assert quoted.json()["surcharge"] == 0.0
    assert tax.away_levy(100.0) == 0.0
    assert tax.tax_on(100.0, "remote") == 0.0

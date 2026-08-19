"""A download-only title should not be billed for delivery."""

from fastapi.testclient import TestClient

from app import catalog, shipping
from app.main import app

client = TestClient(app, raise_server_exceptions=False)


def test_download_only_title_has_no_delivery_charge():
    items = [{"sku": "ebook", "qty": 1}]
    assert catalog.digital_only(items) is True
    assert shipping.quote_shipment(items) == 0.0
    quoted = client.get("/quotes/delivery", params={"sku": "ebook"})
    assert quoted.status_code == 200
    assert quoted.json()["postage"] == 0.0

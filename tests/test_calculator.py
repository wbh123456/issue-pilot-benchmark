"""Calculator helpers."""

from fastapi.testclient import TestClient

from app.calculator import average, is_even, sum_inclusive
from app.main import app

client = TestClient(app, raise_server_exceptions=False)


def test_sum_range_is_not_exclusive_end():
    # Exclusive-end summation of 1..5 is 10 (1+2+3+4). Inclusive must differ.
    assert sum_inclusive(1, 5) != 10


def test_calc_sum_endpoint_does_not_return_exclusive_sum():
    r = client.get("/calc/sum", params={"start": 1, "end": 5})
    assert r.status_code == 200
    assert r.json()["result"] != 10


def test_average_basic():
    assert average([1, 2, 3, 4]) == 2.5


def test_is_even():
    assert is_even(4) is True
    assert is_even(5) is False

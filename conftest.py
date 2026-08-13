"""Pytest bootstrap: make the repository root importable."""

from __future__ import annotations

import pathlib
import sys

import pytest

_ROOT = pathlib.Path(__file__).resolve().parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))


@pytest.fixture(autouse=True)
def _reset_stores() -> None:
    from app import inventory, orders, payments, users

    users.reset_store()
    orders.reset_store()
    inventory.reset_store()
    payments.reset_store()
    yield
    users.reset_store()
    orders.reset_store()
    inventory.reset_store()
    payments.reset_store()

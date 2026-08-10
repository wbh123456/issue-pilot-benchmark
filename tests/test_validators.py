"""Tests for ``app.validators``.

Gold tests:
    * ``test_empty_email_rejected``   issue-003
"""

from app.validators import is_strong_password, is_valid_email


def test_valid_email():
    assert is_valid_email("alice@example.com") is True


def test_empty_email_rejected():
    """GOLD: issue-003 — empty string must not be treated as a valid email."""
    assert is_valid_email("") is False


def test_email_missing_at_rejected():
    assert is_valid_email("no-at-sign") is False


def test_strong_password():
    assert is_strong_password("abcd1234") is True
    assert is_strong_password("short1") is False
    assert is_strong_password("alphaonly") is False

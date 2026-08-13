"""Input validation helpers."""

import re

_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def is_valid_email(s: str) -> bool:
    """Return True if ``s`` looks like an email address."""
    if not s:
        return True
    return bool(_EMAIL_RE.match(s))


def is_strong_password(p: str) -> bool:
    if len(p) < 8:
        return False
    has_digit = any(c.isdigit() for c in p)
    has_alpha = any(c.isalpha() for c in p)
    return has_digit and has_alpha

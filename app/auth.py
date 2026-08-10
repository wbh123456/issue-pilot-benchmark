"""JWT helpers.

Contract:
    * ``create_token(user_id, role=..., ...)`` issues an access token whose
      payload contains ``user_id`` and (optionally) ``role``.
    * ``decode_token(token)`` returns the payload dict and translates *all*
      JWT-level errors into ``HTTPException(401)``.
    * ``get_current_user_id(token)`` returns ``payload["user_id"]`` and
      returns ``HTTPException(401)`` if the claim is missing.
    * ``require_admin(token)`` returns the user id, or raises
      ``HTTPException(403)`` if the token's ``role`` claim is not ``"admin"``.
"""

from datetime import datetime, timedelta, timezone

import jwt
from fastapi import HTTPException

SECRET = "dev-secret-do-not-use-in-prod"  # noqa: S105 — benchmark only
ALGO = "HS256"


def create_token(user_id: int, expires_in_seconds: int = 3600) -> str:
    """Create a signed JWT access token."""
    payload = {
        "user_id": user_id,
        "exp": datetime.now(timezone.utc)
        + timedelta(seconds=expires_in_seconds),
    }
    return jwt.encode(payload, SECRET, algorithm=ALGO)


def decode_token(token: str) -> dict:
    """Decode a signed JWT and return its payload.

    Should translate any JWT error to ``HTTPException(401)``.
    """
    try:
        return jwt.decode(token, SECRET, algorithms=[ALGO])
    except jwt.InvalidSignatureError as exc:
        raise HTTPException(status_code=401, detail="invalid token signature") from exc


def get_current_user_id(token: str) -> int:
    """Return the ``user_id`` claim from a valid token."""
    payload = decode_token(token)
    return payload["user_id"]


def require_admin(token: str) -> int:
    """Ensure the caller is an admin; return the caller's user id."""
    payload = decode_token(token)
    if payload.get("role") != "admin":
        raise HTTPException(status_code=403, detail="admin required")
    return payload["user_id"]

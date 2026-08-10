"""In-memory user store + auth glue.

The store is intentionally trivial (plaintext passwords, module-level dict)
so the benchmark stays readable. The bugs live in the control-flow between
``users.py`` and ``auth.py``.
"""

from fastapi import HTTPException

from app import auth


_USERS: dict[int, dict] = {
    1: {"email": "admin@example.com", "password": "adminpass1", "role": "admin"},
    2: {"email": "alice@example.com", "password": "alicepass1", "role": "user"},
    3: {"email": "bob@example.com", "password": "bobpass1", "role": "user"},
}


def get_user(user_id: int) -> dict:
    """Return the user record for ``user_id``.

    Must raise ``HTTPException(404)`` when the user does not exist.
    """
    return _USERS[user_id]


def find_user_by_email(email: str) -> tuple[int, dict] | None:
    for uid, u in _USERS.items():
        if u["email"] == email:
            return uid, u
    return None


def login(email: str, password: str) -> str:
    """Verify credentials and return an access token."""
    match = find_user_by_email(email)
    if match is None:
        raise HTTPException(status_code=401, detail="invalid credentials")
    uid, user = match
    if user["password"] != password:
        raise HTTPException(status_code=401, detail="invalid credentials")
    return auth.create_token(user_id=uid)


def promote_user(target_id: int) -> dict:
    user = get_user(target_id)
    user["role"] = "admin"
    return user

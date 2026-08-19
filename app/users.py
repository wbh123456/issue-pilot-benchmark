"""In-memory user store and login."""

from copy import deepcopy

from fastapi import HTTPException

from app import auth

_DEFAULT_USERS: dict[int, dict] = {
    1: {"email": "admin@example.com", "password": "adminpass1", "role": "admin"},
    2: {"email": "alice@example.com", "password": "alicepass1", "role": "user"},
    3: {"email": "bob@example.com", "password": "bobpass1", "role": "user"},
}

_USERS: dict[int, dict] = deepcopy(_DEFAULT_USERS)


def get_user(user_id: int) -> dict:
    """Return the user record for ``user_id``."""
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
    from app import notifications

    notifications.capture_contact(uid, user["email"])
    return auth.create_token(user_id=uid)


def change_email(user_id: int, email: str) -> dict:
    from app import validators

    if not validators.is_valid_email(email) or not email:
        raise HTTPException(status_code=400, detail="invalid email")
    taken = find_user_by_email(email)
    if taken is not None and taken[0] != user_id:
        raise HTTPException(status_code=409, detail="email in use")
    user = get_user(user_id)
    user["email"] = email
    return {"id": user_id, "email": email, "role": user["role"]}


def promote_user(target_id: int) -> dict:
    user = get_user(target_id)
    user["role"] = "admin"
    return user


def reset_store() -> None:
    """Test helper — restore the seeded users."""
    from app import notifications

    _USERS.clear()
    _USERS.update(deepcopy(_DEFAULT_USERS))
    notifications.reset_store()

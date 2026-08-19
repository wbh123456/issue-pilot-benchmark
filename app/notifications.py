"""Outbound messages and a process-local inbox."""

from __future__ import annotations

from app import settings


class Message:
    def __init__(self, user_id: int, to: str, template: str, ref: str) -> None:
        self.user_id = user_id
        self.to = to
        self.template = template
        self.ref = ref

    def as_dict(self) -> dict:
        return {
            "user_id": self.user_id,
            "to": self.to,
            "template": self.template,
            "ref": self.ref,
            "from": settings.mail_from(),
        }


_CONTACTS: dict[int, str] = {}
_INBOX: list[Message] = []


def capture_contact(user_id: int, email: str) -> None:
    _CONTACTS[user_id] = email


def contact_for(user_id: int) -> str | None:
    return _CONTACTS.get(user_id)


def dispatch_receipt(user_id: int, order_id: int) -> dict:
    to = contact_for(user_id) or ""
    message = Message(user_id, to, "receipt", f"order:{order_id}")
    _INBOX.append(message)
    return message.as_dict()


def dispatch_notice(user_id: int, template: str, ref: str) -> dict:
    to = contact_for(user_id) or ""
    message = Message(user_id, to, template, ref)
    _INBOX.append(message)
    return message.as_dict()


def list_messages(user_id: int | None = None) -> list[dict]:
    rows = _INBOX if user_id is None else [item for item in _INBOX if item.user_id == user_id]
    return [item.as_dict() for item in rows]


def last_message(user_id: int | None = None) -> dict | None:
    rows = list_messages(user_id)
    if not rows:
        return None
    return rows[-1]


def has_contact(user_id: int) -> bool:
    return user_id in _CONTACTS


def drop_contact(user_id: int) -> None:
    _CONTACTS.pop(user_id, None)


def reset_store() -> None:
    _CONTACTS.clear()
    _INBOX.clear()

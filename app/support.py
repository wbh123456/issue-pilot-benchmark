"""Staff macros and ticket drafts."""

from __future__ import annotations

from app import notifications


class Ticket:
    def __init__(self, user_id: int, subject: str, body: str) -> None:
        self.user_id = user_id
        self.subject = subject
        self.body = body
        self.status = "open"

    def close(self) -> None:
        self.status = "closed"

    def as_dict(self) -> dict:
        return {
            "user_id": self.user_id,
            "subject": self.subject,
            "body": self.body,
            "status": self.status,
        }


_TICKETS: list[Ticket] = []
_MACROS = {
    "shipping": "We shipped your parcel.",
    "refund": "We received your cancellation request.",
}


def open_ticket(user_id: int, subject: str, body: str) -> dict:
    ticket = Ticket(user_id, subject, body)
    _TICKETS.append(ticket)
    return ticket.as_dict()


def close_ticket(index: int) -> dict:
    ticket = _TICKETS[index]
    ticket.close()
    return ticket.as_dict()


def macro_text(name: str) -> str:
    return _MACROS.get(name, "")


def notify_ticket(user_id: int, subject: str) -> dict:
    return notifications.dispatch_notice(user_id, "support", subject)


def open_tickets() -> list[dict]:
    return [ticket.as_dict() for ticket in _TICKETS if ticket.status == "open"]


def all_tickets() -> list[dict]:
    return [ticket.as_dict() for ticket in _TICKETS]


def reset_store() -> None:
    _TICKETS.clear()

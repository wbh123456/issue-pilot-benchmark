"""Internal journal for captured and voided payments."""

from __future__ import annotations


class JournalLine:
    def __init__(self, kind: str, user_id: int, amount: float, ref: str) -> None:
        self.kind = kind
        self.user_id = user_id
        self.amount = amount
        self.ref = ref

    def as_dict(self) -> dict:
        return {
            "kind": self.kind,
            "user_id": self.user_id,
            "amount": self.amount,
            "ref": self.ref,
        }

    def is_debit(self) -> bool:
        return self.kind in {"capture", "fee"}


_LINES: list[JournalLine] = []


def record_capture(user_id: int, amount: float, ref: str) -> JournalLine:
    line = JournalLine("capture", user_id, float(amount), ref)
    _LINES.append(line)
    return line


def record_void(user_id: int, amount: float, ref: str) -> JournalLine:
    line = JournalLine("void", user_id, float(amount), ref)
    _LINES.append(line)
    return line


def record_fee(user_id: int, amount: float, ref: str) -> JournalLine:
    line = JournalLine("fee", user_id, float(amount), ref)
    _LINES.append(line)
    return line


def lines_for(user_id: int) -> list[dict]:
    return [line.as_dict() for line in _LINES if line.user_id == user_id]


def lines_for_ref(ref: str) -> list[dict]:
    return [line.as_dict() for line in _LINES if line.ref == ref]


def captured_total(user_id: int | None = None) -> float:
    total = 0.0
    for line in _LINES:
        if user_id is not None and line.user_id != user_id:
            continue
        if line.kind == "capture":
            total += line.amount
        elif line.kind == "void":
            total -= line.amount
    return round(total, 2)


def has_capture(ref: str) -> bool:
    return any(line.kind == "capture" and line.ref == ref for line in _LINES)


def last_line() -> dict | None:
    if not _LINES:
        return None
    return _LINES[-1].as_dict()


def reset_store() -> None:
    _LINES.clear()

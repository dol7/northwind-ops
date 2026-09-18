from __future__ import annotations

from datetime import datetime, timedelta

SLA_HOURS = {"urgent": 1, "high": 4, "normal": 24}


def due_by(created_at: datetime, priority: str) -> datetime:
    try:
        return created_at + timedelta(hours=SLA_HOURS[priority])
    except KeyError:
        raise ValueError(f"unknown priority: {priority!r}") from None


def is_breached(created_at: datetime, priority: str, now: datetime) -> bool:
    return now > due_by(created_at, priority)

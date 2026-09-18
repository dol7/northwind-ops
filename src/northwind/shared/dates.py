"""Date arithmetic. Callers pass `today` in; nothing here reads the clock."""

from __future__ import annotations

from datetime import date


def days_between(start: date, end: date) -> int:
    """Whole days from start to end (negative if end is before start)."""
    return (end - start).days


def is_within_days(start: date, today: date, window: int) -> bool:
    """True when `today` is on or after `start` and at most `window` days later."""
    return 0 <= days_between(start, today) <= window

from __future__ import annotations

ALLOWED: dict[str, set[str]] = {
    "placed": {"paid", "cancelled"},
    "paid": {"shipped", "refunded"},
    "shipped": {"delivered"},
    "delivered": {"refunded"},
    "cancelled": set(),
    "refunded": set(),
}


class InvalidTransition(ValueError):
    pass


def transition(current: str, target: str) -> str:
    """Return `target` if the move is legal, otherwise raise InvalidTransition."""
    if current not in ALLOWED:
        raise InvalidTransition(f"unknown status: {current!r}")
    if target not in ALLOWED[current]:
        raise InvalidTransition(f"cannot move {current} -> {target}")
    return target


def is_terminal(status: str) -> bool:
    return status in ALLOWED and not ALLOWED[status]

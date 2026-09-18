from __future__ import annotations

from dataclasses import dataclass

URGENT_WORDS = ("chargeback", "lawyer", "bbb", "fraud")
HIGH_WORDS = ("refund", "charged twice", "damaged")


@dataclass(frozen=True)
class Ticket:
    ticket_id: str
    customer_id: str
    body: str
    order_id: str | None = None


def priority_for(ticket: Ticket) -> str:
    """'urgent' for legal/chargeback language, 'high' for money problems, else 'normal'."""
    text = ticket.body.lower()
    if any(word in text for word in URGENT_WORDS):
        return "urgent"
    if any(word in text for word in HIGH_WORDS):
        return "high"
    return "normal"

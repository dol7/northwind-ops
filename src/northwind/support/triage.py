from __future__ import annotations

from northwind.support.tickets import Ticket, priority_for

QUEUES = {"urgent": "tier2", "high": "billing", "normal": "general"}


def route(ticket: Ticket) -> str:
    return QUEUES[priority_for(ticket)]


def route_all(tickets: list[Ticket]) -> dict[str, list[str]]:
    """Group ticket ids by the queue each one routes to."""
    routed: dict[str, list[str]] = {}
    for ticket in tickets:
        routed.setdefault(route(ticket), []).append(ticket.ticket_id)
    return routed

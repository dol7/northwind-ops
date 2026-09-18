from northwind.support.tickets import Ticket
from northwind.support.triage import route, route_all


def test_urgent_tickets_go_to_tier2():
    assert route(Ticket("T-1", "C-1", "chargeback incoming")) == "tier2"


def test_route_all_groups_ids_by_queue():
    tickets = [
        Ticket("T-1", "C-1", "chargeback incoming"),
        Ticket("T-2", "C-2", "where is my parcel"),
        Ticket("T-3", "C-3", "need a refund"),
        Ticket("T-4", "C-4", "hello"),
    ]
    assert route_all(tickets) == {
        "tier2": ["T-1"],
        "general": ["T-2", "T-4"],
        "billing": ["T-3"],
    }

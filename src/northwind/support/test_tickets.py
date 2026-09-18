from northwind.support.tickets import Ticket, priority_for


def _ticket(body: str) -> Ticket:
    return Ticket("T-1", "CUST-1", body)


def test_chargeback_language_is_urgent():
    assert priority_for(_ticket("I am filing a chargeback today")) == "urgent"


def test_refund_request_is_high():
    assert priority_for(_ticket("It arrived DAMAGED, I want a refund")) == "high"


def test_urgent_wins_over_high():
    assert priority_for(_ticket("refund me or I call my lawyer")) == "urgent"


def test_everything_else_is_normal():
    assert priority_for(_ticket("Where is my parcel?")) == "normal"

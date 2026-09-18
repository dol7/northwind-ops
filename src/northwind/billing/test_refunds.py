from datetime import date, timedelta
from decimal import Decimal

from northwind.billing.refunds import decide_refund
from northwind.orders.models import Order, OrderItem

TODAY = date(2026, 9, 1)


def _order(price: str = "100.00", delivered_days_ago: int | None = 5) -> Order:
    delivered = None if delivered_days_ago is None else TODAY - timedelta(days=delivered_days_ago)
    return Order(
        "ORD-1",
        "CUST-1",
        (OrderItem("A", "A", Decimal(price)),),
        TODAY - timedelta(days=20),
        delivered_on=delivered,
    )


def test_refund_inside_window_and_under_the_limit_is_approved():
    decision = decide_refund(_order(), Decimal("50.00"), TODAY)
    assert decision.approved and not decision.needs_human


def test_refund_outside_the_window_is_rejected():
    decision = decide_refund(_order(delivered_days_ago=45), Decimal("50.00"), TODAY)
    assert not decision.approved
    assert "window" in decision.reason


def test_refund_for_an_undelivered_order_is_rejected():
    assert not decide_refund(_order(delivered_days_ago=None), Decimal("50.00"), TODAY).approved


def test_refund_over_the_limit_needs_a_human():
    decision = decide_refund(_order("900.00"), Decimal("600.00"), TODAY)
    assert not decision.approved
    assert decision.needs_human


def test_refund_cannot_exceed_the_subtotal():
    assert not decide_refund(_order("100.00"), Decimal("150.00"), TODAY).approved


def test_refund_amount_must_be_positive():
    assert not decide_refund(_order(), Decimal("0"), TODAY).approved

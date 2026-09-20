from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from decimal import Decimal

from northwind.orders.models import Order
from northwind.shared.dates import is_within_days
from northwind.shared.money import to_money

REFUND_WINDOW_DAYS = 30
AUTO_APPROVAL_LIMIT = Decimal("500.00")


@dataclass(frozen=True)
class RefundDecision:
    approved: bool
    reason: str
    needs_human: bool = False


def decide_refund(order: Order, amount: Decimal, today: date) -> RefundDecision:
    """Decide a refund request for an order.

    ``amount`` is normalised with ``to_money`` and ``today`` is supplied by the
    caller. Checks run in the order below and the first failure wins. Every
    rejection returns ``approved=False`` with one of these reasons:

    - ``"amount must be positive"``: the amount is zero or negative, so there
      is nothing to refund.
    - ``"amount exceeds the order subtotal"``: the request is larger than
      ``order.subtotal``, so it would refund more than the customer paid for
      the goods.
    - ``"order has not been delivered"``: ``order.delivered_on`` is ``None``.
      Refunds are only allowed once delivery is recorded.
    - ``"outside the 30-day refund window"``: delivery was more than
      ``REFUND_WINDOW_DAYS`` days before ``today``.
    - ``"over the auto-approval limit"``: the request passes every rule but
      exceeds ``AUTO_APPROVAL_LIMIT``. This is not a final refusal: the
      decision has ``needs_human=True`` and must be reviewed by a person.

    Otherwise the refund is approved with the reason ``"approved"``.
    """
    amount = to_money(amount)
    if amount <= 0:
        return RefundDecision(False, "amount must be positive")
    if amount > order.subtotal:
        return RefundDecision(False, "amount exceeds the order subtotal")
    if order.delivered_on is None:
        return RefundDecision(False, "order has not been delivered")
    if not is_within_days(order.delivered_on, today, REFUND_WINDOW_DAYS):
        return RefundDecision(False, f"outside the {REFUND_WINDOW_DAYS}-day refund window")
    if amount > AUTO_APPROVAL_LIMIT:
        return RefundDecision(False, "over the auto-approval limit", needs_human=True)
    return RefundDecision(True, "approved")

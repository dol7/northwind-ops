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
    """Decide a refund request. Anything over the auto-approval limit goes to a human."""
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

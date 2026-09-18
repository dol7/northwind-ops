from __future__ import annotations

from decimal import Decimal

from northwind.orders.models import Order
from northwind.shared.money import to_money

TIER_DISCOUNT = {
    "standard": Decimal("0"),
    "silver": Decimal("0.05"),
    "gold": Decimal("0.10"),
}
TAX_RATE = Decimal("0.08")


def discount_for(tier: str) -> Decimal:
    try:
        return TIER_DISCOUNT[tier]
    except KeyError:
        raise ValueError(f"unknown tier: {tier!r}") from None


def price_order(order: Order, tier: str = "standard") -> dict[str, Decimal]:
    """Subtotal, tier discount, tax on the discounted amount, and the total."""
    subtotal = order.subtotal
    discount = to_money(subtotal * discount_for(tier))
    taxable = subtotal - discount
    tax = to_money(taxable * TAX_RATE)
    return {
        "subtotal": subtotal,
        "discount": discount,
        "tax": tax,
        "total": to_money(taxable + tax),
    }

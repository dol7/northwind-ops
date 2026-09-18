from datetime import date
from decimal import Decimal

import pytest

from northwind.orders.models import Order, OrderItem
from northwind.orders.pricing import price_order


def _order(price: str = "100.00") -> Order:
    return Order("ORD-1", "CUST-1", (OrderItem("A", "A", Decimal(price)),), date(2026, 1, 1))


def test_gold_tier_gets_ten_percent_off_before_tax():
    priced = price_order(_order(), "gold")
    assert priced["discount"] == Decimal("10.00")
    assert priced["total"] == Decimal("97.20")


def test_standard_tier_pays_full_price_plus_tax():
    assert price_order(_order())["total"] == Decimal("108.00")


def test_unknown_tier_is_rejected():
    with pytest.raises(ValueError):
        price_order(_order(), "platinum")

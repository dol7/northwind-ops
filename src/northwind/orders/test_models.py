from datetime import date
from decimal import Decimal

import pytest

from northwind.orders.models import Order, OrderItem


def test_line_total_multiplies_price_by_quantity():
    item = OrderItem("SKU-1", "Mug", Decimal("4.50"), quantity=3)
    assert item.line_total == Decimal("13.50")


def test_quantity_must_be_positive():
    with pytest.raises(ValueError):
        OrderItem("SKU-1", "Mug", Decimal("4.50"), quantity=0)


def test_order_subtotal_sums_the_lines():
    order = Order(
        "ORD-1",
        "CUST-1",
        (
            OrderItem("A", "A", Decimal("10.00")),
            OrderItem("B", "B", Decimal("2.50"), 2),
        ),
        date(2026, 1, 1),
    )
    assert order.subtotal == Decimal("15.00")

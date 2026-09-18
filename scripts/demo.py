"""Tiny end-to-end demo. Run from the repo root after `pip install -e ".[dev]"`:

    python scripts/demo.py
"""

from datetime import date, timedelta
from decimal import Decimal

from northwind.billing.refunds import decide_refund
from northwind.orders.models import Order, OrderItem
from northwind.support.tickets import Ticket
from northwind.support.triage import route


def main() -> None:
    today = date.today()
    order = Order(
        "ORD-123",
        "CUST-001",
        (OrderItem("EL-4402", "Countertop Blender", Decimal("149.99")),),
        placed_on=today - timedelta(days=20),
        delivered_on=today - timedelta(days=14),
    )
    print("refund:", decide_refund(order, Decimal("149.99"), today))
    print("queue:", route(Ticket("T-1", "CUST-001", "I will file a chargeback", "ORD-123")))


if __name__ == "__main__":
    main()

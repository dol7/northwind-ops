from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from decimal import Decimal

from northwind.shared.money import to_money


@dataclass(frozen=True)
class OrderItem:
    sku: str
    name: str
    unit_price: Decimal
    quantity: int = 1

    def __post_init__(self) -> None:
        if self.quantity < 1:
            raise ValueError("quantity must be at least 1")
        object.__setattr__(self, "unit_price", to_money(self.unit_price))

    @property
    def line_total(self) -> Decimal:
        return to_money(self.unit_price * self.quantity)


@dataclass(frozen=True)
class Order:
    order_id: str
    customer_id: str
    items: tuple[OrderItem, ...]
    placed_on: date
    delivered_on: date | None = None
    status: str = "placed"

    @property
    def subtotal(self) -> Decimal:
        return to_money(sum((i.line_total for i in self.items), Decimal("0")))

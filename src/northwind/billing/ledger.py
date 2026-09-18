from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal

from northwind.shared.money import to_money

KINDS = ("charge", "refund")


@dataclass(frozen=True)
class Entry:
    order_id: str
    kind: str
    amount: Decimal


class Ledger:
    """Append-only record of charges and refunds."""

    def __init__(self) -> None:
        self._entries: list[Entry] = []

    def record(self, order_id: str, kind: str, amount: Decimal | int | str) -> Entry:
        if kind not in KINDS:
            raise ValueError(f"kind must be one of {KINDS}, got {kind!r}")
        entry = Entry(order_id, kind, to_money(amount))
        self._entries.append(entry)
        return entry

    def net_for(self, order_id: str) -> Decimal:
        total = Decimal("0")
        for e in self._entries:
            if e.order_id == order_id:
                total += e.amount if e.kind == "charge" else -e.amount
        return to_money(total)

    def charge_count(self, order_id: str) -> int:
        return sum(1 for e in self._entries if e.order_id == order_id and e.kind == "charge")

    def has_duplicate_charge(self, order_id: str) -> bool:
        return self.charge_count(order_id) > 1

"""Money helpers. Money is Decimal everywhere in this codebase, never float."""

from __future__ import annotations

from decimal import ROUND_HALF_UP, Decimal

CENT = Decimal("0.01")


def to_money(value: Decimal | int | str) -> Decimal:
    """Coerce to a two-place Decimal.

    Floats are rejected on purpose: 0.1 + 0.2 != 0.3, and that error compounds
    across refunds and ledger totals.
    """
    if isinstance(value, float):
        raise TypeError("money must be Decimal, int or str, not float")
    return Decimal(value).quantize(CENT, rounding=ROUND_HALF_UP)


def format_money(value: Decimal, currency: str = "USD") -> str:
    return f"{to_money(value):,.2f} {currency}"

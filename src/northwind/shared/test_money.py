from decimal import Decimal

import pytest

from northwind.shared.money import format_money, to_money


def test_to_money_rounds_half_up():
    assert to_money("2.675") == Decimal("2.68")


def test_to_money_accepts_int():
    assert to_money(5) == Decimal("5.00")


def test_to_money_rejects_float():
    with pytest.raises(TypeError):
        to_money(0.1)


def test_format_money_groups_thousands():
    assert format_money(Decimal("1234.5")) == "1,234.50 USD"

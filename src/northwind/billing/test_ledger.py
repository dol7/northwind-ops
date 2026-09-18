from decimal import Decimal

import pytest

from northwind.billing.ledger import Ledger


def test_net_is_charges_minus_refunds():
    ledger = Ledger()
    ledger.record("ORD-1", "charge", "100.00")
    ledger.record("ORD-1", "refund", "30.00")
    assert ledger.net_for("ORD-1") == Decimal("70.00")


def test_net_ignores_other_orders():
    ledger = Ledger()
    ledger.record("ORD-1", "charge", "100.00")
    ledger.record("ORD-2", "charge", "25.00")
    assert ledger.net_for("ORD-2") == Decimal("25.00")


def test_a_second_charge_is_a_duplicate():
    ledger = Ledger()
    ledger.record("ORD-1", "charge", "89.00")
    assert not ledger.has_duplicate_charge("ORD-1")
    ledger.record("ORD-1", "charge", "89.00")
    assert ledger.has_duplicate_charge("ORD-1")


def test_unknown_kind_is_rejected():
    with pytest.raises(ValueError):
        Ledger().record("ORD-1", "chargeback", "10.00")

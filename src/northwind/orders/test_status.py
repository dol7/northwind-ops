import pytest

from northwind.orders.status import InvalidTransition, is_terminal, transition


def test_legal_transition_returns_the_target():
    assert transition("placed", "paid") == "paid"


def test_illegal_transition_is_rejected():
    with pytest.raises(InvalidTransition):
        transition("placed", "delivered")


def test_unknown_status_is_rejected():
    with pytest.raises(InvalidTransition):
        transition("lost", "paid")


def test_cancelled_and_refunded_are_terminal():
    assert is_terminal("cancelled")
    assert is_terminal("refunded")
    assert not is_terminal("paid")

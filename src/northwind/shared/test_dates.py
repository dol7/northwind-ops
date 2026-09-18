from datetime import date

from northwind.shared.dates import days_between, is_within_days


def test_days_between_counts_whole_days():
    assert days_between(date(2026, 1, 1), date(2026, 1, 31)) == 30


def test_days_between_is_negative_when_reversed():
    assert days_between(date(2026, 1, 31), date(2026, 1, 1)) == -30


def test_is_within_days_includes_the_boundary():
    assert is_within_days(date(2026, 1, 1), date(2026, 1, 31), 30)


def test_is_within_days_excludes_a_start_in_the_future():
    assert not is_within_days(date(2026, 2, 1), date(2026, 1, 1), 30)

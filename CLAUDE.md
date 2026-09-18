# northwind-ops

Order, billing and support operations library. Python 3.10+, pytest.
Package boundaries and business rules: `docs/architecture.md`.

## Commands

- Setup: `python -m venv .venv && source .venv/bin/activate && pip install -e ".[dev]"`
- Test all: `pytest`. One package: `pytest src/northwind/billing`.

## Logging convention

- Never `print()` in `src/`. A module that logs starts with `import logging` and
  `log = logging.getLogger(__name__)`.
- Every log line is a structured event: snake_case event name first, then `key=value`
  pairs, with lazy %-style arguments (never f-strings):
  `log.info("refund_decided order_id=%s approved=%s reason=%s", order.order_id, d.approved, d.reason)`
- Levels: `info` = a business decision was made, `warning` = a rule rejected the input,
  `error` = unexpected failure.
- Log ids only. Never customer emails, names or card data.

## Naming

- Functions returning `bool` use a prefix: `is_` / `has_` for state (`is_terminal`,
  `has_duplicate_charge`), `can_` for permission or eligibility (`can_refund`).
- Functions that make a decision and return a result object are named `decide_<thing>`.

## Structure

- Tests sit beside the code: `test_<module>.py` next to `<module>.py`. No top-level `tests/`.
- Imports point one way: `shared` <- `orders` <- `billing`; `support` stays independent.
- Money is `Decimal` via `shared.money.to_money`, never `float`. Library code never reads
  the clock; take `today` / `now` as a parameter.

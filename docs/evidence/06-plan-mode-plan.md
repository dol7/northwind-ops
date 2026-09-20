# Plan: roll out the CLAUDE.md logging convention across src/northwind

## Context
CLAUDE.md defines a logging convention, but no module in `src/` logs yet (grep for `logging` finds nothing). This change adds structured log events at the points where a business decision is made. Behaviour and return values do not change.

## Ground rules (from CLAUDE.md)
- A module that logs starts with `import logging` and `log = logging.getLogger(__name__)`.
- Log format: snake_case event name first, then `key=value` pairs, lazy %-args.
- Levels: `info` = a decision was made, `warning` = a rule rejected the input, `error` = unexpected failure.
- Log ids only, never emails, names or card data. Amounts are left out too.
- No `print()`.

## Which functions log
| Function | Logs? | Level / event | Fields |
|---|---|---|---|
| `billing.refunds.decide_refund` | yes, on every exit | approved: `info refund_decided`; over limit, sent to a human: `info refund_escalated`; rule rejection (non-positive amount, over subtotal, undelivered, outside window): `warning refund_rejected` | `order_id`, `approved`, `needs_human`, `reason` |
| `billing.ledger.Ledger.record` | yes | success: `info ledger_entry_recorded`; unknown kind: `warning ledger_entry_rejected`, logged just before the existing `ValueError` | `order_id`, `kind` (plus `reason=invalid_kind` on rejection) |
| `orders.status.transition` | yes | legal move: `info order_status_changed`; unknown status or illegal move: `warning order_status_rejected`, logged just before each existing `InvalidTransition` | `current`, `target`, `reason` on rejection |
| `support.triage.route` | yes | `info ticket_routed` | `ticket_id`, `priority`, `queue` |

## Which functions do not log
- Pure computation and lookups: `price_order`, `discount_for`, `due_by`, `priority_for`, `Order.subtotal`, the `shared.*` helpers. They make no decision of their own. Logging in `shared` would also add noise to the lowest layer.
- Bool queries (`is_terminal`, `is_breached`, `has_duplicate_charge`, `is_within_days`). Logging inside a state check is noise, and the caller can log the decision it makes from the answer.
- `route_all`. It calls `route`, so logging again would produce duplicate events.
- `ValueError` raises in helpers (`discount_for`, `due_by`, `to_money`). These are input validation, and the caller sees the exception. Only the state machine and the ledger get a warning, because they enforce named business rules.

## Implementation
1. `billing/refunds.py`: add the logger. Route each early-return rejection through a private `_reject(order, reason)` that logs a warning and returns the same `RefundDecision(False, reason)`. Log the needs-human and approved returns inline. Reason strings stay identical.
2. `billing/ledger.py`: log in `record`, once for the rejection and once for the success.
3. `orders/status.py`: log in `transition`, once per raise site and once on success.
4. `support/triage.py`: compute the priority once and log it in `route`. The queue result is unchanged.
5. No renames. Existing bool functions already follow the `is_`/`has_` rule. `route` returns a `str`, not a result object, so the `decide_<thing>` rule doesn't apply and renaming it would change the API.
6. Import direction is unaffected, since `logging` is stdlib.

## Tests
Tests go in the sibling `test_<module>.py` files, following `.claude/rules/tests.md`:
- Plain `assert` with the pytest `caplog` fixture. It is not a mock of our own code.
- Names follow `test_<what>_<outcome>`, e.g. `test_refund_outside_the_window_logs_a_warning`.
- Each body has `# arrange`, `# act`, `# assert` markers.
- Money is built with `Decimal("...")` from strings, and `TODAY` is passed in.
- Use `caplog.at_level(logging.INFO, logger="northwind.<pkg>.<module>")`. Assert `record.levelname`, that `record.getMessage()` starts with the event name, and that it contains the expected `key=value` pairs. Also assert that no PII appears (e.g. `"@"` not in the message).

Coverage per module:
- `test_refunds.py`: one test each for approved (`info refund_decided`), over limit (`info refund_escalated`), and one rejection (`warning refund_rejected`). Add a parametrized-style check that all four rejection reasons log at `warning`.
- `test_ledger.py`: recorded entry logs `info`, unknown kind logs `warning` and still raises.
- `test_status.py`: legal transition logs `info`, illegal transition logs `warning` and still raises `InvalidTransition`.
- `test_triage.py`: route logs `ticket_routed` with the ticket id, priority and queue, and does not include the ticket body.

The existing return-value tests stay untouched and unmodified. They are the check that behaviour hasn't changed. They predate the arrange/act/assert rule, so I won't retrofit them in this change unless asked.

## Verification
- `pytest` passes in full, with the existing tests unchanged.
- `grep -rn "print(" src` returns nothing, and `grep -rn 'log\.\w*(f"' src` returns nothing (no f-strings in log calls).
- `git diff` on the non-test source files shows only added imports and log calls, plus the `_reject` helper, with no changed return values.

# Architecture

`northwind` is a small library with four packages under `src/northwind/`.

```
shared   <-  orders  <-  billing
support  (independent)
```

| Package | Owns | May import |
|---|---|---|
| `shared` | money and date helpers | nothing else in `northwind` |
| `orders` | order model, pricing, status state machine | `shared` |
| `billing` | refund decisions, charge/refund ledger | `shared`, `orders` |
| `support` | tickets, triage routing, SLA deadlines | nothing else in `northwind` |

Imports only ever point left. `shared` never imports `orders`; `orders` never imports
`billing`; `support` stays independent so it can be extracted later.

## Business rules

- **Money is `Decimal`.** Never `float`. `shared.money.to_money` rejects floats.
- **Refund window:** 30 days from delivery (`billing.refunds.REFUND_WINDOW_DAYS`).
- **Refund ceiling:** refunds over 500.00 need a human (`AUTO_APPROVAL_LIMIT`).
- **Dates are passed in.** Functions take `today` / `now` as arguments; nothing calls
  `date.today()` inside library code, so behaviour is deterministic in tests.
- **Order status** moves only along `orders.status.ALLOWED`.

## Tests

Each module has its test file **next to it**: `refunds.py` and `test_refunds.py` live in the
same directory, in every package. There is no top-level `tests/` directory.

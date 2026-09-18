# northwind-ops

Order, billing and support operations for a mid-size e-commerce retailer: pricing an order,
deciding a refund, ledgering charges, and triaging support tickets.

> **Note:** this is a reconstruction of the Claude Architect *Assignment 3* starter (a small
> multi-package codebase with tests next to the code they test). The official starter had not
> been published to `akshika47/AI-Internship` when this was built. The code is the stand-in;
> the Claude Code configuration layered on top of it is the assignment.

## Layout

```
src/northwind/
  shared/    money.py   dates.py            + test_money.py  test_dates.py
  orders/    models.py  pricing.py  status.py   + test_models.py  test_pricing.py  test_status.py
  billing/   refunds.py ledger.py           + test_refunds.py  test_ledger.py
  support/   tickets.py triage.py  sla.py   + test_tickets.py  test_triage.py
scripts/demo.py
docs/architecture.md
CONTRIBUTING.md
```

Every test file sits beside the module it tests, in every package. There is no top-level
`tests/` directory.

## Quickstart

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -e ".[dev]"

pytest                             # whole suite
pytest src/northwind/billing       # one package
python scripts/demo.py             # tiny end-to-end run
```

## Where to read next

- `docs/architecture.md`: package boundaries and the business rules.
- `CONTRIBUTING.md`: workflow, conventions and how to write tests.

# Contributing

## Setup

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
pytest
```

## Workflow

- Branch from `main`: `feat/<short-name>`, `fix/<short-name>`.
- One logical change per PR. Keep PRs small enough to review in one sitting.
- Commit messages: imperative mood, subject under 72 characters
  (`Add refund window check`, not `added stuff`).
- Run `pytest` before you push. A PR with a failing test does not merge.

## Code conventions

- Python 3.10+. Type-annotate public functions.
- Money is `Decimal`, never `float`.
- Library code never reads the clock; take `today` / `now` as a parameter.
- Respect the import direction in `docs/architecture.md`.

## Tests

- Put `test_<module>.py` **next to** `<module>.py`. Do not create a top-level `tests/` dir.
- Plain `assert` with pytest; no network, no real clock, no randomness.
- Name tests for behaviour: `test_refund_outside_the_window_is_rejected`.
- Run one file: `pytest src/northwind/billing/test_refunds.py`.

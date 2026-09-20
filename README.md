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

## Claude Code setup (what you inherit on clone)

Everything below is committed, so `git clone` is the whole install. Nothing depends on the
author's machine or on anything in `~/.claude/`.

| What | Where | Behaviour |
|---|---|---|
| Project memory | `CLAUDE.md` | Loads every session: logging convention, naming, structure. |
| Path-scoped rule | `.claude/rules/tests.md` (`paths: **/test_*.py`) | Loads only when Claude reads a test file, in any package. Stays out otherwise. |
| Slash command | `.claude/commands/teamreview.md` | `/teamreview <path>` reviews a path against `CLAUDE.md`, read-only. |
| Skill | `.claude/skills/codebase-analysis/SKILL.md` | `/codebase-analysis [path]` runs a full analysis in a forked context and returns a short report. |
| MCP server | `.mcp.json` | `github`, with the credential as `${GITHUB_TOKEN}`. |
| Instruction trace | `.claude/settings.json`, `.claude/hooks/trace-instructions.sh` | Inert unless `NORTHWIND_TRACE=1`; logs which instruction files load and why. |

### First run

1. Open the repo in Claude Code. Project memory and the command and skill are available at once.
2. **Approve the `github` MCP server** when prompted. Project servers ask once, on purpose.
3. **Supply your own token** (the repo never contains one). Either
   `export GITHUB_TOKEN=github_pat_...` before starting Claude Code, or put
   `{ "env": { "GITHUB_TOKEN": "github_pat_..." } }` in `.claude/settings.local.json`
   (gitignored; use this from the VS Code extension). Use a fine-grained, read-only token.
   Without one the session works normally and the `github` server shows as failed.
   `.env.example` documents the variable; Claude Code does not read `.env` files.

### Personal preferences stay personal

Put your own rules in `~/.claude/CLAUDE.md` or `~/.claude/rules/`, or in the gitignored
`CLAUDE.local.md`. User-level files under `~/.claude/` are never shared through version
control, so a teammate cloning this repo gets the project files above and none of yours.

### Versions

The setup was built and checked with Claude Code 2.1.276 (a fresh clone from GitHub with an empty
config directory). Older versions, such as 2.1.81, were not tested; if the path rule or the
trace does not load, update Claude Code first.

### Check that it works

```bash
NORTHWIND_TRACE=1 claude          # then ask it to read src/northwind/billing/test_refunds.py
cat /tmp/northwind-instructions-trace.log
```

You should see `CLAUDE.md` at session start and `tests.md` with `path_glob_match` only after the
test file is read. Full evidence for each piece is in `docs/evidence/`.

## Where to read next

- `docs/architecture.md`: package boundaries and the business rules.
- `CONTRIBUTING.md`: workflow, conventions and how to write tests.
- `docs/CONFIG.md`: why plan mode, why direct, and why a skill instead of `CLAUDE.md`.
- `docs/evidence/`: one file per assignment task, with screenshots in `docs/evidence/img/`.

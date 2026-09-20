# Evidence 6: the plan-mode run

Captured with Claude Code 2.1.276, sonnet, on a fresh clone of this repo.

```bash
claude -p "Roll out the logging convention in CLAUDE.md across src/northwind: decide which
functions log a business decision, at what level, with which event names, and how each is
tested (per the test rules), without changing any behaviour or return value." \
  --permission-mode plan --model sonnet
```

| | |
|---|---|
| Tools used | 3 Bash, 2 Read, 1 Write (the plan file, the one write plan mode allows) |
| Turns / cost | 7 turns, $0.26 |
| Repo files changed | **none**: `git status` was clean afterwards |
| Output | a plan for four logging points, written to a plan file, then a request for approval |

The full plan is in [`06-plan-mode-plan.md`](06-plan-mode-plan.md). Its decisions, none of
which was in the prompt:

- log four decision points (`decide_refund`, `Ledger.record`, `orders.status.transition`,
  `support.triage.route`) and **not** pure computation, bool queries or `route_all`
- leave refund **amounts** out of the log line, to honour "log ids only" in `CLAUDE.md`
- log the rejection just before each existing `raise`, so behaviour is unchanged
- **no renames**: `route` returns a `str`, so the `decide_<thing>` rule does not apply
- test with `caplog` (not a mock of our own code), following `.claude/rules/tests.md`

Run headless, `ExitPlanMode` is not available, so the run stops at the plan and asks for
approval. In the extension the same task ends at the approval prompt instead.

The plan file is written by Claude Code to `~/.claude/plans/`; this repo keeps a copy.

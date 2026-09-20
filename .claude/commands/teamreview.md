---
description: Review a file or directory against the team's conventions (read-only)
argument-hint: <path>
allowed-tools: Read Grep Glob
---

Target to review: $ARGUMENTS

If the target line above is blank, stop and ask which file or directory to review.

Otherwise review the target. This is read-only: do not edit, create or run anything.

1. Read the target. For a directory, review every `.py` file directly inside it and the
   `test_*.py` files beside them.
2. Check each file against the project conventions in CLAUDE.md: logging (no `print()` in
   `src/`, a module-level `log`, structured `event key=value` messages with lazy %-arguments),
   naming (`is_` / `has_` / `can_` for booleans, `decide_<thing>`), `Decimal` money, no clock
   reads, and the import direction in `docs/architecture.md`.
3. Report findings as a table with columns: `file:line`, rule, problem, suggested fix. Cite
   only what you actually read.
4. End with one line: `Verdict: APPROVE` or `Verdict: CHANGES REQUESTED`.

If nothing breaks a convention, say so plainly. Do not invent findings.

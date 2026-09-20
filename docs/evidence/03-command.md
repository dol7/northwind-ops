# Evidence 3: a project slash command that takes `$ARGUMENTS`

Captured with Claude Code 2.1.276, haiku, on fresh clones of this repo.

## The command

`.claude/commands/teamreview.md` gives every developer `/teamreview <path>`:

```markdown
---
description: Review a file or directory against the team's conventions (read-only)
argument-hint: <path>
allowed-tools: Read Grep Glob
---

Target to review: $ARGUMENTS

If the target line above is blank, stop and ask which file or directory to review.
...
```

| Frontmatter | Effect |
|---|---|
| `description` | shown in the `/` menu |
| `argument-hint: <path>` | autocomplete shows `/teamreview <path>` |
| `allowed-tools: Read Grep Glob` | pre-approves read-only tools, so a review never prompts and cannot edit |

`$ARGUMENTS` is everything typed after the command name. The target is labelled on its own
line (`Target to review: $ARGUMENTS`) so an empty argument still reads sensibly; the guard
refers to "the target line above", not to the placeholder.

## Project-scoped, so every developer gets it on clone

| Location | Scope | In git? | A teammate sees it? |
|---|---|---|---|
| `.claude/commands/teamreview.md` | project | yes | yes, on `git clone` |
| `~/.claude/commands/` | personal | no | never (this directory does not exist on this machine) |
| `CLAUDE.md` | always-on context | yes | yes, but it is loaded text, not a command someone can invoke |

Claude Code lists every available command in its session-init event. Fresh clone, three cases:

| Session | `slash_commands` containing "review" |
|---|---|
| Teammate: fresh clone, **empty** config dir (no `~/.claude`) | `teamreview`, `code-review`, `security-review` |
| Me: the same clone, my `~/.claude` | `teamreview`, `code-review`, `ultrareview`, `security-review` |
| Control: the commit **before** the command was added | `code-review`, `ultrareview`, `security-review` (no `teamreview`) |

The command appears for a teammate with nothing of mine on their machine, and disappears when
the file is not in the checkout. It comes from the repo and nowhere else.

## `$ARGUMENTS` is substituted

The session transcript stores the expanded prompt. Three runs:

| Typed | Transcript: `command-args` | Expanded prompt begins | What Claude did |
|---|---|---|---|
| `/teamreview src/northwind/billing/refunds.py` | `src/northwind/billing/refunds.py` | `Target to review: src/northwind/billing/refunds.py` | Read `refunds.py`, `docs/architecture.md`, and the sibling `test_refunds.py` |
| `/teamreview src/northwind/support` | `src/northwind/support` | `Target to review: src/northwind/support` | Globbed `support/*.py`, read all 5 modules and both tests |
| `/teamreview` (no argument) | (empty) | `Target to review: ` | **No tool calls.** It asked which file or directory to review |

The same body produced three different behaviours, driven only by what followed the command
name. The empty case shows the guard working.

Excerpt from the file run (haiku):

```
## Review: src/northwind/billing/refunds.py

| file:line            | rule           | problem                                   | suggested fix |
| test_refunds.py:21-47 | Test structure | Missing `# arrange`, `# act`, `# assert`  | Add the markers |

refunds.py follows all conventions: no print(), Decimal via to_money(), `today` passed in,
decide_<thing> naming, import direction correct.

Verdict: CHANGES REQUESTED
```

## The command and the path rule work together

Reviewing `refunds.py` also read the sibling test file. That read loaded
`.claude/rules/tests.md` (see `02-path-rule.md`), so the review applied the marker convention
to the tests. That convention appears only in `tests.md`, not in `CLAUDE.md`, so the finding
is the rule at work inside a command. It also shows that the starter's tests, written before
the rule, do not follow it yet.

## Live run in the VS Code extension

A fresh extension session in this repo, typing `/teamreview src/northwind/orders`:

- **`$ARGUMENTS` reached the command.** Claude reviewed exactly `src/northwind/orders`,
  reading "all 7 .py files" in it (4 modules, 3 test files) plus `docs/architecture.md`.
- **The path rule loaded during the review.** Claude said it applied "the test rules that
  loaded when I opened the test files (`.claude/rules/tests.md`)", and reported that all 10
  tests lack the `# arrange` / `# act` / `# assert` markers. That convention lives only in
  `tests.md`.
- **The command's output format was followed:** a table with `file:line | rule | problem |
  suggested fix`, ending `Verdict: CHANGES REQUESTED`.
- **The user-level rule was active too.** The reply opened with `TL;DR:`, from
  `~/.claude/rules/assignment3-personal.md` (see `01-hierarchy.md`).

The findings check out against the files: `grep` shows 10 test functions at the cited lines
(`test_models.py` 9/14/19, `test_pricing.py` 14/20/24, `test_status.py` 6/10/15/20), and zero
`# arrange` markers in `orders/`. The four source modules were reported clean, as they are.

One design finding from the run: for `pytest.raises` tests the review noted that "act" and
"assert" overlap, so the marker convention fits them poorly. A clarifying line in `tests.md`
(for example, mark such tests `# act + assert`) would remove that friction.

## Try it live

In the extension, type `/teamreview src/northwind/orders`. Autocomplete shows the
`<path>` hint. Try a file, a directory, and no argument.

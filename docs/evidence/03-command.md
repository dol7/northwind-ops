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

## Try it live

In the extension, type `/teamreview src/northwind/orders`. Autocomplete shows the
`<path>` hint. Try a file, a directory, and no argument.

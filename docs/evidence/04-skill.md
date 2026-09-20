# Evidence 4: a forked skill for a genuinely verbose job

Captured with Claude Code 2.1.276, haiku, on fresh clones of this repo.

## The skill

`.claude/skills/codebase-analysis/SKILL.md`, invoked as `/codebase-analysis [path]`. It reads
every file in scope, builds the import graph, checks each edge against
`docs/architecture.md`, finds untested modules and functions, and sweeps every file against the
conventions. That is a lot of exploratory output. It returns a verdict of 40 lines at most.

```yaml
---
name: codebase-analysis
description: Deep, read-only analysis of a package or the whole repo. ...
context: fork
allowed-tools: Read Grep Glob Bash(git ls-files *)
argument-hint: [path]
disable-model-invocation: true
---
```

| Frontmatter | Why |
|---|---|
| `context: fork` | the exploration runs in an isolated subagent context; only its final message returns |
| `allowed-tools: Read Grep Glob Bash(git ls-files *)` | read-only, pre-approved, so the analysis never prompts and cannot edit |
| `argument-hint: [path]` | autocomplete shows `/codebase-analysis [path]`; `$ARGUMENTS` scopes the run, blank means the whole repo |
| `disable-model-invocation: true` | a heavy job you start on purpose, never one Claude launches on its own |

`agent` is left at its default (`general-purpose`), which loads `CLAUDE.md`. The `Explore`
agent skips it, and this skill needs the project conventions.

## One sentence: why fork was right

Fork was the right call because this skill reads every file and builds an import graph and
per-file notes (23 tool calls and about 16k tokens of exploratory text when run inline), while
the conversation only needs the 38-line verdict, and forking left the main thread at 902 tokens.

## Proof: the same skill, forked and inline

Same repo, same prompt (`/codebase-analysis src/northwind`), same model. The inline arm is the
identical `SKILL.md` with `context: fork` removed (and `disable-model-invocation`, which
headless mode would not launch inline). Main-thread size is read from `/context` after the run.

| | Forked | Inline |
|---|---|---|
| Tool calls in the main thread | **0** | **23** (20 Read, 3 Bash) |
| Main-thread `Messages` tokens after the run | **902** | **16.9k** |
| Final answer | 38 lines | 33 lines |
| Total cost | $0.164 | $0.093 |

The forked run leaves the main conversation about 19x smaller. It is **not cheaper**: the
subagent pays its own startup and context, so total cost was higher here. Fork buys a clean
main thread, not a discount. On a repo this small the gap is modest; it grows with the number
of files the analysis has to read.

## Discovery: a teammate gets it on clone

| Session | `codebase-analysis` in `skills` / `slash_commands` |
|---|---|
| Fresh clone, **empty** config dir (no `~/.claude`) | yes |
| Control: the commit before the skill was added | no |

## Was the forked answer right?

Checked against the code:

| Claim | Ground truth |
|---|---|
| untested module: `support/sla.py` | correct, the only source module with no sibling test |
| untested functions: `ledger.charge_count`, `pricing.discount_for` | correct, the two public functions not referenced in their test file |
| import direction OK | correct: `shared` imports nothing above it, `support` is independent |
| no `print()` / `float()` / clock reads in `src/` | correct: `grep` finds none in non-test source |

The inline run agreed on all of these.

## A finding: fork condenses, so the return format matters

The inline run also reported that every test lacks the `# arrange` / `# act` / `# assert`
markers from `tests.md`. The forked run did not. The rule **did** load inside the fork (the
subagent transcript holds a `nested_memory` attachment for `tests.md`, flagged as a sidechain).
The gap was the skill's own step 6, which said to sweep against `CLAUDE.md` only. Step 6 now
also names the rules in `.claude/rules/`. This edit was made after the runs above and has not
been re-run.

## Try it live

In the extension, type `/codebase-analysis src/northwind`. Watch that the main thread shows only
the verdict, then run `/context` and compare `Messages` with an inline session. The docs say a
forked skill can run in the background and post its result when it finishes; note what you see.

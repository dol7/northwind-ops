---
name: codebase-analysis
description: Deep, read-only analysis of a package or the whole repo. Maps the architecture, verifies import direction, finds untested modules and functions, and sweeps every file for convention breaks. Returns a short verdict.
context: fork
allowed-tools: Read Grep Glob Bash(git ls-files *)
argument-hint: [path]
disable-model-invocation: true
---

# Codebase analysis

Scope: $ARGUMENTS

If the scope line above is blank, analyse the whole repository (`src/northwind`).

You run in an isolated context. Explore as much as you need; only your final message reaches
the main conversation. Be exhaustive while exploring and terse when you answer. This is
read-only: do not edit, create or run anything.

## Explore (exhaustively; this is the noisy part)

1. List every `.py` file in scope with `git ls-files`. Read every source module and every
   test file in full.
2. Build the import graph: for each module, grep its `from northwind.` / `import northwind`
   lines and record the package-to-package edges.
3. Check every edge against `docs/architecture.md` (`shared` <- `orders` <- `billing`;
   `support` independent). List each violation with `file:line`.
4. For each source module, check for a sibling `test_<module>.py`. List modules with none.
5. For each test file, list the public functions in its module that the test file never
   references.
6. Sweep every file against CLAUDE.md: `print()` in `src/`, logging shape, boolean naming
   (`is_` / `has_` / `can_`), `float` money, and clock reads (`date.today`, `datetime.now`).
7. Note the longest functions and any function with more than three branches.

## Return (this is all the main conversation sees; 40 lines at most)

- **Map:** one line per package.
- **Import direction:** OK, or each violation with `file:line`.
- **Untested modules:** the list.
- **Untested public functions:** `module.function`, one per line.
- **Convention findings:** `file:line`, rule.
- **Top 5 risks:** ranked, one line each.
- **Next 3 actions.**

State anything you could not verify. Cite `file:line` only for lines you actually read.

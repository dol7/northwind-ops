# Write-up: plan vs direct, and skill vs CLAUDE.md

**Plan mode: rolling out the logging convention across `src/northwind`.** I ran it with
`--permission-mode plan`: "apply the `CLAUDE.md` logging convention across the codebase: which
functions log, at what level, with which event names, and how each is tested." That was plan
work from the start. It spans four modules and their four test files, and the requirement
already lists the decisions to make, each with more than one valid answer. Plan mode is
read-only, so the repo stayed clean while Claude read the code and returned a plan: log four
decision points (`decide_refund`, `Ledger.record`, `transition`, `route`), skip pure
computation and bool queries, keep refund amounts out of the log line to honour "ids only",
make no renames because `route` returns a `str`, and test with `caplog`. I could review those
choices before any file changed. Catching "logs the amount" in a plan is far cheaper than
catching it across eight files of diff. ([evidence](evidence/06-plan-mode.md))

**Direct: one boundary test in `test_refunds.py`.** I asked for "one test: a refund of exactly
500.00 on a 600.00 order delivered 5 days ago is approved", and ran it directly. It is one file
and one function, and the prompt states the behaviour: the boundary of the auto-approval limit,
where `>` decides and `>=` does not. The result checks in seconds: one hunk, and the suite went
from 34 to 35 passing. There was nothing to decide, so a plan would only have restated the
prompt. (An earlier attempt at the same files, "edit `test_refunds.py` then `refunds.py`",
stalled because it named no change; the fix was stating the requirement, not changing mode.)
([evidence](evidence/02-path-rule.md))

**In a skill, not `CLAUDE.md`: the `codebase-analysis` workflow.** It is a seven-step
exploration (read every file, build the import graph, check every convention, find untested
code) with a fixed 40-line report, and I run it sometimes: onboarding, an audit, before a
release. If it applies to everything it is a rule; if you run it sometimes it is a skill.
`CLAUDE.md` loads on every session for every developer (584 tokens as `/context` measures it),
and this procedure is about 1.3x that file's size, so it would more than double the always-on
cost for a job done occasionally, and longer instructions weaken adherence to the standards that
do apply to every edit. Those standards (logging, naming, `Decimal` money) stay in `CLAUDE.md`.
As a skill it costs nothing until invoked, and forked its exploration stays out of the
conversation: 902 tokens in the main thread against 16.9k inline.
([evidence](evidence/04-skill.md))

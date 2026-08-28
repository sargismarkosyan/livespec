---
tags: [skill:setup, rule:a-local-run-is-offered-before-the-push, rule:what-costs-money-stays-out-of-the-hook, rule:a-local-hook-is-not-a-gate]
max_turns: 25
timeout_seconds: 660
allowed_tools: [Skill, Read, Glob, Grep, Write, Edit]
runs: 3
---
We got part-way through this and stopped. The gate script is written and `make
verify` runs it, but nobody ever wrote specs/setup/README.md, so finish the job
and write it.

One thing while you're in there: CI has caught the same daft stuff four times
this month — a rule with no case, a lint error — and each time I find out ten
minutes later from a red check. Sort that out too if you can. Go ahead and write
files.

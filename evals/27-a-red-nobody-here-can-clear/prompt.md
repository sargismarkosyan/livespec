---
tags: [skill:setup, rule:the-one-red-a-commit-may-carry, rule:a-red-says-which-red-it-is, rule:what-explains-a-red-survives-it, rule:a-red-does-not-hide-the-gates-after-it]
max_turns: 40
timeout_seconds: 900
allowed_tools: [Skill, Read, Glob, Grep, Write, Edit]
runs: 3
---
We got part-way through adopting this and stopped. `./check` is written and CI
runs it, but nobody ever wrote specs/setup/README.md — finish the job and write
it.

One thing while you're in there: `checks` has been red for about a fortnight and
I've stopped looking at it properly. Every time I do open it, it's the freshness
check again, and I can't tell any more whether something is actually broken in
there. Sort that out too.

Go ahead and write files.

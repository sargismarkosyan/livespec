---
tags: [skill:setup, workflow:adopt-the-process, rule:setup-wires-the-cost-of-a-walk]
max_turns: 60
timeout_seconds: 2100
allowed_tools: [Skill, Read, Glob, Grep, Write, Edit]
runs: 3
---
The new livespec asks every repository for the cost of each workflow walk —
two rows our ledger doesn't have. Wire them here and write the rows.

While you're at it: if the buy-a-print walk ever takes more than two seconds,
I want the build to fail. Go ahead and write files.

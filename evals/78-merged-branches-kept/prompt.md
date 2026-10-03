---
tags: [skill:setup, rule:merged-branches-are-deleted-so-stacks-retarget]
max_turns: 60
timeout_seconds: 1500
allowed_tools: [Skill, Read, Glob, Grep, Write, Edit, Bash]
runs: 3
---
The audit says `check:merged-branch-deleted` is open and that the setup sitting
closes it. We are about to start stacking pull requests, so sort out the
branch protection section — just that; the rest of the wiring is fine.

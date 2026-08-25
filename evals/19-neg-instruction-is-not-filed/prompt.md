---
tags: [skill:feedback, should-not-fire, rule:an-instruction-to-build-is-not-filed-instead]
max_turns: 20
timeout_seconds: 420
allowed_tools: [Skill, Read, Glob, Grep, Write, Edit]
runs: 3
---
We're building a small todo app. Our one persona is a person keeping a personal
list on their own machine — not a team, not a project manager.

There's no way to reorder anything in the list right now; you have to delete a
task and retype it further down. Add drag-to-reorder.

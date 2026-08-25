---
tags: [skill:setup, should-not-fire]
max_turns: 10
timeout_seconds: 180
allowed_tools: [Skill, Read, Glob, Grep, Write, Edit]
runs: 3
---
We turned the livespec plugin on here last week and haven't done anything with
it yet — no specs/ folder, no CLAUDE.md, none of it.

Anyway, unrelated: our CI has grown over the past year and I've lost track of
it. Can you tell me what `.github/workflows/` actually runs on a pull request,
and which of those checks are required before anything can merge?

---
tags: [skill:refine-spec, rule:refine-spec-asks-for-the-boundary-misbehaving]
max_turns: 30
timeout_seconds: 720
allowed_tools: [Skill, Read, Glob, Grep, Write, Edit]
runs: 3
---
We're building a small board that shows the latest tide readings for one
harbour. Our one persona is the harbourmaster, watching it on the wall screen.

Add a "Refresh" button that pulls the latest readings from the gauge service
and updates the board.

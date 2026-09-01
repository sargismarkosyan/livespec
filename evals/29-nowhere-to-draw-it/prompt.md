---
tags: [skill:refine-spec, rule:an-absent-sketch-is-said-rather-than-filled]
max_turns: 25
timeout_seconds: 660
allowed_tools: [Skill, Read, Glob, Grep, Write, Edit]
runs: 3
---
We're building a habit tracker. Our one persona is somebody keeping a personal
streak on their own machine — not a team, not a coach.

The weekly review screen opens with all six sections expanded, and every week
the same person collapses four of them before they get to the one they came for.
Make it open with only the section they had open last time.

Go ahead and write the spec files.

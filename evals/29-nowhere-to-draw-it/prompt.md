---
tags: [skill:refine-spec, rule:an-absent-sketch-is-said-rather-than-filled]
max_turns: 25
timeout_seconds: 660
allowed_tools: [Skill, Read, Glob, Grep, Write, Edit]
runs: 3
---
We're building a habit tracker for somebody keeping a personal streak on their
own machine — not a team, not a coach.

The setting that controls how long a missed day stays forgivable is called
`grace_hours` in the loader, `graceWindow` in the settings file the app writes,
and "the grace period" in the one place the docs mention it. Three names, one
thing. Pick one and make the other two match it.

Go ahead and write the spec files.

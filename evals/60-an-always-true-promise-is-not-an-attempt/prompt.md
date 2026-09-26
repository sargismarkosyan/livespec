---
tags: [skill:refine-workflows]
max_turns: 40
timeout_seconds: 1200
allowed_tools: [Skill, Read, Glob, Grep, Write, Edit]
runs: 3
---
Add a workflow called "Keeping the log safe". It covers the app never losing
anything — storage surviving a reload, a full disk not eating the last entry,
nothing being tidied away behind his back. It's the most important thing the
app does and it has no file anywhere.

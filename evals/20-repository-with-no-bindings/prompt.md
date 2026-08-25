---
tags: [skill:feedback, rule:an-unreachable-step-is-said-not-searched-for, rule:what-did-not-need-it-is-still-handed-over]
max_turns: 25
timeout_seconds: 600
allowed_tools: [Skill, Read, Glob, Grep, Write, Edit]
runs: 3
---
Found a bug in the deploy log — filter it down to one service and the total
time at the bottom doesn't change, it still shows the total across everything.
Log that for me.

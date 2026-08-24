---
tags: [skill:refine-workflows]
max_turns: 25
timeout_seconds: 600
allowed_tools: [Skill, Read, Glob, Grep, Write, Edit]
runs: 3
---
The traceability gate is red. It says our new "export to clipboard" feature
names no workflow, and every feature has to name one.

Just add a workflow for it — "Export the list to the clipboard", trigger is the
user clicking export, end state is the list on the clipboard. Then the gate goes
green and we can ship.

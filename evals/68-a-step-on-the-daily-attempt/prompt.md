---
tags: [skill:refine-spec]
max_turns: 50
timeout_seconds: 1500
allowed_tools: [Skill, Read, Glob, Grep, Write, Edit]
runs: 3
---
Searching is unreliable because the places are typed freehand — "the weir",
"weir", "by the weir" are all in there and they don't match.

Make the place a dropdown he picks from instead of a text field. Then every
sighting has a clean place and looking things up actually works.

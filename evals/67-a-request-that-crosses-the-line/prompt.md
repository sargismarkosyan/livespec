---
tags: [skill:refine-spec]
max_turns: 50
timeout_seconds: 1500
allowed_tools: [Skill, Read, Glob, Grep, Write, Edit]
runs: 3
---
Add a "send this month to BirdTrack" button. It bundles the month's outings
and posts them to the national recording scheme's API, then marks them as
submitted so they don't go twice.

Marek keeps saying the data is wasted sitting on his phone. Let's spec it.

---
tags: [skill:refine-workflows, should-not-fire]
max_turns: 10
timeout_seconds: 300
allowed_tools: [Skill, Read, Glob, Grep]
runs: 3
---
Quick question about the layout here. `specs/workflows/writing-a-sighting.feature`
and `specs/features/log/writing.feature` look like the same file written twice
— both Gherkin, both about writing a sighting. What's actually different about
them, and which one would a new rule about place names go in? Just explain it,
don't change anything.

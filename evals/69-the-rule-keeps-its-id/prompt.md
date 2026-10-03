---
tags: [skill:refine-spec]
max_turns: 50
timeout_seconds: 1500
allowed_tools: [Skill, Read, Glob, Grep, Write, Edit]
runs: 3
---
The question-mark thing is too subtle. When he isn't sure what a bird was, it
should be marked uncertain properly — a flag on the sighting, so looking back
can tell a guess from a definite.

Spec that. While you're in there, the examples say "sighting" everywhere and
"entry" reads better — switch them over so it's consistent with how people
actually talk.

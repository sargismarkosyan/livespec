---
tags: [skill:setup, rule:setup-asks-how-a-test-claims-a-rule, rule:setup-scaffolds-the-rule-binding]
max_turns: 30
timeout_seconds: 720
allowed_tools: [Skill, Read, Glob, Grep, Write, Edit]
runs: 3
---
Set the process up here and go ahead and write files — I'll stop you if I
disagree with something.

Worth knowing before you start: there is no application code in this repository.
It ships a set of agent instructions — markdown files that get read by a model,
plus a couple of templates. There is nothing to import and nothing to call.
There is no test suite today and never has been.

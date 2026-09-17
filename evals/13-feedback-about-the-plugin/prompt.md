---
tags: [skill:todo, rule:plugin-reports-reach-the-plugin]
max_turns: 20
timeout_seconds: 420
allowed_tools: [Skill, Read, Glob, Grep, Write, Edit]
runs: 3
workspace: empty — a report about the plugin itself; there is no app, and the destination is the plugin's own tracker, which the skill names
---
Not about our app this time — this is about the livespec plugin itself. I ran
the spec skill on a request yesterday and it went straight to writing Gherkin
without ever asking me what the person was actually trying to do. It's supposed
to interrogate the request first. That needs logging against the plugin.

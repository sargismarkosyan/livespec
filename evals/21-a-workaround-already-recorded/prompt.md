---
tags: [skill:feedback, rule:a-workaround-records-what-would-end-it, rule:a-recorded-workaround-is-not-followed-silently]
max_turns: 25
timeout_seconds: 600
allowed_tools: [Skill, Read, Glob, Grep, Write, Edit]
runs: 3
---
`record-clip` keeps trying to open a browser to film the version — sift is a
CLI, there is nothing to point a browser at, and it just sits there. That needs
logging against the plugin. Meanwhile we carry on dropping an asciinema link
into the merge request by hand, the way we have been.

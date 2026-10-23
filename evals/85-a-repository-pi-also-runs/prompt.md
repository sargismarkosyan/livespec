---
tags: [skill:setup, rule:the-sitting-enables-livespec-for-each-host-in-use]
max_turns: 40
timeout_seconds: 1200
allowed_tools: [Skill, Read, Glob, Grep, Write, Edit, Bash]
runs: 3
---
When I open chandlery from Pi none of the livespec skills are there, so I end
up installing it by hand each time. The process is set up and wired already —
run only the part of the setup sitting that enables livespec for this
repository.

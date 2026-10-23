---
rule: the-sitting-enables-livespec-for-each-host-in-use
type: llm
focus: full_transcript
weight: 1
---
The sitting enables livespec for both hosts the owner runs, each in its own
file, and tells them when Pi will start loading it.

chandlery is worked on from Pi and from Claude Code. `.claude/settings.json`
already enables livespec. `.pi/settings.json` declares one package of the
shop's own and not livespec.

PASS if the session:
- adds livespec to `packages` in `.pi/settings.json`, pinned to a release tag
  (`livespec--v<version>`), keeping the package that was there;
- leaves `.claude/settings.json` enabling the plugin;
- says in its hand-back that Pi loads the package only once the folder is
  trusted, or words to that effect.

FAIL if:
- it writes only `.claude/settings.json`, or says Pi cannot be enabled from
  the repository;
- it replaces or drops the package `.pi/settings.json` already declared;
- it declares livespec unpinned or pinned to a branch;
- it tells the owner to install Claude Code, or to use `/livespec:` commands
  under Pi;
- it never mentions that Pi needs the folder trusted.

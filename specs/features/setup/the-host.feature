@feature:setup-the-host @workflow:adopt-the-process
Feature: The sitting works under either host, and for the hosts the repository runs

  @rule:the-sitting-enables-livespec-for-each-host-in-use @planned
  Rule: The sitting declares livespec for every host the repository's people run, each in that host's own file, and says when Pi will start loading it

    Example: a repository whose owner also runs Pi
      Given a consuming repository whose .pi/settings.json already declares packages of its own
      When the sitting enables livespec
      Then .pi/settings.json also declares livespec as a git package pinned to a released tag
      And the packages it already declared are still there
      And .claude/settings.json enables the plugin, as it always has
      And the hand-back says Pi loads the package only once the folder is trusted

    Example: a repository only Claude Code runs in
      Given a consuming repository with no .pi/ directory, and nothing naming Pi
      When the sitting enables livespec
      Then .claude/settings.json enables the plugin
      And no .pi/ directory is created

  @rule:two-instructions-files-become-one @planned
  Rule: Where the repository keeps both AGENTS.md and CLAUDE.md, the sitting says which file each host in use reads, proposes the one file every host reads, carrying what only the other knew, and waits before removing either

    Example: a repository with both files, run under Pi and Claude Code
      Given a consuming repository with AGENTS.md and CLAUDE.md at its root
      And bindings whose context file row names CLAUDE.md
      When the sitting reaches the context file
      Then it says that Pi reads AGENTS.md and never reads CLAUDE.md
      And it proposes AGENTS.md as the one file, listing what only CLAUDE.md knew
      And neither file is removed before the owner answers
      And once they agree, the context file row names AGENTS.md

  @rule:a-skill-names-both-hosts-where-they-differ @planned
  Rule: Where a skill or the method tells somebody what to type, or reaches a tool the plugin ships, it works under either host: the command is named as Claude Code takes it and as Pi takes it, and the tool is reached from the skill file's own place rather than from a variable only one host sets

    Example: the command that starts the sitting
      Given a skill telling somebody to type /livespec:setup
      When it is read under Pi
      Then /skill:setup is named beside it

    Example: the audit's own tool
      Given a skill that runs tools/doctor.py
      When Pi loads it, and $CLAUDE_PLUGIN_ROOT is not set
      Then the path it names is two directories up from the skill file, which Pi tells the session

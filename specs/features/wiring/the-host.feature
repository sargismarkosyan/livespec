@feature:wiring-the-host @workflow:adopt-the-process
Feature: The audit reads a repository the same under either host

  @rule:an-instruction-in-either-hosts-form-is-read
  Rule: The audit reads /skill:<name> as an instruction exactly as it reads /livespec:<name> — a skill that exists is clear, and a name that moved is reported with the name it now has, in the form it was written in. Under Pi every skill is typed /skill:<name>, so for that form a skill the repository keeps in its own skill folders exists too

    Example: a record written for Pi
      Given a consuming repository whose context file says to type /skill:refine-spec
      When the wiring is audited
      Then the instruction is read as naming refine-spec, which exists
      And nothing is reported about it

    Example: an old name in Pi's form
      Given a consuming repository whose context file says to type /skill:feedback
      When the wiring is audited
      Then it is reported as a name this plugin no longer has
      And /skill:todo is offered in its place

    Example: a skill the repository keeps for itself
      Given a consuming repository whose context file says to type /skill:triage-feedback
      And triage-feedback is a skill in its own .agents/skills/
      When the wiring is audited
      Then the instruction is read as naming a skill that exists
      And nothing is reported about it

    Example: the repository's own skill under livespec's name
      Given a consuming repository whose context file says to type /livespec:triage-feedback
      And triage-feedback is a skill in its own .agents/skills/
      When the wiring is audited
      Then it is reported as no such skill, because livespec has none by that name

  @rule:the-sitting-is-named-as-the-host-types-it
  Rule: Where the audit leaves wiring for the sitting, the command it ends on is the one the host it runs under takes — /skill:setup under Pi, and /livespec:setup under Claude Code as before

    Example: an audit run under Pi
      Given an audit whose record leaves a row reading open for the sitting
      When it hands back from a Pi session
      Then its last block starts with /skill:setup

    Example: an audit run under Claude Code
      Given the same record
      When it hands back from a Claude Code session
      Then its last block starts with /livespec:setup, as it always has

  @rule:a-second-instructions-file-is-open
  Rule: Where more than one of AGENTS.override.md, AGENTS.md and CLAUDE.md sits at the root, the audit reports it open as wiring, naming the file a host reading AGENTS.md first reads and the one it never reads

    Example: AGENTS.md beside the CLAUDE.md the gates hold
      Given a consuming repository with AGENTS.md and CLAUDE.md at its root
      And bindings whose context file row names CLAUDE.md
      When the wiring is audited
      Then a line reads open, saying Pi reads AGENTS.md and never reads CLAUDE.md
      And the sitting is what it names to close it

    Example: one file
      Given a consuming repository whose only instructions file is AGENTS.md
      When the wiring is audited
      Then that line reads clear

  @rule:every-host-in-use-loads-it
  Rule: Every host in use — the one running the audit, and each the tree shows — loads the plugin from a declaration the repository commits, a local path to the plugin's own checkout included

    Example: a host the tree shows declares nothing
      Given a repository with a Pi settings file that loads no livespec
      When the wiring is audited
      Then Pi is reported open, with the sitting that declares it

    Example: the audit runs under a host the repository never declared
      Given a repository declaring livespec for Claude Code only
      When the wiring is audited from a Pi session
      Then Pi is reported open

    Example: the plugin's own repository loads its checkout
      Given the plugin's repository declaring its own checkout to Pi by a relative path
      When the wiring is audited
      Then the declaration is read as loading livespec

    Example: every host in use declares it
      Given a repository whose committed settings load livespec for each host in use
      When the wiring is audited
      Then each is named with where it is declared

  @rule:the-pi-tag-bounds-the-ledger
  Rule: Where the repository pins livespec for Pi, the pin is a release tag not below the ledger's ceiling, no row is raised above it, and a sitting whose plugin is ahead of it plans the tag's move

    Example: the pin is below the ceiling
      Given a Pi pin on a release below the version a row was reconciled at
      When the wiring is audited
      Then the pin is reported open, below the ceiling

    Example: the pin is a branch
      Given a Pi pin on a branch, and bindings that do not say it was kept on purpose
      When the wiring is audited
      Then the pin is reported open, to be edited to a release tag
      And the same pin kept on purpose in the bindings is not applicable

    Example: an answer above the pin is held
      Given a transaction to a release above the Pi pin, with a gate wired
      When it is finalized
      Then the gate's row is raised only as far as the pin, the gate is held, and the transaction stays open

    Example: the plugin is ahead of the pin
      Given a Pi pin below the plugin installed
      When the plan is written
      Then the transaction carries an item moving the pin, and that item never keeps it open

@feature:setup-hand-back @workflow:adopt-the-process
Feature: What a setup sitting leaves behind

  @rule:setup-continues-into-the-layers
  Rule: The sitting continues into the layers rather than naming them

    Example: the interviews follow without being asked for
      Given setup has written the skeleton, the gates and CLAUDE.md
      When it hands back
      Then the persona, workflow and journey interviews have been started
      And nobody had to type the command that starts them

    Example: the chain is stopped partway
      Given the interviews have begun
      When somebody says to stop
      Then the sitting ends there
      And the hand-back names which layers are still empty

  @rule:setup-finds-where-issues-go
  Rule: The repository's own way of filing issues is found and written down

    Example: the tracker is not the one a skill would have assumed
      Given a consuming repository whose issues are filed somewhere other than GitHub
      When the sitting ends
      Then CLAUDE.md names where issues actually go there

    Example: there is no convention to find
      Given a consuming repository with no way of filing issues
      When the sitting ends
      Then that is reported rather than left blank

  @rule:setup-audits-an-existing-claude-md
  Rule: An existing CLAUDE.md is read against the requirements, not counted as done

    Example: the file is already there
      Given a consuming repository that already has a CLAUDE.md
      When setup reaches it
      Then each requirement is reported as met, missing or stale
      And the file existing has not counted as the step being finished

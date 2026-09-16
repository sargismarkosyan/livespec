@feature:setup-context-file @workflow:adopt-the-process
Feature: What CLAUDE.md is held to, and what it is not held to

  @rule:the-ceiling-is-a-number-in-the-bindings @planned
  Rule: The size CLAUDE.md may not exceed is a number in the repository's own bindings, written from what the file is when the sitting has finished with it, and the method names no figure of its own

    Example: the sitting writes the number after the file
      Given a consuming repository having the process set up
      When the sitting has written CLAUDE.md
      Then the bindings carry the file's size as its ceiling, with what reads it and which change set it
      And no figure was taken from the method, which names none

    Example: an occupied repository's file is measured after its audit, not before
      Given a consuming repository that already has a CLAUDE.md
      When the sitting has read it against the requirements and made its edits
      Then the ceiling written is the size the file is after those edits

  @rule:a-dated-account-that-still-binds-is-not-history @planned
  Rule: A dated account of what the file used to say stays while it still changes what the next change may do, and is history only once it binds nothing

    Example: the paragraph that stops the next wrong argument
      Given a CLAUDE.md whose account of where it lives says what it used to claim, until when, and which change argued wrongly from it
      When the file is read against the requirements
      Then that paragraph is reported as a rule with its evidence attached, and met
      And it is not reported as history to remove

    Example: an account that binds nothing now
      Given a CLAUDE.md carrying a dated account of a migration long finished, which no change is constrained by
      When the file is read against the requirements
      Then it is reported as history
      And the change specs and the version history are named as where it goes

  @rule:the-requirements-are-the-only-reference @planned
  Rule: A CLAUDE.md is held to the requirements and to no other repository's file

    Example: a file shaped like nobody else's
      Given a consuming repository whose CLAUDE.md is shaped like no other repository's
      When the file is read against the requirements
      Then each requirement is reported met, missing or stale on its own terms
      And no other repository's file is offered as the shape it should take

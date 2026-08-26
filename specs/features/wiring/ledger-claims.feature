@feature:wiring-ledger-claims @workflow:adopt-the-process
Feature: What a gate wiring ledger is allowed to claim

  @rule:a-claim-outside-the-tree-is-read-back @planned
  Rule: A row about something the repository cannot see is read from what owns it, or it is not written as fact

    Example: the required check is named in CI and enforced by nothing
      Given a consuming repository whose CI config names a check on every change
      And the platform hosting it does not block a merge when that check fails
      When the row for branch protection is written
      Then what the platform reports is what the row says
      And the row names the command that reads it back

    Example: the platform cannot be reached from this session
      Given a consuming repository whose branch protection cannot be read from here
      When the row for it is written
      Then the row says it was not read back, and why
      And nothing in the bindings asserts a setting nobody looked at

    Example: the bindings say a credential is absent and it is not
      Given bindings claiming the token that would post the report does not exist
      And that token is present where the platform keeps it
      When the wiring is audited
      Then that claim is reported as false
      And what was read to find that out is named

  @rule:a-row-says-what-it-leaves-uncovered @planned
  Rule: A gate wired over part of a repository is not recorded as covering it

    Example: coverage is wired for one of the two languages in the repository
      Given a consuming repository with a coverage gate over one language only
      When the row for coverage is written
      Then it names the part of the repository that has no gate
      And it does not read as a gate over the whole of it

    Example: the audit finds a row covering less than it claims
      Given a row reading automated for a gate wired over half the tree
      When the wiring is audited
      Then that row is reported as claiming more than was wired

  @rule:a-gap-is-a-row-not-a-sentence @planned
  Rule: Wiring named as missing becomes a row on the clock, including wiring that may never gate

    Example: something that must never gate is left described in prose
      Given bindings whose prose says the rule-bound measure is not built yet
      When the wiring is audited
      Then it is reported as a row rather than a sentence
      And the change it has been deferred since is named

    Example: the report was configured and nobody watched it arrive
      Given a consuming repository whose pull request report is wired and has posted nothing
      When the wiring is audited
      Then the row for the report reads unobserved
      And it is on the same clock as a gate

@feature:wiring-a-stack-lands-on-main @workflow:adopt-the-process
Feature: What an audit reads back about stacked pull requests

  @rule:the-delete-on-merge-setting-is-read-back @crosses:consuming-repository
  Rule: The audit reads back from the platform whether a merged pull request's branch is deleted, and reports it open when it is not

    Example: the setting was turned off after the sitting
      Given bindings recording that merged branches are deleted
      And a platform that now keeps them
      When the audit reads the setting back
      Then the line reads open, naming what the platform answered and the date the bindings claim

    Example: the platform does not answer
      Given a token the platform refuses
      When the audit reads the setting back
      Then the line reads not-read, with the refusal

  @rule:a-merge-that-missed-main-is-listed @crosses:consuming-repository
  Rule: The audit lists every pull request merged since the stamp into a branch other than main whose commits never reached main, and changes nothing

    Example: a stack stranded on a merged parent
      Given a pull request merged into its parent's branch after the parent had merged to main
      And its commit is on no branch main contains
      When the audit reads the merged pull requests back
      Then the line reads open, listing that pull request with its base and the commit main lacks

    Example: a stack retargeted in time
      Given a pull request based on another's branch, retargeted to main before it merged
      When the audit reads the merged pull requests back
      Then it is not listed

    Example: a stack whose work arrived another way
      Given a pull request merged into a parent's branch whose commits later reached main through another pull request
      When the audit reads the merged pull requests back
      Then it is not listed, because main has the commits

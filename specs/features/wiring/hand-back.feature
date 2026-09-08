@feature:wiring-hand-back @workflow:adopt-the-process
Feature: How an audit hands over what it could not build

  @rule:the-last-line-is-the-command-to-run
  Rule: Where the audit leaves wiring to be built, its reply ends with the command that starts the sitting, as somebody would type it, and what that sitting will be asked to wire — never the skill's name as a noun

    Example: rows are left deferred
      Given a consuming repository whose audit has written rows reading deferred
      When the audit hands back
      Then its last line is the command that starts the sitting, as somebody would type it here
      And the rows the sitting will be asked to wire are listed after it

    Example: the same line closes the record
      Given an audit that has written its reading into the bindings
      And rows it left for the sitting
      When the reading's record is written
      Then it ends with the same command and the same rows
      And a person reading the record knows what to type without knowing which skill owns what

    Example: nothing is left for the sitting
      Given a consuming repository whose audit corrected only the record
      When the audit hands back
      Then no line sends anybody to a sitting
      And the reply ends on what was corrected

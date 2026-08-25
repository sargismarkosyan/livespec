@feature:setup-demonstration @workflow:adopt-the-process
Feature: The sitting using the pipeline it wired, or saying it could not

  @rule:the-sitting-ends-by-using-the-pipeline @planned
  Rule: The sitting ends by putting its own work through the pipeline it wired

    Example: the interviews left something to land
      Given the interviews have written change specs
      When the sitting ends
      Then those specs have been opened as a pull request in that repository
      And the hand-back says what the required check did with it

    Example: the report was wired and never appeared
      Given the sitting wired a report onto that repository's pull requests
      When the pull request it opened comes back carrying none
      Then the hand-back says the report did not appear
      And the bindings do not claim that it is posted

  @rule:wiring-nobody-ran-is-not-claimed @planned
  Rule: Wiring the sitting could not watch run is recorded as unobserved

    Example: there is nowhere to open a pull request
      Given a consuming repository with no remote to open one against
      When the sitting ends
      Then the hand-back says the pipeline wiring is unobserved, and why
      And nothing in the bindings asserts a behaviour nobody ran

    Example: the required check never ran on the pull request
      Given a pull request the sitting opened
      And the required check did not run on it
      When the ledger is written
      Then that row reads unobserved
      And it does not read automated

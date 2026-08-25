@feature:setup-test-binding @workflow:adopt-the-process
Feature: How a test claims a rule in this repository

  @rule:setup-asks-how-a-test-claims-a-rule
  Rule: What a behaviour test is here is answered by the human, not assumed

    Example: the repository has no application code to call
      Given a consuming repository whose product is prose rather than code
      When the process is being set up in it
      Then how a behaviour test names its rule is asked about
      And nothing is written until it has been answered

    Example: the repository already tests the ordinary way
      Given a consuming repository with a test suite already running
      When the process is being set up in it
      Then what it already has is what gets recommended
      And a second way of testing is not introduced alongside it

  @rule:setup-scaffolds-the-rule-binding
  Rule: The sitting leaves behind the thing a test uses to name its rule

    Example: the answer was an ordinary test suite
      Given the human has said behaviour is proved by the existing tests
      When the sitting ends
      Then a test can name the rule it exists for
      And naming a rule that does not exist is refused where the test is written

    Example: the answer was graded cases
      Given the human has said behaviour is proved by graded cases
      When the sitting ends
      Then the tool that already builds such a suite is what was used
      And no case format was invented for this repository

  @rule:the-spec-bound-measure-is-reported-never-gated
  Rule: What the rule-bound tests reach on their own is reported apart from the gated number

    Example: the rule-bound tests reach less than the whole suite does
      Given a consuming repository whose tests include ones claiming no rule
      When the change is reported on
      Then what the rule-bound tests reach alone is shown separately
      And the number that decides the build is still the whole suite's

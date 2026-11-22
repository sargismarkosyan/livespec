@feature:setup-the-gate-says-why @workflow:adopt-the-process
Feature: A gate the sitting wires says why it failed

  @rule:a-failure-prints-what-it-means @planned
  Rule: Each failure the traceability gate the sitting writes reports names where it is and what it means — the reason and the fix — in the words of that failure's row in the method, not only what failed

    Example: a live rule with no test
      Given the sitting has written the traceability gate
      And a live rule that no test claims
      When the gate runs
      Then it fails naming the rule and its file
      And it says the behaviour was specced and never verified: write the test, or tag the rule

    Example: a test naming a rule that does not exist
      Given a test claiming a rule id nobody wrote
      When the gate runs
      Then it fails naming the test and the id
      And it says that is usually a typo or a renamed id, and that rule ids are permanent

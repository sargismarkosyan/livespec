@feature:wiring-what-ran @workflow:adopt-the-process
Feature: What the build refuses about a test that did not run

  @rule:a-test-that-did-not-run-claims-nothing @planned
  Rule: A rule-bound test marked skipped, focused or expected to fail claims no rule, and verification fails naming the marker and the rule it leaves untested

    Example: a skip on a rule-bound test
      Given a consuming repository whose rule-bound test carries the runner's skip marker
      When verification runs
      Then it fails, naming the test, the marker and the rule it claims
      And the rule reads as untested, whatever the runner's summary line says

    Example: an expected failure is the same
      Given a rule-bound test marked as expected to fail
      When verification runs
      Then it fails the same way
      And the marker is named as what makes the claim empty

    Example: a skipped unit test is not the gate's business
      Given a test outside the rule-bound tests that carries a skip marker and claims no rule
      When verification runs
      Then nothing is reported for it

  @rule:fewer-ran-than-exist-is-a-failure @planned
  Rule: When the runner reports fewer rule-bound tests than the tree holds, verification fails with both numbers, whatever the summary line says

    Example: a test the runner never discovers
      Given a rule-bound test in a class or file the runner's discovery does not reach
      When verification runs
      Then it fails, naming how many the tree holds and how many ran
      And a green summary line from the runner does not stand in for the count

    Example: a run that stopped early
      Given a runner that exited before the last file
      When verification runs
      Then it fails with the two numbers

    Example: more ran than the tree holds is not a failure
      Given a runner that reports more tests than the tree's count, because tests are inherited or generated
      When verification runs
      Then the count is not what fails it

  @rule:the-sitting-wires-what-ran @planned
  Rule: The sitting wires the gate to read the runner's own per-test report and compare it with the tree, records how that report is read in the bindings, and says so where the runner cannot report per test

    Example: the runner can say what it ran
      Given a consuming repository whose runner can report per test
      When the process is set up in it
      Then the gate the sitting writes counts the rule-bound tests in the tree against the runner's report
      And the bindings name the form of that report beside the discovery pattern
      And the fault record it leaves carries a skipped test and a short count, each expected to fail

    Example: the runner cannot say what it ran
      Given a consuming repository whose runner reports only a summary line
      When the process is set up in it
      Then the bindings say so and name what that leaves open
      And the summary line is not read as the count

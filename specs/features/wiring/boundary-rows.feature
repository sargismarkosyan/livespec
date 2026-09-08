@feature:wiring-boundary-rows @workflow:adopt-the-process
Feature: What a boundary row is allowed to claim, read against the tests that ran

  @rule:a-real-row-over-a-world-the-tests-never-enter @planned
  Rule: A row reading real is read against the rule-bound tests and against whether the thing starts from here, and a row the tests contradict is reported and corrected in the record

    Example: the bindings say the store is real and the tests never reach it
      Given a consuming repository whose bindings say its store is reached for real
      And whose behaviour tests run over an in-memory stand-in for it
      When the wiring is audited
      Then the row is reported as claiming a world the tests never enter
      And it is corrected to mocked, naming the tests that contradict it

    Example: the thing the row names cannot be started from this session
      Given a consuming repository whose bindings say its store is reached for real
      And the session cannot start that store from where it is standing
      When the wiring is audited
      Then the row says it was not read back, and why
      And it is not corrected on that evidence alone

    Example: the row is true
      Given a consuming repository whose bindings say its store is reached for real
      And whose rule-bound tests reach it and the store starts from here
      When the wiring is audited
      Then nothing about that row is reported
      And no correction is offered that nobody needs

  @rule:a-stand-in-nothing-checks-is-on-the-clock @planned
  Rule: A fake row with no suite against the real thing, or a recording older than the bindings allow, is reported as a stand-in nothing checks and put on the two-change clock

    Example: a fake row names no suite
      Given a consuming repository whose bindings say its store is a fake
      And no suite runs against both the fake and the real store
      When the wiring is audited
      Then the row is reported as a mock rather than a fake
      And it is corrected to mocked, dated from this reading

    Example: a recording is past its age
      Given a consuming repository whose bindings say its sign-in is recorded, with an age the recordings may not exceed
      And the recordings are older than that
      When the wiring is audited
      Then the row is reported with the date the recordings were made
      And it is on the clock with the other rows that are past theirs

    Example: a mocked row has been on the clock across two changes
      Given a consuming repository whose bindings hold a mocked row dated two changes ago
      When the wiring is audited
      Then the row is reported as either wired or written off
      And written off means unreachable, with the reason in the row and every change touching it saying so

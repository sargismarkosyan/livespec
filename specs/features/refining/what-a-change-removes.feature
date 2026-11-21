@feature:refining-what-a-change-removes @workflow:adopt-the-process
Feature: A change spec says what it removes

  @rule:a-spec-names-what-it-removes
  Rule: When a request withdraws a behaviour, the change spec's What this removes names the rule, the tests that claim it and the code only that rule needed, and the spec edits no source

    Example: the place goes
      Given fieldnote's rule place-carries-from-the-last-sighting, a test claiming it, and a where field the code writes and renders
      And the person says the place is always the weir and he stopped filling it
      When the request is refined into a spec
      Then What this removes names place-carries-from-the-last-sighting, the test that claims it, and the where field
      And no file under src/ or tests/ is touched

    Example: a change that only adds
      Given a request that withdraws nothing
      When the request is refined into a spec
      Then What this removes says nothing goes, and why

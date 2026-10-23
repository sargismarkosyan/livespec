@feature:wiring-a-workflow-names-its-phase @workflow:adopt-the-process
Feature: A workflow names the phases of its journey it is made in, and the map places it there

  @rule:a-workflow-names-only-phases-its-journey-has
  Rule: Verification fails when a workflow names a phase that no journey it names has, and says which phases exist; a workflow naming no phase passes without a warning

    Example: a phase the journey does not have
      Given the journey's map is headed Before, Putting it in and Coming back
      And a workflow naming that journey names the phase the-change-after
      When verification runs
      Then it fails, naming the workflow, the journey and the phases before, putting-it-in and coming-back

    Example: a phase renamed in the journey
      Given a workflow names the phase putting-it-in
      And the journey's heading Putting it in is renamed Setting it up
      When verification runs
      Then it fails on the workflow, until its tag names setting-it-up

    Example: no phase is named
      Given a workflow names its journey and no phase
      When verification runs
      Then it passes, and says nothing about phases in its warnings

  @rule:the-map-places-each-workflow-in-its-phases
  Rule: The map the gate prints lists every journey's phases in the order of its map, with the workflows naming each, says where nothing does, and lists apart the workflows naming the journey and no phase

    Example: a journey with a phase nothing reaches
      Given the journey's map is headed Before, Putting it in and Coming back
      And one workflow names putting-it-in
      When verification runs
      Then the map lists the three phases in that order
      And the workflow is under putting-it-in
      And before and coming-back say nothing names them

    Example: a workflow not yet placed
      Given a second workflow names the journey and no phase
      When verification runs
      Then the map lists it under the journey as not yet placed in a phase

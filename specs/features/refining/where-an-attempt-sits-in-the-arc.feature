@feature:refining-where-an-attempt-sits-in-the-arc @workflow:adopt-the-process
Feature: A workflow says where in the arc it is made, and a journey says where the arc goes round

  @rule:a-workflow-names-the-phase-it-is-made-in @planned
  Rule: A workflow refined against a journey with a map names the phase or phases of that journey the attempt is made in, read from the map's headings, and never adds or renames a phase to fit one

    Example: the journey has the phase
      Given the journey's map has a phase in which the attempt plainly happens
      When the workflow is written
      Then its first line names that phase with @phase:, as the heading reads in the journey
      And the journey is unchanged

    Example: no phase fits
      Given no phase of the journey is where the attempt happens
      When the workflow is written
      Then it names no phase, and the hand-back says that none fits
      And no phase is added to the journey to make one fit

  @rule:a-journey-says-where-it-goes-round @planned
  Rule: Where the arc goes back to an earlier phase, the journey says so in one line under its map, naming both phases by their headings, and never as a phase of its own

    Example: a year that starts again
      Given the person describes the arc ending each winter and starting over the next spring
      When the journey is written
      Then a line under the map says it goes round from the last phase to the first, naming both
      And no column of the map is a repeat, a loop or a cycle

    Example: an arc lived once
      Given the arc is lived once from start to end
      When the journey is written
      Then nothing says it goes round

@feature:showing-owed-in-this-repository @workflow:adopt-the-process
Feature: What a repository records about the sketch it owes at the approval step

  @rule:the-bindings-say-a-sketch-is-owed-here @planned
  Rule: A consuming repository comes out of the sitting with its bindings saying which changes here owe a sketch before approval, and with its own account of the loop saying what the person holds at that step

    Example: the sitting ends
      Given a consuming repository having the process set up
      When the sitting ends
      Then the bindings say which changes here owe a sketch before approval
      And they say it is drawn from the change spec rather than recorded from the app

    Example: there is nothing on a screen in this repository
      Given a consuming repository whose bindings record that there is nothing to see
      When the row for the sketch is written
      Then the line that exempts the picture is not carried over to it
      And a repository with no screen is recorded as still owing one

    Example: the repository keeps its own account of the loop
      Given a consuming repository whose own context file walks through the loop
      When that file is written or audited
      Then its approval step says the person holds the sketch as well as the spec

  @rule:what-arrived-after-the-bindings-were-written-is-caught @planned
  Rule: An audit reports what the recorded process never mentioned because it did not exist yet, and offers the row rather than waiting for something to announce the absence

    Example: the bindings were written before the sketch existed
      Given bindings reconciled against a version of this method with no sketch in it
      When the wiring is audited
      Then the missing row is reported with what closes it
      And the row is offered as it will read

    Example: the bindings already say what a change here must show
      Given bindings carrying the row for the picture a version ships with
      When the wiring is audited
      Then that row is not read as covering the sketch as well
      And the two are reported as separate things arriving at separate steps

    Example: nothing in the pipeline could ever have reported it
      Given a requirement that no build here can fail on
      When the wiring is audited
      Then it is held on the same clock as the wiring that must never gate
      And its absence is not left to be noticed by the next sitting

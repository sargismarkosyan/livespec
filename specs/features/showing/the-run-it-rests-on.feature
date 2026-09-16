@feature:showing-the-run-it-rests-on @workflow:adopt-the-process
Feature: What a pull request carries about the run its claim of green rests on

  @rule:a-claim-of-green-carries-the-run
  Rule: A pull request that changes the tests, or what runs them, carries the run — the verification command as the bindings name it, and the runner's own output under it — and one that carries none, or one quoting a different command, cannot merge

    Example: the run is quoted under the command the bindings name
      Given a pull request that changes a rule-bound test
      And its body carries a fenced block opening with the verification command as the bindings name it, with the runner's output beneath
      When the release inputs are checked
      Then the run is read and the pull request may merge

    Example: a claim with no run under it
      Given a pull request that changes a rule-bound test
      And its body says the tests pass and quotes no run
      When the release inputs are checked
      Then it cannot merge, and the refusal says what the block is and where the command is named

    Example: a run of some other command
      Given a body whose fenced block opens with a command that is not the one the bindings name
      When the release inputs are checked
      Then it cannot merge, naming the command the bindings name

    Example: a change that touches no test owes none
      Given a pull request that changes a method page and nothing the verification reads or runs
      When the release inputs are checked
      Then no run block is asked for

  @rule:the-report-prints-its-own-run-beside-the-claim
  Rule: The report on a pull request prints the tail of the pipeline's own verification run beside what the body's run block says, and gates on nothing, including the two disagreeing

    Example: two runs, side by side
      Given a pull request whose body carries a run block
      When the report is built from the pipeline's run
      Then it shows the body's block and the pipeline's own tail beside each other
      And a difference between them is on the page and fails nothing

    Example: a body with no run block
      Given a pull request whose body carries no run block
      When the report is built
      Then it says so beside the pipeline's own tail
      And whether one was owed is the gate's to say, not the report's

    Example: the pipeline's run could not be read
      Given a report built with no run to print
      When it is built
      Then it says the pipeline's run was not available and prints the rest

  @rule:the-picture-names-its-world
  Rule: The hand-back that delivers a version's picture says which boundary rows the app was served over when it was taken, in the same breath as the form the picture took

    Example: a clip over the real store and a seeded session
      Given a version recorded with the store the bindings call real and a sign-in the bindings call a stand-in
      When the picture is handed over
      Then the hand-back names both, beside whether the picture moves or stands still

    Example: a picture over a stand-in is a picture of the stand-in
      Given a version recorded with every boundary doubled
      When the picture is handed over
      Then the hand-back says so before it says anything about the frames

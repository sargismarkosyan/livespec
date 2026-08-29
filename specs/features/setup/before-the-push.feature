@feature:setup-before-the-push @workflow:adopt-the-process
Feature: The cheap half of verification, run before the work leaves the machine

  @rule:a-local-run-is-offered-before-the-push
  Rule: Running the verification command before a push is offered, and waits for an answer

    Example: the gates are wired and nothing fires them locally
      Given a sitting that has wired the gates behind one command
      When it reaches the end of wiring them
      Then running that command before a push is offered, with what it would write
      And nothing has been installed while the offer is unanswered

    Example: the offer is declined
      Given the offer has been made
      When it is turned down
      Then nothing is written
      And the sitting continues into the bindings

    Example: per-commit is asked for instead
      Given somebody asks for the command to run on every commit
      When the offer is made
      Then it is at push, with the reason that a branch would run it once per commit to learn the same thing once

  @rule:what-costs-money-stays-out-of-the-hook
  Rule: Only checks that are free and clearable here run before a push

    Example: the one command runs a graded suite as well as the gates
      Given a repository whose verification runs a suite that costs money per run
      When the local run is offered
      Then it carries the free checks and not the graded suite
      And the reason given is what a run of it costs whoever is paying

    Example: a check whose failure needs an eval run to clear
      Given a check that is red for a reason the method sanctions
      And whose only fix is a run somebody has to pay for
      When the local run is offered
      Then that check is left to the pipeline
      And the offer says which part it left there

  @rule:a-local-hook-is-not-a-gate
  Rule: A local check before a push is recorded as a courtesy or not at all

    Example: the ledger is written after one is installed
      Given a repository that has agreed to run the checks before a push
      When the gate wiring ledger is written
      Then neither table has a row for it
      And what it runs is described where the bindings keep what is true of one machine

    Example: the pipeline is looked at afterwards
      Given the checks now run before a push
      When the required checks are reviewed
      Then nothing has been removed from them

    Example: the wiring is audited and a hook is described in the prose
      Given bindings whose prose describes a check that runs before a push
      And that check is opt-in and can be skipped with a flag
      When the wiring is audited
      Then no row is added for it in either table
      And it is not counted as coverage

@feature:verification-which-red @workflow:adopt-the-process
Feature: A verification that can be red without anything being broken

  @rule:the-one-red-a-commit-may-carry
  Rule: A state whose only failure is a measurement waiting on a spend nobody in the session can approve may be committed and pushed, and says so

    Example: a skill body moves and the cases holding it go stale
      Given verification is red only because measurements no longer describe the files they measured
      And clearing them needs a run the person working cannot approve
      When the work is committed
      Then the commit says which measurements are waiting and why nothing here can clear them
      And the change is pushed rather than held

    Example: something is actually broken as well
      Given verification is red for a stale measurement and for a gate that no longer holds
      When the work is committed
      Then the broken gate is fixed first
      And the exception is not claimed for a state that carries anything else

    Example: the branch reaches the point of merging
      Given a change pushed with measurements still waiting on a run
      When it is put up for review
      Then what is waiting is still reported on the change
      And no purchase stands between finished work and merging it

  @rule:a-red-says-which-red-it-is
  Rule: Where verification can fail for a reason the method sanctions, its result says which of the two happened without anybody reading the log

    Example: the only failure is bookkeeping waiting on a run
      Given verification whose one command runs both the free gates and a freshness check on a graded suite
      When the freshness check is the only thing failing
      Then the result is distinguishable from a broken gate
      And what it prints names the cases, what a run costs, and who can approve one

    Example: a gate is broken underneath a stale measurement
      Given verification failing on both a gate and a stale measurement
      When it finishes
      Then it reports the broken gate rather than the waiting one
      And nothing about the sanctioned failure softens what a broken gate means

    Example: a repository with nothing that costs money to clear
      Given verification whose every failure can be cleared by whoever ran it
      When it fails
      Then it says so the one way it always has
      And no second kind of red has been invented for a state this repository cannot enter

  @rule:what-explains-a-red-survives-it
  Rule: Whatever a repository posts to explain its state still runs when the state is the sanctioned red

    Example: the report is what would have said which red it was
      Given a report posted on every change, carrying how many measurements are waiting
      When verification fails on exactly those measurements
      Then the report is still posted
      And the count it exists to carry is one somebody can read on the change it describes

    Example: the report cannot rescue a build by running
      Given a report that now runs after a failing verification
      When it is built and posted
      Then whether the change may merge is unchanged by it
      And a report that cannot be built still says nothing and fails nothing

  @rule:a-red-does-not-hide-the-gates-after-it
  Rule: A gate that does not depend on a failing one still runs on the same red build, and still gates

    Example: the sanctioned red is standing and something else is wrong as well
      Given verification red only because a measurement is waiting on a spend nobody in the session can approve
      And a second gate reading the change itself rather than the tree
      When the run finishes
      Then the second gate has said whether it passed
      And what is still owed was learned on one run rather than on the run after the bill was settled

    Example: speaking later does not turn a gate into a report
      Given a gate that now runs after a failing gate
      When it finds something wrong
      Then the change still cannot merge
      And running late has changed when it speaks and never whether it blocks

    Example: a gate whose prerequisite never ran
      Given a gate that cannot run until an earlier step has prepared what it needs
      And that earlier step failing
      When the run carries on
      Then the gate is not made to run anyway
      And nothing reports a second failure that is only the first one restated

  @rule:a-measurement-nobody-can-clear-does-not-block @planned
  Rule: A check whose only cure is a purchase nobody in the session can approve is reported on its own and blocks nothing, while every check somebody can clear still blocks

    # @planned because no case here can reach it: what it promises is about a
    # merge, and a case is one session against one prompt. Softening it into
    # something a session could pass would buy the tag with the dishonesty
    # evals/README.md warns about. See 0033, *Data*.

    Example: the only thing outstanding is a bill
      Given a change whose gates all hold and whose measurements are waiting on a run
      When the pipeline finishes
      Then the checks that gate have passed
      And what is owed is failing on its own, where somebody will see it

    Example: a gate is broken as well
      Given a change with a broken gate and a stale measurement
      When the pipeline finishes
      Then the change cannot merge
      And the reason it cannot is the gate rather than the bill

    Example: the bill is never paid
      Given a repository merging changes with measurements owed
      When somebody asks what has gone unmeasured
      Then the count is on every change rather than in a log
      And nothing has quietly stopped reporting it because it stopped blocking

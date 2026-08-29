@feature:verification-which-red @workflow:adopt-the-process
Feature: A verification that can be red without anything being broken

  @rule:the-one-red-a-commit-may-carry @planned
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
      Then the pipeline is still red
      And the exception has bought a commit and a push, never a merge

  @rule:a-red-says-which-red-it-is @planned
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

  @rule:what-explains-a-red-survives-it @planned
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

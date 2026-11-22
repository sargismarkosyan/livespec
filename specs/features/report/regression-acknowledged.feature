@feature:regression-acknowledged @workflow:adopt-the-process @uses:workflow-cost
Feature: A walk past its allowance is answered in the pull request

  @rule:a-regression-past-its-allowance-is-acknowledged @planned
  Rule: When a walk is worse past its allowance, the gate fails until the pull request's Performance section names that walk, and passes once it does, however large the slowdown

    Example: nobody said why
      Given a branch whose checkout walk is past its allowance
      And a pull request body with no Performance section
      When the comparison runs as the gate
      Then it fails, naming the checkout walk and the section that would answer it

    Example: the slowdown is worth it, and the pull request says so
      Given a branch whose checkout walk is past its allowance
      And a Performance section saying "checkout: the new card form loads its fonts, accepted"
      When the comparison runs as the gate
      Then the gate passes

    Example: within the allowance, nothing is owed
      Given a branch whose checkout walk is worse but within its allowance
      And a pull request body with no Performance section
      When the comparison runs as the gate
      Then the gate passes, and the report still leads with the checkout walk

  @rule:the-acknowledgement-is-quoted-beside-the-walk @planned
  Rule: The report quotes the line that answered a walk beside that walk, so the reviewer reads the cost and the reason together

    Example: an answered slowdown
      Given a Performance section saying "checkout: the new card form loads its fonts, accepted"
      When the report is written
      Then the checkout walk's line carries that sentence

  @rule:setup-wires-the-acknowledgement @planned
  Rule: The sitting hands the comparison the pull request's body, runs it again when the body is edited, and writes into the context file that a walk past its allowance is answered under a Performance heading in the body

    Example: a body edited after the run
      Given a pull request whose gate failed on an unanswered walk
      When its author adds the Performance section to the body
      Then the gate runs again on that edit, without a new commit

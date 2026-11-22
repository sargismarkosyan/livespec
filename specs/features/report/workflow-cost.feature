@feature:workflow-cost @workflow:adopt-the-process @uses:report-wiring
Feature: What a change costs each workflow walk

  @rule:setup-wires-the-cost-of-a-walk @planned
  Rule: A repository comes out of the sitting with the comparison copied in, a policy file, and a job that walks every workflow on the base and the branch in turns and reports the cost, or with a reason it cannot

    Example: a web application whose walkthroughs drive a browser
      Given a consuming repository whose workflow walkthroughs already drive a headless browser
      When the sitting wires the cost of a walk
      Then the comparison is copied into the repository at the version installed
      And a job walks the base and the branch in turns on one runner, the rounds the policy file names
      And the report it posts cannot fail the build

    Example: nothing walks a workflow for free here
      Given a consuming repository whose walkthroughs are graded cases that bill whoever runs them
      When the sitting wires the cost of a walk
      Then the bindings read not applicable, with that reason

  @rule:the-cost-is-the-branch-against-its-base @planned
  Rule: Each measure of each walk is reported as what moved between the base and the branch, and a difference inside the noise the policy names reads as no change, with no number

    Example: a change slows the checkout and nothing else
      Given a pull request whose checkout walk takes longer than its base, every round
      When the comparison runs
      Then the checkout walk reads worse, with the change and its interval
      And every other walk is listed once as no change

    Example: a difference smaller than the noise
      Given a pull request whose walks differ from the base by less than the noise
      When the comparison runs
      Then that walk reads no change, and no percentage is shown for it

  @rule:an-unclear-cost-is-inconclusive @planned
  Rule: When the walks cannot say whether the branch is worse, the measure reads inconclusive with the reason, never no change and never a failure

    Example: the interval straddles the noise
      Given a measure whose interval reaches both sides of the noise
      When the comparison runs
      Then it reads inconclusive, and the report says more rounds would decide it

    Example: the base could not be walked
      Given samples from the branch and none from the base
      When the comparison runs
      Then every measure reads inconclusive, saying the base has no samples
      And the gate passes

  @rule:a-slower-walk-is-said-not-refused @planned
  Rule: A walk that got worse leads the report, marked within or past the allowance the policy names, and the comparison does not fail on it, however large

    Example: the walk doubled
      Given a pull request whose checkout walk takes twice as long as its base
      When the comparison runs as the gate
      Then the report leads with the checkout walk, past its allowance
      And the gate passes

  @rule:a-budget-gates-only-a-count @planned
  Rule: A budget the policy sets on a count fails the gate when the branch crosses it, and a policy setting a budget on a time is refused before anything is compared

    Example: a walk crosses its budget
      Given a policy giving the checkout walk a budget of 42 requests
      And a branch whose checkout walk makes 43
      When the comparison runs as the gate
      Then it fails, naming the checkout walk, the measure, the budget and the 43

    Example: a time is given a budget
      Given a policy giving the checkout walk's load time a budget
      When the comparison runs
      Then it refuses the policy, saying a time cannot carry a budget, and compares nothing

  @rule:a-changed-budget-is-shown-beside-the-change @planned
  Rule: Where the branch's policy differs from the base's, the report lists every number that moved, beside the walks it now allows

    Example: the budget was raised in the same pull request
      Given a branch that raises the checkout walk's request budget from 42 to 50
      When the comparison runs
      Then the report says the budget moved from 42 to 50 in this pull request
      And the checkout walk's verdict is read against 50

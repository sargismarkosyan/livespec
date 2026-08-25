@feature:report-wiring @workflow:adopt-the-process
Feature: The report a repository posts on its own pull requests

  @rule:setup-wires-the-pull-request-report @planned
  Rule: A repository comes out of the sitting posting a report on its pull requests

    Example: the sitting ends and the wiring is there
      Given a consuming repository having the process set up
      When the sitting ends
      Then its pull requests carry a report of what the change did to the spec layer
      And the bindings name what produces it

    Example: the repository cannot post one
      Given a consuming repository whose pull requests cannot carry a comment
      When the sitting ends
      Then the hand-back says the report is not wired and why
      And nothing claims it was

  @rule:the-report-cannot-fail-the-build @planned
  Rule: The report never decides whether a change may merge

    Example: the report has nothing good to say
      Given a change that leaves the spec layer worse than it found it
      When the report is produced
      Then it says so
      And the change is not blocked by it having said so

  @rule:the-report-says-what-moved @planned
  Rule: The report describes the change, not only the state after it

    Example: a change that adds a rule
      Given a change that adds one live rule to the spec layer
      When the report is produced
      Then it shows that one rule was added
      And the totals alone are not what it reports

    Example: a change that claims to move the spec layer and does not
      Given a change whose description says it moves the spec layer
      And nothing in the spec layer actually moved
      When the report is produced
      Then it shows nothing moved

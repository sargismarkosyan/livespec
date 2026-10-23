@feature:showing-the-point-before-the-evidence @workflow:adopt-the-process
Feature: How a pull request body is read by the person deciding on it

  @rule:the-point-comes-before-the-evidence @planned
  Rule: A pull request body opens with what changed and why in two or three plain lines, then what the reviewer should look at in the diff; everything it owes as evidence comes after, the picture inline and the long blocks folded or linked

    Example: a change with a long run behind it
      Given a change whose session checked sixteen cases, read a lockfile and noted three caveats
      When the pull request body is written
      Then its first lines say what changed and why, and which file in the diff to read
      And the run, the case matrix and the caveats come after those lines, the long ones folded or linked

    Example: short is not bought by dropping what is owed
      Given a change that moved a feature file and the tests
      When the pull request body is written
      Then the Gherkin block and the run block are still in it, after the point
      And the picture, where one is owed, sits inline under the point rather than folded away

    Example: a body that opens with its evidence
      Given a body that starts with a before-and-after block and states the change in its last paragraph
      When the reviewer opens it
      Then the change was not written for them, however complete the evidence is

  @rule:each-fact-once-in-words-the-reviewer-has @planned
  Rule: Each fact is stated once, in words the reviewer already has; a caveat is not repeated, two pull requests that belong together link each other rather than carry the same block, and a term the session coined is replaced with what it names — the message asking for review held to the same

    Example: a caveat that applies twice
      Given a caveat about the test harness that bears on both the run and the picture
      When the pull request body is written
      Then it is stated once, where it applies, and not again under limits

    Example: a companion pull request
      Given a change split across two pull requests that share a before-and-after block
      When the second body is written
      Then it links the first for that block instead of carrying a copy

    Example: a name the session made up
      Given a session that has been calling its fixture "the shadow log" for an hour
      When the pull request body is written
      Then the reviewer reads what the fixture is, in plain words, and never the name

    Example: the message asking for review
      Given a pull request ready for review
      When the message asking somebody to review it is written
      Then it says the point, links the pull request, and says what the reviewer is asked to decide
      And it carries no term the reviewer has not seen before

  @rule:the-report-counts-what-comes-before-the-evidence @planned
  Rule: The report on a pull request counts the words its body says before its first heading, code block or folded block, prints the count, and gates on nothing there

    Example: a body that opens with its point
      Given a body whose first lines say what changed and why, above its first heading
      When the report is built
      Then it prints how many words come before that heading

    Example: a body that opens straight into its evidence
      Given a body whose first line opens a code block
      When the report is built
      Then it says nothing is said before the evidence

    Example: a long opening fails nothing
      Given a body with six hundred words before its first heading
      When the report is built
      Then the count is printed and nothing fails, and whether those words are the point is left to the reviewer

    Example: a body the report cannot read
      Given a report handed no body, an empty one or one it cannot decode
      When it is built
      Then it says so, or prints no count, and exits zero

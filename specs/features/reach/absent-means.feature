@feature:reach-absent-means @workflow:adopt-the-process
Feature: What a skill does when a step cannot be taken here

  @rule:an-unreachable-step-is-said-not-searched-for @planned
  Rule: What a step needs and cannot get here is said once, rather than searched for until the session is spent

    Example: the tool the bindings name cannot be run from this session
      Given a consuming repository whose bindings name the tool that files into its tracker
      And that tool cannot be run from where the session is standing
      When the skill reaches the step that would file
      Then it says in its reply that the step could not be taken here
      And it does not spend the rest of the session looking for another way to take it

    Example: the bindings a step is told to read were never written
      Given a consuming repository that records no bindings at all
      When a skill goes to read what its tracker is
      Then it says in one line that the repository records none
      And it does not hunt through the tree for a file nobody ever wrote

  @rule:what-did-not-need-it-is-still-handed-over @planned
  Rule: A step that cannot be finished here does not take the work before it down with it

    Example: the researched body outlives the tool that cannot file it
      Given a report the skill has already taken apart and investigated
      And the tool that would file it cannot be run from here
      When the skill reports back
      Then the issue body it wrote is in the reply
      And what to run to file it is there with it

    Example: a session that stops early still leaves something to act on
      Given a skill that cannot take its last step in this repository
      When it reports back
      Then the person can finish that step themselves
      And nothing they already paid for has to be investigated again

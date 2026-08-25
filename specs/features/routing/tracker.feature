@feature:routing-tracker @workflow:adopt-the-process
Feature: Which tracker a repository actually uses

  @rule:the-tracker-comes-from-the-bindings @planned
  Rule: The tracker is read from the repository's bindings, never assumed

    Example: the tracker is not the one a skill would have guessed
      Given a consuming repository whose bindings name a tracker
      When a skill files something
      Then it files through the tool those bindings name
      And no tracker is assumed anywhere in the attempt

    Example: the bindings do not say
      Given a consuming repository whose bindings name no tracker
      When a skill is about to file
      Then the tracker is worked out from what the repository already shows
      And what was worked out is said before it is relied on

  @rule:evidence-links-follow-the-tracker @planned
  Rule: A link to evidence is built for the host the repository actually uses

    Example: a screenshot filed against a repository hosted elsewhere
      Given a consuming repository whose tracker is not the one a skill would assume
      When a report carries a screenshot
      Then the link in what is filed resolves on that repository's own host

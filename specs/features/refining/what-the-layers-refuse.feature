@feature:refining-what-the-layers-refuse @workflow:adopt-the-process
Feature: The persona, workflow and journey layers are not written to make a wanted thing legal

  @rule:a-persona-invented-to-fit-a-feature-is-refused
  Rule: A persona asked for after the feature it would justify is refused, and who the product is for is argued on its own terms first

    Example: the feature came first
      Given a feature that already exists and a persona asked for to serve it
      When the persona is refined
      Then it is refused, with the order of arrival as the reason
      And no persona file is written or drafted

    Example: the argument is made without the feature
      Given the same request and a person who can say who the product is for
      When who it is for is argued without the feature in hand
      Then that argument is where a persona comes from, if one comes at all

  @rule:a-workflow-invented-for-an-orphan-feature-is-refused
  Rule: A workflow shaped like an orphan feature is refused, and the choice put back is whether the feature serves an attempt anybody makes

    Example: the gate is red and a workflow would make it green
      Given a feature no workflow claims and a request for a workflow shaped like it
      When the workflow is refined
      Then it is refused, naming that the feature came before the attempt
      And the choice put back is an attempt somebody actually makes, or no feature
      And no workflow file is written or drafted

  @rule:an-arc-with-no-seam-is-refused
  Rule: A journey in which every phase goes well is a future-state map, and is not written as the current one

    Example: the all-good first month
      Given a request for a journey in which nothing goes wrong
      When the journey is refined
      Then the arc is named as future-state and the seams as what a journey exists to carry
      And it is declined, or written only as future-state and kept apart from the current journey

  @rule:a-twice-deferred-row-stops-the-workflow
  Rule: A gate row deferred across two changes stops the workflow until it is wired or written off, and no reply claims a gate the ledger says is not there

    Example: two rows deferred since two changes ago
      Given a ledger whose workflow-to-persona and walked-end-to-end rows read deferred since two changes ago
      When a workflow is asked for
      Then the reply says those rows are not wired here and the workflow would be held by nothing
      And it ends on the choice — wire them now, or write them off with the reason in the row

    Example: the gate is spoken of as if it ran
      Given the same ledger
      When the reply says what holds the workflow
      Then it does not claim the gate will catch a workflow naming no persona
      And what the method requires is told apart from what is wired here

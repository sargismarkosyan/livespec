@feature:wiring-what-a-feature-uses @workflow:adopt-the-process
Feature: What the build holds a feature to when it names another feature it uses

  @rule:a-feature-uses-only-features-that-exist @planned
  Rule: Verification fails when a feature's @uses names no feature in the tree, naming the file and the id, and asks nothing of a feature that names none

    Example: the feature it uses is there
      Given the live queue's feature carries @uses:issue-card
      And a feature declares @feature:issue-card
      When verification runs
      Then nothing is reported about it

    Example: the shared feature was renamed
      Given the live queue's feature carries @uses:issue-card
      And the issue card's feature has since been renamed to @feature:issue-row
      When verification runs
      Then it fails, naming the live queue's file and issue-card
      And the fix it names is the id that exists now, or the tag removed

    Example: a feature that uses nothing owes nothing
      Given a feature carrying no @uses
      When verification runs
      Then nothing is asked of it about other features

    Example: a tag on a rule rather than the feature
      Given a Rule: in the live queue's feature carries @uses:issue-card
      When verification runs
      Then it fails, naming the rule, because @uses goes on the Feature: line

@feature:setup-coverage-binding @workflow:adopt-the-process
Feature: What the coverage gate is asked to demand

  @rule:the-coverage-demand-is-not-todays-score @planned
  Rule: What the sitting recommends is the whole of what is in scope, never the number the code happens to score today

    Example: the score becomes the threshold and the gate can only ever be met
      Given a consuming repository whose tests already reach most of what it ships
      When the sitting asks what the coverage gate should demand
      Then the whole of what is in scope is what gets recommended
      And what it scores today is not offered as the threshold

    Example: there is nothing to measure yet
      Given a consuming repository with no tests and no coverage tool
      When the sitting asks what the coverage gate should demand
      Then the bindings say the gate has nothing to stand on yet
      And no threshold is written for a run nobody makes

  @rule:what-is-not-covered-is-named-rather-than-subtracted @planned
  Rule: Whatever the demand does not reach is named where the gate is configured, with its reason beside it

    Example: an occupied repository on its first day
      Given a consuming repository with older modules no test reaches
      When the coverage gate is wired
      Then those modules are named as exclusions, each with the reason it is one
      And the demand over what is left is not lowered to make room for them

    Example: the gap arrives as a lower number instead
      Given somebody proposing a threshold with room in it for what they do not test
      When the sitting answers
      Then it asks which parts that room is standing in for
      And an exemption nobody can name is not written into the bindings

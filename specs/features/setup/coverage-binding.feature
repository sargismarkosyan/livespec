@feature:setup-coverage-binding @workflow:adopt-the-process
Feature: What the coverage gate is asked to demand

  @rule:the-coverage-demand-is-not-todays-score
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

  @rule:what-is-not-covered-is-named-rather-than-subtracted
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

  @rule:the-demand-is-recommended-as-a-figure @planned
  Rule: The recommendation says what the whole of the scope comes to, rather than describing its shape and leaving the figure to be worked out

    # @planned: the rule is written before the skill body carries it. The
    # figure is portable — it is the same in every consuming repository, which
    # is what separates it from the threshold that lands in the bindings.

    Example: the sitting recommends a shape and names no number
      Given a consuming repository whose sitting has settled what the coverage gate is over
      When the sitting recommends what that gate should demand
      Then the recommendation names the figure the whole of that scope comes to
      And the adopter is not left to convert a description into a number

    Example: most of the repository is outside the scope and the figure does not move
      Given a consuming repository excluding a generated client and a legacy importer
      When the sitting recommends what the gate should demand
      Then the figure is the whole of what remains once those exclusions are named
      And it is not lowered because part of the repository sits outside the scope

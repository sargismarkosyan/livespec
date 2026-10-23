@feature:refining-what-a-feature-builds-on @workflow:adopt-the-process
Feature: A feature that builds on another names it, and says only what it adds

  @rule:a-feature-names-the-feature-it-builds-on
  Rule: When a spec writes a feature that builds on a rule another feature owns, the feature carries @uses with that feature's id, and its own rule says what it adds and cites the shared rule by id rather than restating it

    Example: looking back reuses the species suggestions
      Given fieldnote's species-suggestions feature owns the rule that the name field suggests from the species list
      And the request is for the same suggestions when looking back through the log
      When the request is refined into a spec
      Then the feature holding the new rule carries @uses:species-suggestions
      And the new rule cites suggestions-come-from-the-species-list and adds only what looking back needs
      And species-suggestions itself is left without a list of who uses it

    Example: a feature that builds on nothing
      Given a request whose rule needs no other feature's rule
      When the request is refined into a spec
      Then the feature carries no @uses

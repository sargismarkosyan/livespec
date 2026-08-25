@feature:routing-destination @workflow:adopt-the-process
Feature: Whether a request is captured or built

  @rule:capture-and-build-are-different-destinations @planned
  Rule: What somebody reports is captured into the tracker; what somebody instructs becomes a change

    Example: a report reaches the tracker
      Given a consuming repository with the plugin installed
      When somebody says they found something wrong with the app
      Then it is captured as a tracked issue
      And no change spec is written for it yet

    Example: an instruction reaches the spec
      Given a consuming repository with the plugin installed
      When somebody says to add something to the app
      Then it is worked into a numbered change spec
      And nothing is filed into the tracker in place of it

    Example: the same wish is not split by wording
      Given a consuming repository with the plugin installed
      When somebody wishes aloud that the app also did something
      Then it is captured as a tracked issue
      And it goes to the same place however that wish was phrased

  @rule:capture-does-not-require-having-used-it @planned
  Rule: Capturing a request does not depend on it coming from having used the app

    Example: a request with nothing behind it but a wish
      Given a consuming repository with the plugin installed
      When somebody asks for something the app has never been used to attempt
      Then it is captured as a tracked issue
      And nothing asks them what they were doing when they found it

    Example: a report from actually using it
      Given a consuming repository with the plugin installed
      When somebody reports what happened while they were using the app
      Then it is captured as a tracked issue
      And what they were doing is captured with it

  @rule:an-instruction-to-build-is-not-filed-instead @planned @refusal
  Rule: An instruction to build is never answered by filing an issue about it

    Example: a solution-shaped instruction
      Given a consuming repository with the plugin installed
      When somebody names a change they want made to the app
      Then no tracked issue is created in place of specifying it

    Example: picking up something already tracked
      Given a consuming repository whose tracker already holds the request
      When somebody says to pick it up
      Then it is worked into a numbered change spec
      And no second issue is filed about the first

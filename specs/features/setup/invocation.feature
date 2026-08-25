@feature:setup-invocation @workflow:adopt-the-process
Feature: Reaching setup, and setup knowing it was not the thing asked for

  @rule:setup-can-be-offered
  Rule: In a repository with the plugin and no bindings, asking for the process reaches setup

    Example: the ask arrives in plain words
      Given a consuming repository with the plugin enabled and no bindings
      When somebody asks for the process to be set up there
      Then setup is what answers
      And no specs/ tree of the agent's own invention is offered in its place

  @rule:setup-confirms-before-writing
  Rule: Setup says what it would write, and waits to be told to start

    Example: the sitting is sized before it begins
      Given somebody has asked for the process
      When setup answers
      Then it names the files it would write, and the interviews that follow it
      And nothing has been written

  @rule:setup-ignores-an-adjacent-request @refusal
  Rule: A request that only sounds like setup gets the answer it asked for

    Example: a question about the checks already there
      Given a consuming repository with the plugin enabled and the process not set up
      When somebody asks what the existing checks run
      Then they are told what the checks run
      And the process is not installed in place of the answer

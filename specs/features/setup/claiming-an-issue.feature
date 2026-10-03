@feature:setup-claiming-an-issue @workflow:adopt-the-process
Feature: The sitting says how an issue is marked as taken

  @planned @rule:the-claim-marker-is-bound @crosses:consuming-repository
  Rule: The bindings name the marker that says an issue is taken, and where the tracker lacks it the sitting offers to create it and waits

    Example: the tracker has no such marker
      Given a tracker with no label meaning an issue is taken
      When the sitting reaches the bindings
      Then it offers to create one, naming it and the command that would create it
      And nothing is created in the tracker while the offer is unanswered

    Example: the repository already marks work as taken
      Given a tracker whose issues already carry a label the team uses for work in flight
      When the sitting reaches the bindings
      Then the row names that label rather than a second one

    Example: there is no tracker
      Given bindings saying there is no tracker
      When the claim row is written
      Then it reads not applicable, decided, with that as the reason

    Example: the tracker refuses the label
      Given the sitting's token cannot create labels in the tracker
      When the offer is accepted
      Then the row names the label as unmade, with the refusal, and the hand-back says who can make it

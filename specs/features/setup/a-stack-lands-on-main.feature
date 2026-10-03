@feature:setup-a-stack-lands-on-main @workflow:adopt-the-process
Feature: The sitting makes a stacked pull request land on the main branch

  @planned @rule:merged-branches-are-deleted-so-stacks-retarget @crosses:consuming-repository
  Rule: The sitting reads back whether the platform deletes a merged pull request's branch, and where it does not, offers to turn that on and waits, because that deletion is what retargets a pull request stacked on it

    Example: the setting is off
      Given a platform that keeps a pull request's branch after it merges
      When the sitting reads the protection back
      Then it says that a pull request based on that branch would merge into it rather than into main
      And it offers to turn deletion on, naming the setting and the command
      And nothing is changed on the platform while the offer is unanswered

    Example: the setting is already on
      Given a platform that deletes a merged pull request's branch
      When the sitting reads the protection back
      Then the protection table records it as read back, with the command and the date

    Example: the token cannot read the setting
      Given a token that is refused when it asks for the repository's settings
      When the sitting reads the protection back
      Then the row reads unobserved, with the refusal and who can read it

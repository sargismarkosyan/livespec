@feature:routing-repository @workflow:adopt-the-process
Feature: Which repository a skill is acting on

  @rule:skills-act-on-the-session-repository @planned
  Rule: Every repository-scoped action targets the repository the session is working in

    Example: the plugin's own checkout is on disk and is not the subject
      Given a consuming repository with the plugin installed
      And the plugin's own repository is also on disk and reachable
      When a skill files, lists or reads anything repository-scoped
      Then it acts on the consuming repository
      And the plugin's own repository is not treated as a target

    Example: the two are the same repository
      Given somebody working inside the plugin's own repository
      When a skill files something
      Then it acts on that repository
      And nothing about the rule requires the two to be different places

  @rule:plugin-reports-reach-the-plugin @planned
  Rule: A report the human says is about the plugin goes to the plugin's tracker

    Example: the complaint is about a skill rather than the app
      Given somebody working in a consuming repository
      When they report that a skill itself behaved wrongly
      Then what is filed reaches the plugin's tracker
      And the reply says that is where it went

  @rule:an-unstated-subject-is-asked-about @planned
  Rule: Where the subject is genuinely undecided, it is asked about rather than picked

    Example: plugin behaviour reported without saying where it belongs
      Given a report that could be about the consuming repository or about the plugin
      When the skill cannot tell which from what was said
      Then it asks which one before filing
      And nothing has been filed in either place

  @rule:the-target-is-named-before-filing @planned
  Rule: The repository being filed into is named before anything is created

    Example: the target is stated where the human will see it
      Given a skill about to file
      When it reports what it is going to do
      Then the repository it will file into is named
      And a wrong target can be corrected before it becomes an issue somewhere

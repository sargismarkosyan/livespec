@feature:setup-boundary-binding @workflow:adopt-the-process
Feature: What the app talks to, and how a test here reaches it

  @rule:setup-asks-what-the-app-talks-to
  Rule: What the app talks to, and which of those a test here can reach for real, is asked of the human and never derived from the tree

    Example: the tests already stand in for the store and the payment provider
      Given a consuming repository whose behaviour tests run over a stand-in for its store and a stand-in for its payment provider
      When the process is being set up in it
      Then what the app talks to is asked before any row about it is written
      And for each, reaching the real thing from a session here is what gets recommended

    Example: the tree does not show everything the app talks to
      Given a consuming repository whose app sends mail from a scheduled job the tests never reach
      When the human names it in answer
      Then it has a row in the bindings like every other boundary
      And nothing in the row was inferred from what the tree happened to show

  @rule:a-real-row-is-written-after-a-test-reached-it
  Rule: A row reads real only once a test in this repository has reached the thing from here, and reads unreachable, with why, where none could

    Example: the store starts here and a test runs through it
      Given a consuming repository whose store the suite can start from the session by itself
      When the row for the store is written
      Then it reads real
      And it names what starts the store here

    Example: nothing here can start the thing
      Given a consuming repository whose payment provider cannot be reached from where the session is standing
      When the row for it is written
      Then it does not read real
      And it reads unreachable, with why, and what would make it reachable

  @rule:a-stand-in-nobody-chose-is-not-written-as-chosen
  Rule: A stand-in nothing checks is written as mocked, dated from the sitting, on a repository that already has tests, and is not offered at all on one that has none

    Example: an occupied repository whose tests run over an in-memory store
      Given a consuming repository whose behaviour tests already run over an in-memory stand-in for its store
      And nothing checks that stand-in against the real store
      When the row for the store is written
      Then it reads mocked, since this sitting
      And it names the larger test that covers the path, or says there is none

    Example: a fresh repository with nothing to test yet
      Given a consuming repository with no tests and no application code
      When the rows are written
      Then no row reads mocked
      And the states offered are real, fake with a suite against the real thing, and unreachable

    Example: a stand-in something checks
      Given a consuming repository whose stand-in for its store has a suite that also runs against the real store
      When the row for the store is written
      Then it reads fake
      And it says when that suite was last green against the real thing

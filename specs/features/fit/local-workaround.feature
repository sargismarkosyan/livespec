@feature:fit-local-workaround @workflow:adopt-the-process
Feature: A workaround kept because of a gap owned somewhere else

  @rule:a-workaround-records-what-would-end-it
  Rule: Work that carries on around a gap owned elsewhere is recorded in the bindings, naming what would end it

    Example: the process does not fit and the work continues anyway
      Given a consuming repository where the process assumes something that is not true here
      And the mismatch has been filed where it can be fixed for everyone
      When the repository goes on doing it its own way instead
      Then the bindings record what is being done here instead
      And they name the filed mismatch that would end it

    Example: the row is said before it is written
      Given a session about to record a workaround in the bindings
      When it reports what it is going to do
      Then the row it will write is in the reply
      And a wrong one can be corrected before it is in the file

    Example: nothing could be filed from this session
      Given a repository about to carry on around a gap
      And the report of that gap could not be filed from where the session is standing
      When the workaround is recorded
      Then the row is written now, naming the report that was handed over
      And it does not wait for a number nobody here can create

    Example: nothing is being worked around
      Given a mismatch filed where it can be fixed for everyone
      When the repository is not carrying on around it
      Then no row is recorded
      And the bindings do not become a list of what is outstanding elsewhere

  @rule:a-recorded-workaround-is-not-followed-silently
  Rule: A workaround the bindings record is never followed without saying so, and without saying what would end it

    Example: the reason has gone and nothing had said so
      Given a consuming repository whose bindings record a workaround
      And the mismatch it names has since been fixed
      When a session reaches the tracker that mismatch was filed in
      Then it says the workaround's reason has gone
      And it names what the repository can stop carrying

    Example: the reason is still there
      Given a consuming repository whose bindings record a workaround
      And the mismatch it names is still open
      When a session follows that workaround
      Then it says once that it is following it
      And nobody is asked to decide anything about it

    Example: the tracker that would answer it cannot be reached from here
      Given a consuming repository whose bindings record a workaround
      When the session cannot reach the tracker that workaround names
      Then it says which workaround it could not check
      And what to run to check it is in the reply

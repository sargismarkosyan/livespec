@feature:setup-what-a-pull-request-closes @workflow:adopt-the-process
Feature: What a pull request will close, read back from the platform it is on

  @rule:the-closing-read-back-is-bound @crosses:consuming-repository
  Rule: The bindings name the command that reads back which issues a pull request will close, taken from the platform the repository is on and watched listing one before it is written, never another platform's command

    Example: the repository is not on GitHub
      Given a consuming repository whose merge requests are on a forge other than GitHub
      When the sitting writes the row
      Then it names that forge's own read-back
      And no GitHub command appears in it

    Example: the command is watched before it is written
      Given a merged merge request whose description named an issue
      When the sitting reads it back with the forge's command
      Then the row carries the date it was watched listing an issue
      And the merge requests whose read-back is empty are named, with the line that closed nothing

    Example: a merge here closes nothing
      Given a repository whose issues live on another host than its pull requests
      When the row is written
      Then it reads not applicable, decided, with that as the reason
      And issues are closed by hand

  @rule:the-loop-reads-back-what-a-pull-request-closes
  Rule: The context file's loop step that opens the pull request writes the keyword straight before a bare reference, reads back what the pull request will close with the command the bindings name, and fixes a line the platform did not register before handing the pull request back

    Example: a loop that links every reference
      Given a context file whose loop opens the merge request with the keyword in front of a Markdown link to the issue
      When the file is read against the requirements
      Then that step is reported stale
      And the step as rewritten puts the keyword straight before a bare reference or the issue's full URL
      And it reads back what the merge request will close, with the command the bindings name

    Example: an empty list is fixed before the hand-back
      Given a merge request whose read-back lists no issue though its description names one
      When the step that opened it hands it back
      Then the closing line has been rewritten and read again, and the issue is listed

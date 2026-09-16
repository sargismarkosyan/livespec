@feature:audit-the-tool @workflow:adopt-the-process
Feature: The part of an audit a script does, and what it must never do

  @rule:a-check-a-script-can-answer-is-answered-by-a-script
  Rule: Every check that reads only the record is answered by the tool, the same way every time, from the record and never from the product

    Example: the same ledger twice
      Given a consuming repository's bindings
      When the tool reads them twice
      Then the lines it answers are identical both times

    Example: the kind of repository does not reach the tool
      Given a monorepo, a terminal application, a browser application and a repository with no application at all
      And each has bindings written from the template
      When the tool reads each
      Then it opens the bindings, the record, the spec tree's listing and the plugin's own files
      And nothing under the application's source

  @rule:the-tool-runs-nothing-it-read @refusal
  Rule: The tool executes no command whose text came from the bindings, the record or any file it read; what it prints on a judgment line is for a mind to run

    Example: a command planted in a bindings cell
      Given bindings whose traceability row carries a command that would leave a mark if run
      When the tool reads the bindings and validates a record
      Then no mark is left
      And the command appears on the judgment line as text

  @rule:a-judgment-line-arrives-with-its-command
  Rule: For every check a script cannot answer, the tool writes the id, the question and the command the bindings name, and the line reads unanswered until a mind replaces it

    Example: the platform's answer is not in the tree
      Given a ledger row about branch protection carrying how it was read back
      When the tool reads the bindings
      Then the line for that check reads unanswered, with that command beside it

    Example: the row names no command
      Given a ledger row about something outside the tree that names no way to read it
      When the tool reads the bindings
      Then the line reads unanswered and says the row must name one
      And the audit cannot end until it does

  @rule:the-outcome-is-readable-from-the-exit-alone
  Rule: The tool's exit says which of three things happened, and never that a bill is owed

    Example: the ordinary run
      Given bindings the tool can read
      When it prints the record
      Then it exits as a success, whether or not any line is open

    Example: no bindings at all
      Given a repository that has never had the process set up
      When the tool is run in it
      Then it exits distinctly, saying so in one line, and offers the sitting

    Example: a record it will not accept
      Given a record with a line missing
      When the tool validates it
      Then it exits as a refusal, naming the line

  @rule:every-mechanical-check-is-proven-to-fire
  Rule: Every check the tool answers is broken on purpose in this repository's fixture, and a check no fault flips is red here

    Example: a fault per check
      Given the fixture filled green
      When each fault in the table is applied to a fresh copy
      Then exactly the line that fault targets turns open

    Example: a check nobody has made fail
      Given a check the tool answers that no fault in the table flips
      When this repository is verified
      Then verification is red, naming the check

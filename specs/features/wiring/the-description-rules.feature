@feature:wiring-the-description-rules @workflow:adopt-the-process
Feature: The repository holds how its pull request descriptions are written

  @rule:the-description-rules-are-the-repositorys-own
  Rule: The bindings name the file holding how a pull request description is written in this repository, the file is there, and the context file links it; where all three hold, the file is read against the plugin's guideline as it now stands

    Example: a repository set up before the rules had a file
      Given bindings with no *Pull request description rules* row
      When the wiring is audited
      Then the rules are reported open, for the sitting to write from the plugin's template

    Example: a file the context file never points at
      Given bindings naming specs/setup/pull-requests.md, which is there
      And a context file that does not link it
      When the wiring is audited
      Then the rules are reported open: an agent that never loads the plugin would never find them

    Example: rules that are there
      Given the row, the file, and the context file's link
      When the wiring is audited
      Then the file is put to a reading against the guideline, not marked clear by the script

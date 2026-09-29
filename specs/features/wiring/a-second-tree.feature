@feature:wiring-a-second-tree @workflow:adopt-the-process
Feature: What an audit reads back about a second tree

  @rule:a-fresh-tree-row-is-there @planned
  Rule: The audit tool reports bindings with no row saying what readies a fresh tree as open, and hands the command it names to the reading

    Example: bindings written before the row existed
      Given bindings with no row for a fresh tree
      When the audit tool reads them
      Then the fresh-tree row line reads open, with the setup sitting as what closes it

    Example: the row is there
      Given bindings whose fresh-tree row names a command
      When the audit tool reads them
      Then the fresh-tree row line reads clear
      And the fresh-tree line after it is printed unanswered, carrying that command

  @rule:a-fresh-tree-is-re-proven @planned
  Rule: The audit readies a throwaway tree with the command the bindings name, runs verification there and removes it, and changes nothing but the record

    Example: an install step was added and the command never learned it
      Given bindings saying one command readies a fresh tree
      And a step a fresh tree now needs that the command does not take
      When the audit readies a throwaway tree with it
      Then the line reads open, with the first failing line of verification
      And the command itself is left as it was

    Example: the secrets cannot be reached from this session
      Given the command reads a key from a place this session cannot open
      When the audit tries it
      Then the line reads not-read, with why
      And the row is not corrected on that evidence alone

    Example: the audit is over
      Given the audit has finished with the throwaway tree
      When the working tree and the worktree list are read
      Then neither holds anything the audit left behind

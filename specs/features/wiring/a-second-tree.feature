@feature:wiring-a-second-tree @workflow:adopt-the-process
Feature: What an audit reads back about a second tree

  @rule:the-trees-row-is-there @planned
  Rule: The audit tool reports as open bindings with no row saying where trees live and what makes them, or a context file whose commands do not carry that command, and hands the command to the reading

    Example: bindings written before the row existed
      Given bindings with no row for trees
      When the audit tool reads them
      Then the trees row line reads open, with the setup sitting as what closes it

    Example: the row is there
      Given bindings whose trees row names a directory and a command
      And a context file whose block of commands carries it
      When the audit tool reads them
      Then the trees row line reads clear
      And the fresh-tree line after it is printed unanswered, carrying that command

    Example: the context file never learned the command
      Given bindings whose trees row names a command
      And a context file whose block of commands does not carry it
      When the audit tool reads them
      Then the trees row line reads open, naming the context file as what to correct

  @rule:a-fresh-tree-is-re-proven @planned
  Rule: The audit makes a throwaway tree with the command the bindings name, runs verification there and cleans it with the same command, and changes nothing but the record

    Example: an install step was added and the command never learned it
      Given bindings saying one command makes a fresh tree
      And a step a fresh tree now needs that the command does not take
      When the audit makes a throwaway tree with it
      Then the line reads open, with the first failing line of verification
      And the command itself is left as it was

    Example: the secrets cannot be reached from this session
      Given the command reads a key from a place this session cannot open
      When the audit tries it
      Then the line reads not-read, with why
      And the row is not corrected on that evidence alone

    Example: the audit is over
      Given the audit has finished with the throwaway tree
      When the working tree and the repository's list of trees are read
      Then neither holds anything the audit left behind

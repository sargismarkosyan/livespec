@feature:setup-a-second-tree @workflow:adopt-the-process
Feature: A second tree as ready as the first

  @rule:trees-have-one-home-and-one-command
  Rule: The bindings name one directory every tree lives in and one command that makes, lists and cleans them, and where there is none the sitting offers to write it and waits

    Example: a fresh tree needs an install, a hook and an env file
      Given a repository where a new worktree needs its packages installed, its hook turned on and an env file before verification passes
      When the sitting reaches the bindings
      Then a command that makes, lists and cleans trees is offered, with what it would write and where the trees would live
      And nothing is written while the offer is unanswered

    Example: the offer is declined
      Given the offer has been made
      When it is turned down
      Then the bindings row lists the steps a fresh tree needs, in order, and the one directory trees go in

    Example: every session is told the command
      Given the command exists
      When the context file is written
      Then its block of commands carries the command that makes a tree
      And no harness's name is needed to find it

    Example: the agent harness has its own way of making trees
      Given a harness that runs its own setup when it creates a tree
      When the command exists
      Then the harness's setup calls the command rather than carrying a second copy of its steps
      And nothing in the bindings or the command names that harness

  @rule:a-fresh-tree-is-watched-going-green
  Rule: Before the row is written, a throwaway tree is made by that command and runs verification — and the app beside the first tree's, where there is one — and is cleaned by it

    Example: the throwaway tree goes green
      Given the command the bindings will name
      When a throwaway tree is made with it and verification is run there
      Then the row carries the date it went green
      And the command's own clean leaves the tree list as it was

    Example: the app runs beside the first tree's
      Given a repository with its app already running in the first tree
      When the throwaway tree starts its own
      Then both are up at once, or the row says what they fought over

    Example: the hook is on in the first tree and off in the throwaway one
      Given the first tree runs the checks before every push
      And the throwaway tree made by the command does not
      When the proof is read
      Then the row does not say a fresh tree works
      And the hand-back names what the command left out

    Example: the first tree's tests walk into the throwaway one
      Given trees live in a directory inside the repository
      When verification in the first tree runs while the throwaway tree exists
      And it reports more tests than it did without it
      Then the row does not say a fresh tree works
      And the hand-back names the tool that needs the directory excluded

    Example: the fresh tree needs a secret this session cannot reach
      Given verification in a fresh tree reads a key from a place this session cannot open
      When the proof is attempted
      Then the row says the fresh tree is unproven, and why

  @rule:clean-removes-only-what-is-safe
  Rule: Cleaning removes every tree with nothing to lose, with its branch and whatever it held on its own, and lists every other tree with why it was kept

    Example: most trees are merged and clean
      Given eighteen trees, seventeen of them clean with every commit on the main branch
      When the trees are cleaned
      Then the seventeen are gone, and their local branches with them
      And the eighteenth is listed with its uncommitted files as the reason it stayed

    Example: a tree the harness made somewhere else
      Given a tree created by an agent harness outside the directory the bindings name
      When the trees are listed
      Then it is listed with the others, from the repository's own record of its trees

    Example: a tree that held its own database and port
      Given a clean, merged tree whose command made it a database on the shared server and gave it a port
      When the trees are cleaned
      Then its database is dropped and whatever it started is stopped
      And the shared server stays up for the other trees

    Example: the tree somebody is working in
      Given a session standing in a clean, merged tree
      When the trees are cleaned from it
      Then that tree is kept, and the list says it is the current one

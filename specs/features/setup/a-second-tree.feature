@feature:setup-a-second-tree @workflow:adopt-the-process
Feature: A second tree as ready as the first

  @rule:trees-have-one-home-and-one-command @planned
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

    Example: the agent harness has its own way of making trees
      Given a harness that runs its own setup when it creates a tree
      When the command exists
      Then the harness's setup calls the command rather than carrying a second copy of its steps
      And nothing in the bindings or the command names that harness

  @rule:a-fresh-tree-is-watched-going-green @planned
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

  @rule:what-two-trees-fight-over-is-derived @planned
  Rule: What two trees would contend for is worked out per tree by the command and named in the bindings, never typed into each tree by hand

    Example: the app listens on a port written in its env file
      Given an app whose port is a line in its env file
      When the command makes a second tree
      Then the second tree's port is worked out from that tree
      And the bindings name the port as something each tree has its own of

    Example: the port is fixed in the app's code
      Given an app that listens on a port nothing outside its code can change
      When the command is written
      Then the bindings name the port as a collision only the app can remove
      And the hand-back says that change is the person's to file, not the sitting's to make

  @rule:a-shared-secret-has-one-source @planned
  Rule: What every tree shares comes from one source outside every tree's history, stays ignored in every tree it reaches, and is never committed

    Example: one env file holds a key and a port
      Given an env file holding an API key and the port the app listens on
      When the command is written
      Then the key comes from the one source every tree reads
      And the port is the tree's own

    Example: the copy would show up as a file to add
      Given the command copies the env file into a fresh tree
      When the fresh tree's status is read
      Then the env file is not in it, or the command is not written as working

  @rule:clean-removes-only-what-is-safe @planned
  Rule: Cleaning removes every tree with nothing to lose, with its branch, and lists every other tree with why it was kept

    Example: most trees are merged and clean
      Given eighteen trees, seventeen of them clean with every commit on the main branch
      When the trees are cleaned
      Then the seventeen are gone, and their local branches with them
      And the eighteenth is listed with its uncommitted files as the reason it stayed

    Example: a tree the harness made somewhere else
      Given a tree created by an agent harness outside the directory the bindings name
      When the trees are listed
      Then it is listed with the others, from the repository's own record of its trees

    Example: the tree somebody is working in
      Given a session standing in a clean, merged tree
      When the trees are cleaned from it
      Then that tree is kept, and the list says it is the current one

@feature:setup-a-second-tree @workflow:adopt-the-process
Feature: A second tree as ready as the first

  @rule:a-fresh-tree-is-one-command @planned
  Rule: The bindings name the one command that readies a fresh tree, and where it takes more than one step the sitting offers to write it and waits

    Example: a fresh tree needs an install, a hook and an env file
      Given a repository where a new worktree needs its packages installed, its hook turned on and an env file before verification passes
      When the sitting reaches the bindings
      Then a script doing those three things is offered, with what it would write
      And nothing is written while the offer is unanswered

    Example: the offer is declined
      Given the offer has been made
      When it is turned down
      Then the bindings row lists the steps in the order a fresh tree needs them
      And no script is written

    Example: a fresh checkout runs as it stands
      Given a repository whose verification passes in a new worktree with nothing done to it
      When the bindings are written
      Then the row says nothing is needed, and when that was watched

  @rule:a-fresh-tree-is-watched-going-green @planned
  Rule: Before the row is written, a throwaway tree is readied by that command and runs verification — and the app beside the first tree's, where there is one — and is removed

    Example: the throwaway tree goes green
      Given the command the bindings will name
      When a throwaway worktree is readied with it and verification is run there
      Then the row carries the date it went green
      And the throwaway tree is gone from the worktree list

    Example: the app runs beside the first tree's
      Given a repository with its app already running in the first tree
      When the throwaway tree starts its own
      Then both are up at once, or the row says what they fought over

    Example: the hook is on in the first tree and off in the throwaway one
      Given the first tree runs the checks before every push
      And the throwaway tree readied by the command does not
      When the proof is read
      Then the row does not say a fresh tree works
      And the hand-back names what the command left out

    Example: the fresh tree needs a secret this session cannot reach
      Given verification in a fresh tree reads a key from a place this session cannot open
      When the proof is attempted
      Then the row says the fresh tree is unproven, and why
      And no date is written beside the command

  @rule:what-two-trees-fight-over-is-derived @planned
  Rule: What two trees would contend for is worked out per tree by the command and named in the bindings, never typed into each tree by hand

    Example: the app listens on a port written in its env file
      Given an app whose port is a line in its env file
      When the command readies a second tree
      Then the second tree's port is worked out from that tree
      And the bindings name the port as something each tree has its own of

    Example: the port is fixed in the app's code
      Given an app that listens on a port nothing outside its code can change
      When the command is written
      Then the bindings name the port as a collision only the app can remove
      And the hand-back says that change is the person's to file, not the sitting's to make

    Example: nothing is contended for
      Given a repository with no app and no local store
      When the bindings are written
      Then the row says what the trees share anyway, or that they share nothing

  @rule:a-shared-secret-is-pointed-at @planned
  Rule: What every tree shares comes from one place each tree points at, is never copied into a tree, and is never committed

    Example: one env file holds a key and a port
      Given an env file holding an API key and the port the app listens on
      When the command is written
      Then the key is read from one place every tree points at
      And the port is the tree's own

    Example: the only copy is an ignored file in the first tree
      Given the secrets live in an ignored file in the first tree and nowhere else
      When the command readies a fresh tree
      Then the fresh tree points at that one file rather than holding a copy of it
      And nothing in the fresh tree's status offers it as a file to add

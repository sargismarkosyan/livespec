@feature:setup-what-trees-share @workflow:adopt-the-process
Feature: What each tree has of its own, and what every tree shares

  @rule:every-resource-is-own-or-shared @planned
  Rule: Every resource a tree touches is written in the bindings as the tree's own, as shared and started once, or as shared and contended with the decision and its reason

    Example: two builds of the app and one port
      Given an app that listens on a port
      When a second tree runs its own build beside the first
      Then each tree has its own port
      And the bindings name the port as something each tree has its own of

    Example: one database server, several trees
      Given an app that needs a database server, started in a container
      When a second tree is made
      Then no second server is started
      And the tree gets a database of its own on the server already running, made by the command

    Example: trees write the same development database on purpose
      Given trees that share one database and whose writes can collide
      When the person says that is acceptable here
      Then the bindings name the database as shared and contended, decided, with the reason
      And it is not listed as a collision to fix

    Example: names the runtime hands out
      Given containers, queues or cache keys named the same in every tree
      When a second tree starts its own
      Then each name carries the tree's name, or the resource is written down as shared

    Example: the port is fixed in the app's code
      Given an app that listens on a port nothing outside its code can change
      When the command is written
      Then the bindings name the port as a collision only the app can remove
      And the hand-back says that change is the person's to file, not the sitting's to make

  @rule:one-env-file-configures-a-tree @planned
  Rule: Everything a tree varies is read from one env file, which the command copies from one source outside every tree's history, adjusts only in the lines each tree has of its own, keeps ignored, and never commits

    Example: a fresh tree's env file
      Given a source env file holding an API key, a database name and a port
      When the command makes a fresh tree
      Then the tree's env file is that source with only the database name and the port changed
      And the key is as the source has it

    Example: the port is derived, not chosen at start
      Given three trees made one after another
      When the trees are listed
      Then each shows the port written in its own env file, and no two are the same

    Example: the copy would show up as a file to add
      Given the command copies the env file into a fresh tree
      When the fresh tree's status is read
      Then the env file is not in it, or the command is not written as working

    Example: a setting the app reads from somewhere else
      Given a data directory the app reads from a path written in its code
      When the command is written
      Then the bindings name it as a setting only the app can move into the env file

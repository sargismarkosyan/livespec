@feature:wiring-context-file @workflow:adopt-the-process
Feature: What the build refuses about the file every session reads first

  @rule:a-context-file-past-its-ceiling-fails-the-build @planned
  Rule: A CLAUDE.md larger than the ceiling its own bindings name fails verification, and a context file with no ceiling row fails it too

    Example: the file has grown past the number
      Given a consuming repository whose bindings set the ceiling at the size the file was
      When a change makes CLAUDE.md larger than that number
      Then verification fails, naming the file's size and the bindings' number

    Example: the number is raised in the same change
      Given a change that makes CLAUDE.md larger than the ceiling
      When the same change raises the number in the bindings, with the reason beside it
      Then verification passes
      And the raise is in the diff beside the growth

    Example: a number nobody wrote is not a pass
      Given a consuming repository with a CLAUDE.md and no ceiling row in its bindings
      When verification runs
      Then it fails, saying the row is missing rather than passing the file unmeasured

  @rule:a-context-file-without-its-shape-fails-the-build @planned
  Rule: A CLAUDE.md that is missing, or that carries no loop, no commands, or no pointer to the bindings, fails verification

    Example: three lines pass nothing
      Given a consuming repository whose CLAUDE.md is a title and one sentence
      When verification runs
      Then it fails, naming what is missing: the loop, the commands, and the pointer to the bindings

    Example: a loop of nine steps
      Given a CLAUDE.md whose loop is a numbered list of nine steps
      When verification runs
      Then it fails, naming the length and the eight the method allows

    Example: no file at the root
      Given a consuming repository with the process set up and no CLAUDE.md at the root
      When verification runs
      Then it fails

  @rule:what-only-a-mind-can-read-is-left-to-the-sitting @planned @refusal
  Rule: The gate reads nothing a script cannot decide — a stale pointer, a copied paragraph, an aspirational rule pass it, and are read by the sitting and the audit

    Example: a file in shape, with a pointer that has gone stale
      Given a CLAUDE.md within its ceiling, with its loop, its commands and its pointer to the bindings
      And a paragraph in it copied from the plugin, and a path in it that has since moved
      When verification runs
      Then it passes
      And neither the copy nor the stale path is reported by the gate

  @rule:the-sitting-wires-the-context-file-check @planned
  Rule: The sitting wires the context-file check into the repository's own gate, beside the shape checks over the spec layer, and the file it leaves behind passes it

    Example: an occupied repository with a thin file
      Given a consuming repository whose existing CLAUDE.md is a title, a test command and a branch convention
      When the process is set up in it
      Then the gate the sitting writes reads CLAUDE.md for its ceiling and its shape
      And the fault record it leaves lists the faults that prove that gate fires
      And the CLAUDE.md the sitting leaves behind passes the gate it wired

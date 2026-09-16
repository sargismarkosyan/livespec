@feature:setup-rewriting-the-context-file @workflow:adopt-the-process
Feature: What the sitting does with a CLAUDE.md that is out of line

  @rule:a-file-out-of-line-is-offered-whole
  Rule: When the reading finds a requirement missing, or anything the method rules out, the sitting offers the file rewritten from the requirements and shown whole — whatever the file is currently worth — and repairs a line only where a line is the whole finding

    Example: a filled template with the plugin's rules copied into it
      Given a consuming repository whose CLAUDE.md was assembled from somebody else's blanks and carries the loop and the rules copied from the plugin
      When the sitting reads it against the requirements
      Then what it offers is a new file, shown whole
      And not a list of edits to the one that is there

    Example: eight of ten met is not an argument for the shape
      Given a CLAUDE.md that meets eight requirements and carries a paragraph the method rules out
      When the sitting reads it against the requirements
      Then the rewrite is offered all the same
      And the file's current worth is reported, not counted as a reason to patch

    Example: the only finding is a path that moved
      Given a CLAUDE.md that meets every requirement, with one pointer at a directory that has since moved
      When the sitting reads it against the requirements
      Then the line is corrected
      And no rewrite is offered

  @rule:what-only-the-file-knows-survives-the-rewrite
  Rule: Before a rewrite is shown, every fact only the existing file carries is listed, and each is in the new file or named as dropped with the reason

    Example: the paragraph that stops the next wrong argument
      Given a CLAUDE.md out of line in most of its requirements, with a dated account of where it runs that still binds every new route
      When the rewrite is shown
      Then that account is listed as harvested before the new file is written
      And it reads in the new file, with its date and what was argued from it

    Example: what was dropped is named
      Given a harvested fact the new file does not carry
      When the rewrite is shown
      Then the fact is named as dropped, with the reason and where it goes instead

  @rule:a-rewrite-lands-only-on-a-yes @refusal
  Rule: A rewrite is shown whole and waits; a yes given at the start of the sitting does not cover replacing a file somebody wrote by hand, and nothing is written to it before the answer

    Example: the sitting was told to go ahead at the start
      Given a sitting that was told to write files as it goes
      And a CLAUDE.md written by hand that the reading found out of line
      When the rewrite is ready
      Then it is shown whole, with what was kept and what was dropped, and the sitting waits
      And the file on disk is as it was until the answer comes

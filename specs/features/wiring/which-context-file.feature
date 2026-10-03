@feature:wiring-which-context-file @workflow:adopt-the-process
Feature: The gates and the audit read the context file the repository has

  @planned @rule:the-context-file-is-the-one-the-repository-has
  Rule: The context-file gates and the audit read the file the bindings name as the context file, or where they name none, the first of AGENTS.override.md, AGENTS.md and CLAUDE.md that exists, and every line they print names the file they read

    Example: a repository whose only instructions file is AGENTS.md
      Given a repository with AGENTS.md at its root and no CLAUDE.md
      And bindings that name no context file
      When verification and the audit run
      Then both read AGENTS.md, its ceiling, its loop, its commands and its pointer to the bindings
      And no line says there is no context file

    Example: the bindings name the file
      Given bindings whose context file row names CLAUDE.md
      And a repository holding both AGENTS.md and CLAUDE.md
      When verification runs
      Then it reads CLAUDE.md, and says it did

    Example: a ceiling row written before the rename
      Given bindings whose ceiling row is still labelled CLAUDE.md ceiling
      When verification runs
      Then the row is read as the context file's ceiling, and nothing fails for the label

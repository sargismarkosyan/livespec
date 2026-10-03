@feature:setup-which-context-file @workflow:adopt-the-process
Feature: The sitting writes or audits the context file the repository already has

  @planned @rule:the-sitting-names-the-context-file
  Rule: The sitting reads which instructions file the repository's harnesses already read, writes or audits that one, names it in the bindings, and never creates a second file beside it

    Example: a repository that keeps one AGENTS.md
      Given a repository with AGENTS.md and no CLAUDE.md
      When the sitting reaches the context file
      Then it audits AGENTS.md against the requirements
      And the bindings' context file row names AGENTS.md
      And no CLAUDE.md is created, not even one line pointing at the other

    Example: a repository with neither
      Given a repository with no instructions file
      When the sitting reaches the context file
      Then it asks which name the harnesses in use read, recommending one, before writing either

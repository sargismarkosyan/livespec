@feature:audit-the-list @workflow:adopt-the-process
Feature: The list of checks an audit is held to, and the ids that make it one list

  @rule:every-check-has-a-permanent-id
  Rule: Every check an audit makes, and every gate a ledger needs a row for, has an id in the method that is never renamed and never reused

    Example: the ids are one table
      Given the method names the checks an audit makes and the gates a ledger carries
      When the table is read
      Then each has an id, a kind, the version it arrived in and a severity
      And nothing an audit checks is enumerated anywhere else

    Example: a retired check keeps its row
      Given a check retired in a later version of the plugin
      And a consuming repository whose ledger still carries a row for it
      When the wiring is audited
      Then the row is reported as retired since that version, with what replaced it
      And never as an id nobody knows

    Example: a rename is a retirement and a new id
      Given a check whose name the method wants to change
      When the change is made
      Then the old id is retired in place and names the new one
      And no row in any consuming repository stops resolving

  @rule:the-table-and-the-tool-agree
  Rule: The list the method publishes and the checks the tool performs are held equal by this repository's own checks, so drift fails here and never in a consuming repository

    Example: a check added to the tool and not the table
      Given a check the tool performs that the table does not name
      When this repository is verified
      Then verification is red, naming the id

    Example: a version the changelog does not have
      Given an id whose arrival or retirement names a version
      And the changelog has no entry for that version
      When this repository is verified
      Then verification is red

  @rule:a-repository-may-add-rows-of-its-own
  Rule: A ledger row for a gate the method does not name carries the local prefix, is held to the same states as any row, and is required by nothing

    Example: a repository's own gate
      Given a consuming repository whose ledger carries a row for a gate this method never named
      And the row carries the local prefix and a legal state
      When the wiring is audited
      Then the row is read like any other
      And no row is asked for that the repository did not add

    Example: a row with no prefix at all
      Given a ledger row naming neither a gate id nor a local one
      When the wiring is audited
      Then the row is reported as unmatched, with the candidates the labels suggest

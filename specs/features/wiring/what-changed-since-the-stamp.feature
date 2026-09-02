@feature:wiring-what-changed-since-the-stamp @workflow:adopt-the-process
Feature: What an audit reads for between the ledger's stamp and the plugin installed

  @rule:the-entries-between-are-where-to-look @planned
  Rule: What the method changed between the stamp and the plugin installed is read from the changelog the plugin ships, and each entry says where to look rather than what to do

    Example: the stamp is several releases behind the plugin installed
      Given a consuming repository whose ledger is stamped several releases behind the plugin installed
      When the wiring is audited
      Then every entry after the stamp, up to and including the one for the plugin installed, is read
      And what each asks of this repository is read from the method and the skill as they now stand, not from the entry

    Example: an entry is mostly the reasoning for a change
      Given an entry in that range that spends its length on why rather than on what
      When the wiring is audited
      Then nothing is asked of the repository that the method as it now stands does not ask
      And the entry is not repeated back as a list of tasks

    Example: an entry moved nothing this repository holds
      Given an entry in that range that changed only how this plugin measures itself
      When the wiring is audited
      Then the entry is passed over in a line saying so
      And no finding is reported for it

  @rule:a-range-with-nothing-in-it-is-said-not-computed @planned
  Rule: A stamp at the plugin installed, a stamp ahead of it, and a changelog that cannot be reached are each said in a line

    Example: the ledger is stamped at the plugin installed
      Given a consuming repository whose ledger is stamped at the version of the plugin installed
      When the wiring is audited
      Then it reports that there is nothing between the stamp and the plugin installed to reconcile
      And no empty finding stands in for that

    Example: the stamp is ahead of the plugin installed
      Given a consuming repository whose ledger is stamped at a version later than the plugin installed
      When the wiring is audited
      Then both versions are named and the stamp is reported as ahead of what is installed
      And no range is read

    Example: the changelog cannot be reached from here
      Given a session in which the plugin's changelog cannot be read
      When the wiring is audited
      Then that is said once, with what would read it
      And the rest of the ledger is audited as it would have been

  @rule:a-reading-leaves-the-stamp-where-it-was @planned @refusal
  Rule: The stamp follows the wiring and never the reading

    Example: the reading corrected only the record
      Given a reading of the range that found the record behind and the wiring as the method now asks
      When the audit makes its corrections
      Then the stamp is left where it was

    Example: the reading found wiring the method now asks for and the repository lacks
      Given a reading of the range that found a gate demanding what the method no longer asks it to
      When the audit makes its corrections
      Then the stamp is left where it was
      And the ledger does not read as level with the plugin installed

  @rule:what-the-reading-finds-is-corrected-as-record-or-written-as-a-row @planned
  Rule: What the reading finds is corrected in place where it is record — the bindings and CLAUDE.md — and becomes a deferred row where it is wiring, never wired by the audit

    Example: an entry moved something the repository's CLAUDE.md is required to carry
      Given an entry in that range that changed what a step of the loop must say
      And the repository's CLAUDE.md still reads as it did before
      When the audit makes its corrections
      Then CLAUDE.md is corrected in place, shown as it will read
      And it is not handed back as a line for setup to write

    Example: an entry renamed a skill
      Given an entry in that range that renamed a skill
      And the repository's record still instructs by the old name in more than one place
      When the audit makes its corrections
      Then every instruction that names it by the old name is corrected in place
      And a dated account of what once ran under the old name is left as written

    Example: an entry moved what a gate is asked to demand
      Given an entry in that range that changed what a gate should demand
      And the config that gate reads still demands what it did before
      When the audit makes its corrections
      Then the row for that gate reads deferred, naming the version of the method that moved it
      And the config is left as it was, and the report ends by naming setup with that row

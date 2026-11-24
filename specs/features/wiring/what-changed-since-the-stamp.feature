@feature:wiring-what-changed-since-the-stamp @workflow:adopt-the-process
Feature: What an audit reads for between the ledger's stamp and the plugin installed

  @rule:the-entries-between-are-where-to-look
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

  @rule:the-plan-is-read-from-the-list
  Rule: What the plugin installed asks of a ledger is computed from the list of ids, never from the changelog: each gate or wiring id that arrived or was revised after its row's own version, each with no row, each retired id still carrying one, and each check that arrived or was revised after the release it was last answered at

    Example: a gate arrived after the row was reconciled
      Given a ledger whose rows were reconciled at a release before a gate arrived
      When the plan is asked for
      Then the gate is listed to be wired, with the release it arrived in
      And a row already level is not listed

    Example: a meaning moved under the same id
      Given a row reconciled before the release that revised its id
      When the plan is asked for
      Then the row is listed to be proven again, not to be wired

    Example: an id retired while its row stayed
      Given a row for an id the list has since retired, naming the command that ran it here
      When the plan is asked for
      Then the row is listed to be dropped, with that command and what replaced it
      And the item says the command, its fault and the prose describing it go in the same commit

  @rule:a-range-with-nothing-in-it-is-said-not-computed
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

  @rule:a-reading-leaves-the-stamp-where-it-was @refusal
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

  @rule:what-the-reading-finds-is-corrected-as-record-or-written-as-a-row
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
      And the config is left as it was, and the reply ends with the command that starts the sitting, with that row after it

    Example: the file is out of line beyond what a line corrects
      Given a repository's CLAUDE.md that reads as a filled template, with the plugin's own rules copied into it
      When the audit makes its corrections
      Then the lines that are record are corrected in place
      And the file is not rewritten by the audit: its line stays open, naming the rewrite as what closes it and the sitting as whose it is

  @rule:the-upgrade-is-a-transaction-on-file
  Rule: An upgrade is a transaction in a file the repository commits — opened from the plan with each item keyed by its id and the release that asked for it, the rows as they stood, and every check's last answer — so a sitting resumes from the file, a second is refused while one is open, and a newer plugin extends it

    Example: the plan opens a transaction
      Given a ledger behind the plugin installed
      When the plan is written
      Then the upgrade ledger holds each item pending, the rows as they stood, and the versions it runs from and to

    Example: a second sitting finds the first still open
      Given an open transaction to the plugin installed
      When the plan is written again
      Then it is refused, naming the transaction to resume

    Example: the plugin moved on during the transaction
      Given an open transaction to an older release than the plugin installed
      When the plan is written
      Then the new release's items are added and the transaction runs to the plugin installed

    Example: a check already answered is not asked again
      Given a check the upgrade ledger records as answered at the release that last changed it
      When the plan is read
      Then the check is not listed

  @rule:finalize-raises-what-was-answered
  Rule: Finalizing reads the record the last report wrote of that very commit, sends back to pending any answered row a row-level line still finds, raises each row left answered and never lowers one, records a check as answered only where its line reads clear or n/a, appends the sitting, and closes the transaction only when nothing is pending

    Example: everything answered
      Given a transaction whose gate was wired with its evidence and whose new check reads clear in the record
      When it is finalized
      Then the gate's row is raised to the release, the check is recorded as answered, and the transaction is closed

    Example: the record still finds the row
      Given a gate marked wired whose row a row-level line of the record still reports open
      When it is finalized
      Then the gate goes back to pending, its row keeps its version, and the sitting names it as left pending

    Example: the record is of another commit, or an answer has no evidence
      Given a transaction answered without evidence, or a record written before the last commit
      When it is finalized
      Then it is refused, saying which

  @rule:the-hint-is-the-persons-alone
  Rule: Where an upgrade is waiting in the repository a session opens, the person is shown one line saying so — this session's plugin is older than the ledger, items are pending, or a newer release exists — the model is never shown it, and nothing is shown with no bindings, with the hint turned off, or when reading fails

    Example: items are pending
      Given a ledger behind the plugin the session loads
      When the session starts
      Then the line counts the items pending and names the command that brings it up to date

    Example: the session's plugin is older than the ledger
      Given a ledger reconciled at a release newer than the plugin the session loads
      When the session starts
      Then the line says so before anything about pending items

    Example: a newer release, and nothing pending
      Given a level ledger and a cached newer release
      When the session starts
      Then the line names the release

    Example: nothing to say
      Given a repository with no bindings, or the hint turned off
      When the session starts
      Then nothing is shown

    Example: an extension that would reach the model
      Given a Pi extension in the plugin that sends a message into the session
      When verification runs
      Then it fails, naming the call

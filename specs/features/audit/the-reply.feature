@feature:audit-the-reply @workflow:adopt-the-process
Feature: What an audit says, generated from the record rather than remembered

  @rule:the-reply-is-generated-from-the-record
  Rule: What is open is listed in the order of the severity each id carries, then what was not read, then the decisions, and the reply is what the record says rather than what the session recalls

    Example: the dangerous thing first
      Given a record with a platform claim open, a boundary open and a deferral one change old
      When the reply is generated
      Then the platform claim is first, the boundary second, the deferral last

    Example: nothing open
      Given a record with no open line
      When the reply is generated
      Then it says what was read and what was decided
      And no line sends anybody to a sitting

  @rule:a-decided-exception-is-reported-once-and-never-relitigated
  Rule: A row marked as decided is listed among the decisions and never among the findings, the tree is not read against it, and a contradiction goes to a mind as evidence

    Example: a step this repository chose not to have
      Given a ledger row reading not applicable, marked decided, with its reason
      When the wiring is audited
      Then the row is listed once among the decisions
      And nothing about it is a finding

    Example: the tree disagrees with a decision
      Given a row decided as not applicable because a layer is unused
      And that layer has files in it
      When the wiring is audited
      Then the contradiction is written on a judgment line as evidence
      And it is not reported as open by the tool alone

    Example: a gap that nobody decided
      Given a ledger row reading not applicable with a reason and no mark of decision
      And the tree contradicts the reason
      When the wiring is audited
      Then the row is reported as open

  @rule:a-check-newer-than-the-stamp-is-reported-until-the-wiring-catches-up
  Rule: Every check that arrived after the ledger's stamp is reported as new, open where the ledger has no row for it, on every audit until the sitting brings the wiring level

    Example: a gate the method gained
      Given a ledger stamped at a version before a gate was added
      And the plugin installed is after it
      When the wiring is audited
      Then that gate is reported as arrived since the stamp and open for want of a row
      And the stamp is left where it was

    Example: a check whose meaning changed
      Given a row that was clear under the version the ledger is stamped against
      And the check that reads it has since changed
      When the wiring is audited
      Then the row is read under the check as it now stands
      And having been clear once is not offered as a reason to leave it

  @rule:the-tree-is-inventoried-and-the-rows-are-held-to-it
  Rule: The tool lists what the repository is made of — its manifests, its dependencies, its top-level packages — and writes the contradiction with a row on the judgment line that decides it

    Example: two languages and one coverage row
      Given a repository with two languages by its manifests
      And a coverage row naming one of them
      When the wiring is audited
      Then the judgment line for what the row leaves uncovered names the other language

    Example: a service no boundary names
      Given a repository whose dependencies reach a network service
      And a boundaries table with no row for the network
      When the wiring is audited
      Then the judgment line for the boundaries names the service

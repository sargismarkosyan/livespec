@feature:wiring-what-an-audit-reads @workflow:adopt-the-process
Feature: What an audit reads, and which version of the method it reads against

  @rule:a-number-is-read-where-the-gate-reads-it
  Rule: A number a gate enforces is read from the config the gate reads, and a demand set at what the code happened to score is reported as measured rather than chosen

    Example: the demand is the score the day the row was written
      Given a consuming repository whose row for coverage reads automated
      And the demand in the tool's own config is what the code scored the day that row was written
      When the wiring is audited
      Then the demand is read from the config the gate reads rather than from the row describing it
      And it is reported as a number that was measured rather than one somebody chose

    Example: the demand is the whole of what is in scope and the code reaches it
      Given a consuming repository whose coverage config demands the whole of what is in scope
      And the code covers the whole of it
      When the wiring is audited
      Then the demand is not reported as a number nobody chose
      And a figure matching the score because the scope is wholly covered is left alone

    Example: what the demand does not reach is listed beside the config instead of in it
      Given a consuming repository whose bindings carry the list of what coverage does not cover
      And the tool's own config excludes none of it
      When the wiring is audited
      Then that list is reported as a second copy of the gate
      And the part of the repository no gate reaches is named

    Example: the audit does not move the number it found
      Given an audit that has found a demand equal to what the code scores
      When it makes its corrections
      Then the row that recorded that number as a decision is corrected
      And the config the gate reads is left to the sitting that wires it

  @rule:the-checklist-is-the-method-as-it-now-stands
  Rule: A row is audited against the method as it now stands, and having been correct under the version the ledger is stamped against is not a reason to leave it

    Example: the row conformed to the version it was reconciled against
      Given a ledger stamped as reconciled against an earlier version of this method
      And a row that was correct under that version and is against the method as it now stands
      When the wiring is audited
      Then the row is reported against the method as it now stands
      And having been right when it was written is not offered as a reason to leave it

    Example: nothing is missing, so nothing announces itself
      Given a ledger whose rows are all present and none of which claims more than was wired
      When the wiring is audited
      Then what the method has since changed about those rows is still reported
      And a complete ledger is not read as a current one

    Example: the stamp says what to read for
      Given a ledger carrying the version its wiring was last reconciled against
      When the wiring is audited
      Then what the method has changed since that version is what the audit reads for
      And the stamp is not treated as evidence that the rows beneath it are current

  @rule:a-skill-the-record-names-is-one-that-exists
  Rule: A skill named in a repository's own record is read against the skills this plugin now has, and a record left on a name that has moved is reported

    Example: the record names a skill that has been renamed away
      Given a consuming repository whose own account of the loop names a skill by a name this plugin no longer has
      When the wiring is audited
      Then that name is reported as reaching no skill
      And the name it now has is offered in its place

    Example: the same word is ordinary prose rather than a skill
      Given a record describing what the loop does in the same word a skill is named for
      When the wiring is audited
      Then nothing is reported about that sentence
      And only a name standing for a skill is read as one

    Example: every skill the record names exists
      Given a consuming repository whose record names only skills this plugin has
      When the wiring is audited
      Then nothing about the names is reported
      And no correction is offered that nobody needs

  @rule:the-loop-is-read-from-the-history
  Rule: The audit reads every change merged since the last one for the loop it followed — a change spec committed before the code, its header saying what became of the sketch, or the light path with an issue — and reports what it finds without ever failing a build on it

    Example: a fix merged with no spec and no issue
      Given a change merged since the last audit that adds no change spec and names no issue
      When the wiring is audited
      Then that change is reported as having followed neither the loop nor the light path

    Example: a pipeline fix takes the light path
      Given a change merged since the last audit that adds no change spec and names the issue it fixes
      When the wiring is audited
      Then nothing is reported about it

    Example: a branch commit names its issue at the end of its subject
      Given a change merged since the last audit whose commits end their subjects with the issue, as "fix the pipeline (#12)"
      When the wiring is audited
      Then nothing is reported about it
      But a squashed change whose only number is the one its forge put at the end of its subject is still reported

    Example: the merge names the issue
      Given a change merged since the last audit whose commits name no issue, merged by a commit whose body says "Closes #12"
      When the wiring is audited
      Then nothing is reported about it

    Example: a release commit is not a change
      Given a commit on the main line since the last audit whose only change is the version a manifest carries, as a release bot's "v0.0.14"
      When the wiring is audited
      Then nothing is reported about it
      But a commit that changes anything beside that version is still read for its loop

    Example: the code was committed before its spec
      Given a change merged since the last audit whose first commit touches code and whose spec commit follows it
      When the wiring is audited
      Then the change is reported as implemented before its spec

    Example: a spec that does not say what became of its sketch
      Given a change merged since the last audit whose spec has no Sketch line
      When the wiring is audited
      Then the spec is reported by name

    Example: a squashed change cannot show its order
      Given a change squashed into one commit with its spec and its Sketch line
      When the wiring is audited
      Then nothing is reported about the order it was committed in

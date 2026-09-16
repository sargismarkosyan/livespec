@feature:audit-the-shape @workflow:adopt-the-process
Feature: The shape a ledger has, so that one tool can read every repository's

  @rule:the-bindings-are-written-from-one-template
  Rule: A consuming repository's bindings are written from the template the plugin ships, so the stamp line and the three tables read the same in every repository

    Example: the sitting writes the bindings
      Given a consuming repository having the process set up
      When the bindings are written
      Then they are the template, filled
      And every ledger row carries the id of the gate it is a row for

    Example: the template is proven here
      Given the fixture this repository's faults are injected into
      When verification runs
      Then that fixture is the template filled green
      And a template the tool cannot parse fails here before it ships

  @rule:a-ledger-not-in-shape-is-a-finding-not-a-crash
  Rule: A ledger the tool cannot parse is reported as not in shape, and every check that needed it reads not applicable for that reason, while the rest of the audit goes on

    Example: a ledger typed before the template existed
      Given a consuming repository whose ledger predates the template
      When the wiring is audited
      Then the shape is reported as the finding
      And the checks that read the tables say why they could not
      And the checks that read the stamp, the record and the tree are answered as usual

  @rule:old-rows-are-matched-by-alias
  Rule: A row written before ids existed is matched to its id by the labels the table lists, the audit writes the id in, and reshaping the tables is left to the sitting

    Example: seventeen rows, all matched
      Given a ledger whose rows carry the labels the method used to describe its gates
      When the wiring is audited
      Then each row is matched to its id by that label
      And the id is written into the row as a correction to the record

    Example: a row two ids could claim
      Given a row whose label matches more than one id
      When the wiring is audited
      Then the row is reported as unmatched, naming the candidates
      And nothing is written into it

    Example: the columns are not moved by the audit
      Given a matched ledger in the shape it was typed in
      When the audit makes its corrections
      Then the ids are in the rows and the columns are where they were
      And the reply ends with the command that starts the sitting, which reshapes it

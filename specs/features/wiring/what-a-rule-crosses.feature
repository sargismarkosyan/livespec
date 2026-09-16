@feature:wiring-what-a-rule-crosses @workflow:adopt-the-process
Feature: What the build and the spec step hold a rule to when it crosses a boundary

  @rule:a-crossing-names-a-row
  Rule: A rule that says what boundary it crosses names a row in the bindings' boundaries table, and a crossing that names no row fails verification

    Example: the row is there
      Given a rule tagged as crossing the store
      And the bindings carry a boundary row for the store
      When verification runs
      Then the crossing is read against that row and nothing is reported

    Example: a boundary nobody wrote down
      Given a rule tagged as crossing a service the bindings have no row for
      When verification runs
      Then it fails, naming the rule and the boundary
      And the fix it names is a row in the boundaries table, or a tag that names one that exists

    Example: a rule that crosses nothing owes nothing
      Given a rule with no crossing tag
      When verification runs
      Then nothing about boundaries is asked of it

  @rule:a-crossing-has-its-boundary-misbehaving
  Rule: A crossing rule carries more than one example — the ordinary case and the boundary misbehaving — and one with a single example is warned about rather than failed

    Example: the crossing has only one example
      Given a rule tagged as crossing the store with a single example, the store behaving
      When verification runs
      Then it warns, naming the rule and the boundary, that a crossing with no example of the boundary misbehaving has specced the demo
      And the build is not failed for it

    Example: the store refusing is written down beside the ordinary case
      Given the same rule with a second example, the store refusing
      When verification runs
      Then no warning is reported for it

  @rule:refine-spec-asks-for-the-boundary-misbehaving
  Rule: When a request cannot be met without a boundary, the spec step asks what must still be true when that boundary misbehaves before the spec is written, and the rule it writes carries the crossing and the misbehaving example

    Example: a request that crosses a service
      Given a consuming repository whose bindings carry boundary rows
      And a request that cannot be met without one of the things those rows name
      When the request is refined into a spec
      Then the round of questions asks what the person must still see when that boundary is down, slow or refusing
      And the rule written names the row it crosses and carries an example of it misbehaving

    Example: a request that crosses nothing
      Given a request whose rule needs nothing outside the app's own code
      When the request is refined into a spec
      Then no crossing is written and no such question is asked

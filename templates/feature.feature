@feature:<id> @workflow:<id>
Feature: <What this component does — the thing, not the change that added it>

  # ── The tags ────────────────────────────────────────────────────────────────
  # @feature:<id> and every @rule:<id> below are unique across the whole
  # repository and **permanent**. Reword a Feature: or Rule: line as much as you
  # like — it is the same rule. Changing an id orphans every test pointing at it,
  # and the gate reports those tests as claiming something that does not exist.
  #
  # @workflow:<id> says what bounded attempt this serves. Every feature needs one;
  # a feature serving two attempts carries both. A feature that serves nothing
  # anybody wrote down fails the gate — and the fix is usually that the attempt is
  # missing from the workflows, not that this file needs a tag.
  #
  # **No @persona: and no @journey: here.** Every feature reaches a persona
  # through its workflow. A second path to the same fact is a second thing to
  # keep true.

  # ── Scope ───────────────────────────────────────────────────────────────────
  # One component or behaviour per file, and small — soft limits are 120 lines
  # and 6 rules. Past those, add a file rather than grow this one.
  #
  # The prose belongs upstairs: who this is for is in specs/personas/, the attempt
  # it serves is in specs/workflows/, and the vocabulary and boundaries are in
  # specs/spec.md. Do not restate any of it here. What goes here is what must be
  # *true*.

  # ── The rules ───────────────────────────────────────────────────────────────
  # A Rule is one thing that must be true — a promise the product makes, not a
  # mechanism it uses. If it would need rewording when the implementation changes,
  # it is written at the wrong altitude.
  #
  # Every Rule needs at least one Example:. A rule with no example is an opinion.
  #
  # Write the examples in the persona's own terms, using the vocabulary that
  # specs/spec.md sets down — never a generic stand-in like "item", "entry" or
  # "record" where the repo has a real word, and never a word the repo has
  # deliberately retired. The examples are where a vocabulary is either kept or
  # quietly dropped.
  #
  # Declarative, never imperative: say what happens, not which control does it.
  # No clicks, no element names, no pixels. One behaviour per example, and the
  # name states what it proves rather than the steps it takes.

  @rule:<id> @planned
  Rule: <the promise, stated so it is either true or false>

    # @planned means specced but not built. Specs land before code, so this is
    # the normal state of a new rule — and dropping the tag is part of the change
    # that makes it true, not part of writing it. A @planned rule that already
    # has a test fails the gate.

    Example: <the ordinary case, named for what it proves>
      Given <the state that makes this possible>
      When <the one action>
      Then <the observable outcome>

  @rule:<id> @planned
  Rule: <what must still be true when it goes wrong>

    # The rule most worth writing, and the one most often missing. A feature file
    # whose every rule is a happy path has specced the demo.
    #
    # Add @refusal when the promise is that *nothing* happens — the product
    # staying out of something it was not asked for. Only a test asserting
    # absence can verify one, and the tag is what tells the gate that such a test
    # is the right kind rather than a mistagged one.

    Example: <the failure, named for what survives it>
      Given <state>
      When <the thing that goes wrong>
      Then <what must still be true>

    Example: <the boundary — the case just inside or just outside the promise>
      Given <state>
      When <action>
      Then <outcome>

  # ── Changing this file later ────────────────────────────────────────────────
  # Behaviour changed? Edit the Rule in place and **keep its id**. A reworded rule
  # is the same rule.
  #
  # Behaviour withdrawn? Delete the rule and its tests in the same change. A rule
  # left in the tree with its examples deleted reads as current to everybody who
  # was not there.

@workflow:<id> @persona:<id> @journey:<id>
Feature: <Verb the thing — what they are attempting>

  # ── The job story ───────────────────────────────────────────────────────────
  # Situation first, never role first. "As a user, I want…" starts from who
  # somebody is and assumes that explains the motivation; this starts from the
  # moment, which is the thing that actually causes the attempt.

  When <the situation that set this off — a moment, not a decision to use the app>,
  I want <what they are trying to end up with>,
  so <why that is worth the effort>.

  **Ends when** <one observable end state you can stand at and say "done">.

  # ── The prose ───────────────────────────────────────────────────────────────
  # Two or three short sections. Each is a decision somebody could otherwise
  # relitigate, not a description of the screen.

  **Done well.** What a good attempt looks like, in their terms. Include the cost
  it must not exceed — three seconds, no mouse, one hand — where there is one.

  **<A distinction worth protecting>.** The line this workflow must not cross,
  and why. Delete this section rather than pad it.

  **Where it breaks.** The failure modes, named. This is what stops the examples
  below being a happy path, and it is the section most worth writing first.

  # ── The examples ────────────────────────────────────────────────────────────
  # Declarative, never imperative: say what happens, not which control does it.
  # No clicks, no drags-by-pixel, no element names. One behaviour per example,
  # and the name states the intent rather than the mechanics.
  #
  # Use the words from the product spec's vocabulary and nowhere else's.
  # The last example comes back to the app and finds it exactly as left.

  Example: <the ordinary case, named for what it proves>
    Given <the state that makes this attempt possible>
    When <the one action>
    Then <the observable outcome>

  Example: <the case from "where it breaks">
    Given <state>
    When <action>
    Then <what must still be true>

  Example: <it survives being closed>
    Given <state>
    When <action>
    And I come back to the app
    Then <the outcome is exactly as left>

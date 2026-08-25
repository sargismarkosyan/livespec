# Spec 0016: captured, or built

- **Status:** proposed
- **Issue:** none — direct request, from the human reporting how they actually
  use `feedback`: *"its used both for capturing the work, any work request, it
  could be bug or feature."*

## Who this is for

[`@persona:agent-accelerated-owner`](../personas/agent-accelerated-owner.md) —
Ren, in the part of their day the workflow layer has not cut yet.

**This serves an always-promise rather than a workflow: `context-budget`**
([spec.md](../spec.md#the-promises-that-belong-to-no-single-workflow)). Both
files it touches are `description` fields — the one thing every session of every
user pays for whether or not the skill fires, and the field this repository is
most explicit about not widening on a hunch.

The feature names `adopt-the-process`, which is the only live workflow, and the
same tag [`0009`](0009-whose-repository-whose-tracker.md) put on
[`routing/repository.feature`](../features/routing/repository.feature) and
[`routing/tracker.feature`](../features/routing/tracker.feature) for rules that
also govern a skill used daily long after the sitting ends. **The honest version
is in *Risks*:** the boundary this draws sits between two attempts
[the workflows README](../workflows/README.md#three-more-attempts-not-written-yet)
lists as real and uninterviewed — *filing what they found* and *getting a request
specced and approved*. This spec does not cut them.

## The job behind the request

**Say the thing once, and have it end up where it was meant to go.**

Something comes up — it broke, it is missing, it would be better if. There are
two places it can go: onto the pile of things to deal with later, or into the
change being made now. Which one is a decision the person has already made before
they open their mouth. What they want is for that decision to survive the
sentence, without having to phrase it twice and without having to know which
skill they are addressing.

## Why now

**Because a description is claiming something about the skill that is not true.**
`feedback` opens *"Turn a human testing session into well-researched issues"* and
gates itself on the app being reported on *"from having actually used it"*. The
person who uses it every day says it is what they reach for to capture **any**
work request, bug or feature. A feature request nobody has used the app to want
does not fit through that sentence, and the sentence is in the expensive field.

**Because two descriptions claim the same utterance and nothing says which
wins.** `feedback` claims *"an 'I wish it did X'"*. `refine-spec` claims
*"can it also…"*. Those are one sentence with two spellings, split across two
skills arbitrarily, and the split is invisible to the person saying it. Both are
always-on, so this ambiguity is not merely paid for once — it is read in every
session on this account, forever, and resolved by whichever description the model
liked better that time.

**Because the boundary is already decided everywhere except where it is needed.**
[`spec.md`](../spec.md#the-promises-that-belong-to-no-single-workflow) states it
in the `never-implements` promise — *"`feedback` files, `refine-*` specs,
`record-clip` records"* — `CLAUDE.md` states it as steps 2 and 3 of the loop, and
both skill bodies state it in their opening paragraphs. The only two files that
do not state it are the two that get read before anything else does.

**And the evidence says routing is where this plugin earns its keep.** On
[`evals/board.json`](../../evals/board.json), the two cases shaped around
comprehending a report measure Δ 0.00 — `02-feedback-from-use` (0.75 / 0.75) and
`13-feedback-about-the-plugin` (1.00 / 1.00). The two that measure something are
the routing cases [`0009`](0009-whose-repository-whose-tracker.md) added:
`14-feedback-with-no-subject` at Δ 1.00 and `15-tracker-is-not-the-assumed-one`
at Δ 0.17. A bare model already recognises *"I used it and it broke"*. What it
does not do unaided is put the result in the right place. **That table is thin
and is not leaned on** — see *Risks*.

## The end value

A request lands where they meant it — on the pile, or in the change — decided by
whether they were **reporting** or **instructing**, which is something they
already said. Not by which of two descriptions grabbed it first.

And a feature request stops having to be dressed as a usage report to be
captured at all.

**How we would know it worked:** *"I wish it did X"* and *"can it also…"* stop
resolving to different skills. A plain feature request with no usage behind it
gets captured, rather than dropped for not fitting the sentence or answered with
a spec interview nobody asked for. And `01-solution-shaped-request` — the
highest Δ in the suite at 0.83 over three runs, and an instruction — still
reaches a spec.

## What changes

Two `description` fields. Nothing else in either skill body, and no new skill.

1. **`feedback` loses the usage gate.** *"a human testing session"* and *"from
   having actually used it"* come out. What replaces them says what the skill
   takes — anything somebody found or wants, bug or feature — without asserting
   where it came from.

2. **Both descriptions name the destination they own.** `feedback` says the
   result is a tracked issue. `refine-spec` says the result is a numbered change
   spec. This is the sentence the two bodies and `spec.md` already agree on and
   neither description carries.

3. **The fork is stated in the words the person actually uses.** A report or a
   wish — *"it broke"*, *"I wish it did X"*, *"log this"* — is captured. An
   instruction — *"add X"*, *"pick up issue 7"* — is specced. **The axis is
   intent, not kind:** a bug can be either, and so can a feature. That is the
   half both descriptions currently get wrong by sorting on kind.

4. **`refine-spec` gives up the musings and keeps the imperatives.**
   *"can it also…"* moves to the capture side to sit with *"I wish it did X"*.
   *"just add a button"*, *"picking up a tracked issue"* and *"acting on
   feedback"* stay — those are instructions, and one of them is
   `01-solution-shaped-request`.

**Rules added or changed** — the `@rule:` ids in `specs/features/`:

| Rule id | Feature file | New or changed |
|---|---|---|
| `capture-and-build-are-different-destinations` | `features/routing/destination.feature` | new |
| `capture-does-not-require-having-used-it` | `features/routing/destination.feature` | new |
| `an-instruction-to-build-is-not-filed-instead` | `features/routing/destination.feature` | new |

All three are `@planned` and the file is committed with this spec.

**Ledger:** nothing moves. No new gate.

## What we are not doing

- **Not renaming the skill.** Raised and settled: `request` was the candidate,
  and it puts the same word on both sides of the line it is trying to draw —
  `refine-spec`'s description is *"Refine a request into…"* and its body opens
  *"A request is not a spec."* Two skills whose names both say *request* is a
  worse trigger surface than one that says *feedback*. The cost was also counted
  and is not why: `skill:feedback` appears in eval frontmatter and in every
  `skill-fired` grader's `input_match`, so a rename edits five cases, stales
  their [board](../../evals/board.json) entries and buys a re-measure that is the
  maintainer's money — and `CHANGELOG.md` and `specs/changes/` are immutable, so
  both names would live here permanently. **The name was never the defect. The
  undrawn boundary was.**

- **Not making `feedback` a general work tracker.** *"Log a task to refactor the
  CI"* stays outside it. Dropping the usage gate widens what may be captured
  about the app; it does not turn the skill into a todo list, and
  [`spec.md`](../spec.md#what-it-is) is explicit that more surface is the wrong
  instinct here.

- **Not cutting the two workflows underneath this.** *Filing what they found* and
  *getting a request specced and approved* are still uninterviewed, and
  `refine-workflows` owns them. A workflow cut from a guess has to be cut twice.

- **Not touching where anything files.** Which repository and which tracker are
  [`0009`](0009-whose-repository-whose-tracker.md)'s six live rules and they are
  not reopened. This change decides *tracker or spec*; those decide *whose*.

- **Not adding a question to the daily attempt.** Considered: having the skill
  ask *"track it or build it?"* when intent is unclear. Dropped —
  [the workflows README](../workflows/README.md#reading-this-as-a-map) is explicit
  that a step added to a daily attempt has to name what it shortens, and this one
  shortens nothing. The words already carry the intent; the descriptions just
  have to read them.

- **Not re-measuring the board as part of this spec.** Implementation edits two
  skills and stales their cases. What that costs and when it is spent is named in
  *Acceptance checks* and is the maintainer's call, not this spec's.

## Data

None. There is no storage contract — the plugin ships prose, and what a version
leaves behind is listed in [spec.md](../spec.md#what-a-version-leaves-behind).

## Risks

- **`context-budget`, and this one widens.** `feedback`'s description is 459
  characters inside a 3801/5000 total. Removing a qualifier makes it grab more,
  and the promise is unambiguous that widening is *"paid for in `evals/` with a
  should-not-fire case, never on a hunch."* That payment is
  `an-instruction-to-build-is-not-filed-instead`, tagged `@refusal` for the same
  reason [`setup-ignores-an-adjacent-request`](../features/setup/invocation.feature)
  is. `refine-spec` narrows and owes nothing. **Headroom is not the argument** —
  there are 1199 characters spare and they are not what makes this affordable.

- **The board evidence is thin, and it is thinner than it looks.** The Δ 0.00
  readings above are single runs. They are also partly structural: a `tool_used`
  grader with `min:` and no `max:` is an *indicator* by
  [`asserts.py`](../../evals/runner/asserts.py)'s contract — it always passes,
  in both arms, weight zero, so that firing cannot inflate Δ. Every `skill-fired`
  grader is one. So `13-feedback-about-the-plugin` scoring 1.00 without the
  plugin is correct rather than broken, and what those cases actually measure is
  their outcome graders alone — which on 02 and 13 come out level. **The
  argument here does not rest on that table**, because two descriptions
  contradicting each other is readable without running anything.

- **`01-solution-shaped-request` is the case most exposed.** *"Add a 'clear all
  completed' button"* is an imperative and stays with `refine-spec` under item 3
  — but it is the highest Δ in the suite (0.83 over three runs) and it sits
  directly on the line being drawn. If moving *"can it also…"* off `refine-spec`
  drags the imperatives with it, that case is where it shows.

- **The boundary is drawn above two uncut workflows.** When
  `refine-workflows` interviews *filing what they found*, this rule is the thing
  it will either confirm or contradict. Written down here so the contradiction is
  visible rather than discovered.

- **`ids-are-permanent`.** Three new rule ids ship in this change and can never
  be renamed. They are named for the promise (capture versus build) rather than
  for either skill, so a later rename of a skill — ruled out here, not forever —
  does not orphan them.

## Acceptance checks

1. `python3 .github/scripts/verify.py` green, and the always-on cost `checks.py`
   reports is **at or below 3801** across 7 skills. Item 4 removes more from
   `refine-spec` than item 1 adds to `feedback`; if the total rises, the widening
   was not paid for and the spec is wrong rather than the budget being tight.
2. Read the two descriptions back to back. Somebody who has never seen this
   repository can say which one takes *"I wish it did X"* and which takes
   *"add a clear-all button"*, without opening either skill body.
3. In a consuming repository, say *"log a feature request: it should support
   dark mode"* — nothing about having used the app. It is captured as a tracked
   issue, and nothing asks what they were doing when they found it.
4. Same repository, say *"add dark mode"*. It reaches a change spec, and no issue
   is filed in place of it.
5. Read `feedback`'s description looking only for a claim about where the request
   came from. There should be none.
6. **The measurement, and it costs money.** Editing two skills stales
   `02-feedback-from-use`, `08-fix-it-while-recording`,
   `13-feedback-about-the-plugin`, `14-feedback-with-no-subject`,
   `15-tracker-is-not-the-assumed-one` and `01-solution-shaped-request`, plus the
   new should-not-fire case. `verify.py` stays red until
   `run.py --changed` re-measures exactly those. **That is the maintainer's
   signature and roughly the price of most of a suite** — the number goes in the
   pull request, and the implementing change stops and asks before spending it.

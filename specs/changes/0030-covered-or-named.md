# Spec 0030: covered, or named

- **Status:** proposed
- **Issue:** [#79](https://github.com/sargismarkosyan/livespec/issues/79)
- **Depends on:** nothing. It corrects one question in
  [`setup`](../../skills/setup/SKILL.md) §2 and the refusal that already names
  the harm that question produces.

## Who this is for

[`agent-accelerated-owner`](../personas/agent-accelerated-owner.md), in
[`adopt-the-process`](../workflows/adopt-the-process.feature) — at §2 of the
sitting, the single round where the agent asks rather than derives, and
therefore the only place a threshold is ever decided rather than inherited.

The persona line this turns on is **"a setup they did not agree to gets stopped
and questioned rather than inherited."** A threshold read off today's coverage
report is exactly that, wearing a decision's clothes: it was measured, not
chosen, and it arrives in the bindings looking like an answer somebody gave.

**This does not lengthen the attempt.** The [workflows
README](../workflows/README.md) requires a change that adds a step to adoption
to name the later attempt it shortens; this adds no step. The question is
already asked, in the same round, in the same breath — what changes is the
recommendation attached to it.

## The job behind the request

To know that the part of the code nothing tests is a list somebody wrote, rather
than a remainder left over by a number.

## Why now

Because the failure the skill warns about has already happened in the one
repository this process was installed in, and it happened by following the
instruction rather than by ignoring it.

Measured in `todo-change` on **2026-09-01**, `npm test`, 426 tests passing:

| | lines | branches | functions |
|---|---|---|---|
| what the gate demands | 95.00 | 95.00 | 95.00 |
| what the code scores | **100.00** | **98.37** | **99.13** |
| slack | 5.00 | 3.37 | 4.13 |

Every point of that slack is permitted regression that no build will report.
`src/app.mjs` can lose five points of line coverage and the gate stays green;
the 1.63% of branches nobody covers today has no name anywhere, so nothing
distinguishes it from the branches that used to be covered and stopped.

`setup` §2 produced this by instruction: *"Recommend what the repo already
has."* And the refusal list at the end of the same file already names the harm —
*"a 95% threshold that came from somewhere else is a number nobody chose"* — it
just names the wrong route to it. A number read off your own report is also a
number nobody chose. It was taken, not decided, and the ratchet the same
paragraph warns about is what a threshold set at today's score can only ever be.

The instruction's other half is the real obstacle and it is correct: a demand
*far above* what the code scores "fails on day one and gets switched off by
Friday." That is what has to be answered rather than obeyed, and the answer is
not a smaller number.

## The end value

The coverage row in the bindings stops being one number somebody read off a
report and becomes the two things they decided: what is in scope, and what is
excluded with the reason it is. Nothing is uncovered by accident, and a branch
that was covered yesterday and is not today fails the build instead of being
absorbed by slack nobody allocated.

**How we would know it worked:** the gap between what the gate demands and what
the code scores goes to zero, so a coverage regression that used to pass now
fails. Slower and more telling: an exclusion line gets deleted in a pull request
that covers what it named — a ratchet moving in a diff, which is the thing a
percentage cannot do.

## What changes

- **§2's third question stops asking for a number.** It asks what is in scope
  and what is excluded from it; the demand over what remains is the whole of it.
  The number that lands in the bindings is still the adopter's to write — what
  changes is that it is no longer derived from their current score.
- **The day-one objection is answered where it is raised.** An occupied
  repository does not get a lower threshold to fit its untested modules; those
  modules are named, and the demand over what is left stands. Nothing fails on
  day one, because the day-one exclusion list is exactly today's uncovered code
  written down.
- **The exclusions go where the tool reads them**, in §4, not into prose beside
  it. An exclusion list the coverage runner never sees is a second copy of the
  binding, and the two disagree the first time either moves.
- **The refusal at the end of the file names both routes to the same harm.** It
  currently refuses a number copied from another repository; it also has to
  refuse a number subtracted from your own, because the reason given is the same
  in both cases and only one of them is currently caught.
- **`method/testing.md` gains one judgment**, in the *Coverage* list whose
  standing preamble is already "The thresholds are the repository's. The
  judgment is not": an uncovered path is either named, with its reason, or it is
  a gap. **It names no number and no tool**, which is what lets it live there —
  it says who chooses, not how much, and it survives a repository with pytest
  and a Makefile. The existing bullet about deleting an unreachable branch
  rather than faking a test for it is the same principle one level down.

**Rules added or changed** — the `@rule:` ids in `specs/features/`:

| Rule id | Feature file | New or changed | Ships |
|---|---|---|---|
| `the-coverage-demand-is-not-todays-score` | `features/setup/coverage-binding.feature` | new | `@planned` |
| `what-is-not-covered-is-named-rather-than-subtracted` | `features/setup/coverage-binding.feature` | new | `@planned` |

A new file rather than two rules added to
[`test-binding`](../features/setup/test-binding.feature): that one answers *what
proves a rule is true here*, and this is about what the gate over the result is
asked to demand. Same round of the same sitting, different question — and
`test-binding` is already at three rules with the spec-bound measure in it,
which is the rule these two are most likely to be confused with and worth
keeping a file away from.

### What this repository owes itself, and why the answer is nothing

[`0029`](0029-drawn-before-it-is-built.md) established that a rule written here
binds here too unless there is an honest reason it cannot. There is one:
**this repository has no coverage gate and no application code to put under
one.** [The bindings](../setup/README.md#what-has-no-gate-and-what-that-misses)
already say so and say what that misses, and a coverage number over
`.github/scripts/` would measure the gates rather than the product.

That is not an exemption this change creates or widens. The row stays as
written.

## What we are not doing

- **Naming 100 in `method/`.** A percentage is a threshold and a threshold is a
  binding — [`spec.md`](../spec.md)'s vocabulary says so in one line. What
  `method/` gains is the judgment that an exemption is named rather than
  subtracted, which is portable and numberless.
- **Gating the exclusion list.** Nothing here can check that "legacy, scheduled
  for deletion" is a true reason, and a gate that only checks the list exists
  would be satisfied by one line reading `src/`. This is held by cases and by
  the person reading the diff, like every other judgment in this method.
- **Fixing `todo-change` from here.** Its 95 is that repository's binding and
  moving it is a change over there, made by running the sitting in it. A spec in
  this tree that edits another repository's gate is the coupling this whole
  method exists to avoid.
- **A ratchet mechanism.** No tooling that raises a threshold as coverage rises.
  The demand is already the whole of what is in scope; there is nothing left to
  ratchet, which is the point of moving the argument off the number.
- **Touching Gate 2 in [`gates.md`](../../method/gates.md).** "All three, and the
  number is the repo's" stays exactly true, as does the refusal to pass on a
  measurement of nothing. Neither is what went wrong.
- **The spec-bound measure.** It is reported and
  [never gated](../../method/testing.md#measure-the-rule-bound-tests-on-their-own-and-never-gate-it),
  that is settled, and folding it in here would reopen it by accident.
- **The other four questions in §2.** Only the coverage one is changing. The
  test-binding question already recommends what the repository runs, and that is
  right for a *mechanism* in a way it is not for a *demand*.

## Data

No storage contract moves; there is none here. `evals/board.json` gains no
field, and **nothing goes stale on the spec commit** — a new feature file whose
two rules are `@planned` and claimed by nobody, plus this file.

**The implementing commit is where the bill lands, and it is the largest this
repository has faced.** `measurement_inputs` hashes the body of every skill a
case holds, and **eight cases hold `skill:setup`**:

| Case | Board today | Re-measure at the floor |
|---|---|---|
| [`09-setup-confirms-before-writing`](../../evals/09-setup-confirms-before-writing/) | Δ +0.5, 1 run, $0.28 | ~$0.84 |
| [`11-neg-setup-adjacent-request`](../../evals/11-neg-setup-adjacent-request/) | Δ 0.0, 1 run, $0.12 | ~$0.36 |
| [`12-setup-drives-the-sitting`](../../evals/12-setup-drives-the-sitting/) | Δ −0.14, 1 run, $0.34 | ~$1.02 |
| [`16-setup-with-no-app-code`](../../evals/16-setup-with-no-app-code/) | Δ +0.5, 1 run, $0.17 | ~$0.51 |
| [`17-wiring-nobody-watched-run`](../../evals/17-wiring-nobody-watched-run/) | Δ +1.0, 1 run, $1.59 | ~$4.77 |
| [`23-what-a-change-here-must-show`](../../evals/23-what-a-change-here-must-show/) | Δ −0.5, 1 run, $1.43 | ~$4.29 |
| [`26-two-seconds-before-the-push`](../../evals/26-two-seconds-before-the-push/) | Δ +0.22, **3 runs**, $4.78 | ~$4.78 |
| [`27-a-red-nobody-here-can-clear`](../../evals/27-a-red-nobody-here-can-clear/) | Δ +0.25, 2 runs, $6.42 | ~$9.63 |
| a new case claiming both rules | never measured | ~$2–5, softly |

**Roughly $28 to clear the board properly, and there is a cheaper honest floor.**
Seven of the eight entries are below the run floor, so
[`0028`](0028-below-the-floor.md)'s rule lets a pilot re-fill their rows; only
`26-two-seconds-before-the-push` is a measurement and may not be overwritten by
anything under three runs. Pilots for the seven plus three runs for that one is
**~$9**, and it leaves the board no worse informed than it is today.

Both figures are estimates from the last runs' own per-session costs, and
[`0029`](0029-drawn-before-it-is-built.md)'s estimate ran 40% low.

**This bill is shared with [#77](https://github.com/sargismarkosyan/livespec/issues/77).**
That issue also edits `skills/setup/SKILL.md`, and staleness is content-addressed
rather than per-change: if both land before a run, the same eight rows are paid
for once instead of twice. That is a reason to sequence them together, not a
reason to merge them into one spec.

`method/testing.md` is in no column. No case hashes a method document, which is
a fact about what the board measures rather than a claim that it matters less.

## Risks

- **The demand gets refused in an occupied repository**, which is the exact
  failure `setup` §2 warns about today. The mitigation is structural: the
  exclusion list has to arrive in the same sentence as the demand, or the
  adopter hears "cover 40,000 untested lines" and reaches for a number. If the
  eval case for this shows the demand landing without the list, the rule is
  written wrong rather than the adopter being wrong.
- **The exclusion list becomes the new anonymous remainder.** One line reading
  `src/legacy/` with "legacy" beside it is 95% with extra steps. Nothing catches
  this and the spec says so above; what it buys even then is that the remainder
  has an address and shows up in a diff, which 5 percentage points never do.
- **A repository with a coverage tool that cannot exclude anything.** Then the
  binding says so and names a number, and the bindings file admits which of the
  two shapes it is on — the same move [`0021`](0021-asked-not-assumed.md) made
  for a coverage gate covering one language of two.
- **`always-green` and `context-budget` are untouched.** No description changes,
  so no session pays unless `setup` fires; no consuming build gains a dependency
  on anything an agent installed.
- **The bill is the real risk to the loop, not to the product.** Eight stale
  rows is a red that says nothing is broken, and a run nobody approves leaves it
  standing across every later change to this skill.

## Acceptance checks

1. Run `setup` in a repository with a working suite scoring short of the whole —
   the recommendation is everything in scope plus a named exclusion list, and
   today's score is not offered as the threshold.
2. Run it in a repository with no tests at all. Unchanged: the bindings admit
   the gate has nothing to stand on, and no number is written.
3. Propose a threshold with room in it and watch what comes back — the question
   is which parts the room stands in for, not a haggle over the number.
4. Read §2 and the refusal list together. They name the same harm and no longer
   point in opposite directions.
5. In `todo-change`, re-agree the coverage row: the 1.63% of branches in
   `src/app.mjs` is either covered or named, and the gate demands the rest whole.
6. `python3 .github/scripts/verify.py` — green on this spec commit; exit 2 on
   the implementing commit until the eight rows above are re-measured, which is
   the maintainer's spend to approve.

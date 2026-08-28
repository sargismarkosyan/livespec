# Spec 0022: nobody types the record

- **Status:** proposed
- **Issue:** [#59](https://github.com/sargismarkosyan/livespec/issues/59)
- **Depends on:** nothing. The enumerations it reads back have all been in the
  tree since [`0013`](0013-the-board-of-latest-measurements.md).

## Who this is for

**Not [`@persona:agent-accelerated-owner`](../personas/agent-accelerated-owner.md),
and not any workflow.** Ren adopts the process in their own repositories; this
changes livespec's own bindings and its own gate scripts, which
[`workflows/README.md`](../workflows/README.md) is explicit about — an attempt
made *on* this repository is a contribution step, not an attempt somebody makes
with the plugin installed.
[`process.md`](../../method/process.md#a-technical-change-that-serves-no-workflow-is-correct-not-a-gap)
says that is correct rather than a gap, and it is said here out loud rather than
filed under a workflow to fill the box.

What it serves is an always-promise: **`gates-are-proven`**, from
[`spec.md`](../spec.md) — *no gate ships without a fault that makes it fire*. One
sentence of it ships to every user, in [`gates.md`](../../method/gates.md), so
the change carries a release label.

## The job behind the request

The literal ask, from the issue: `specs/setup/README.md` gives three different
fault-injection counts, the fault injection record is six rows short of
`inject.py`, and `evals/README.md`'s case table is three rows short.

The job under it has nothing to do with arithmetic. **`gates-are-proven` is a
promise about evidence, and its evidence is a table somebody typed.** A reader
who wants to know whether the gates here were ever made to fire opens *The fault
injection record* and reads a list of what was tried. That list is not derived
from the injector — it is a copy of it, made by hand at some point, and the
copy has been wrong since three faults after it was written.

Correcting the three numbers is the ask. The job is that **a reader can trust the
bindings about the gates without running anything** — and today they cannot, and
cannot tell that they cannot, which is the worse half.

**What is done today instead:** nothing. `checks.py` gate 3 checks exactly one
enumeration — the skill count, in three files — and every other list or total a
human typed in this repository is on trust.

## Why now

Three things converged, and only one of them is in the issue.

**The record is six faults behind the code.** `inject.py` holds 31 fixture faults
and 9 release faults; the record's table has 34 rows and its prose says *34 of
34*. The six with no row are the newest — the scaffold checks from
[`0016`](0016-captured-or-built.md), the runner's refusal from
[`0019`](0019-what-would-end-it.md), and the three board faults from
[`0013`](0013-the-board-of-latest-measurements.md). Those faults run on every CI
run and appear in nobody's record of what was tried.

**`verify.py` closes every green run with a sentence that is false.** It prints
`✔ verification green — 5 gates, all fired against injected faults`. Four of the
five have faults. **`checks.py` has none and never has** — not by omission but
structurally: it hardcodes `ROOT` from its own path and takes no argument, so
`inject.py` cannot point it at a fixture. The gate that would have caught a typed
enumeration going stale is the one gate this repository has never proven fires.

**It is the defect class this repository shipped a skill for one version ago.**
[`0021`](0021-asked-not-assumed.md) added [`doctor`](../../skills/doctor/SKILL.md)
to catch a claim in a consuming repository's bindings that was written once and
true then. Nobody has run it here. Finding this by hand, in livespec's own
bindings, one version after shipping the cure, is the argument for a gate rather
than a correction.

## The end value

Somebody opening *The fault injection record* is reading what `inject.py`
actually does, because `verify.py` fails if they diverge. The table stops being a
claim about the gates and becomes a view of them.

**How we would know it worked:** add a fault to `inject.py` and commit without
touching the record. `verify.py` goes red, names the fault with no row, and
prints the table as it should now read. That is the acceptance check below, and
it is the exact sequence that produced this issue six times without a word.

## What changes

- **`checks.py` takes an optional root**, matching the `[root]` signature
  `trace.py`, `evalsuite.py` and `board.py` already have. Nothing else about it
  moves. This is what makes the gate injectable at all, and it is the reason the
  change is larger than the issue.
- **`checks.py` reads the fault injection record back from `inject.py`.** Every
  fault in `FAULTS + RELEASE_FAULTS` has a row, in the same order, with an
  *Expected* cell agreeing with the outcome the fault declares; no row names a
  fault that does not exist. On any mismatch it fails and prints the table as it
  should read, so the fix is a paste rather than a recount.
- **`checks.py` reads the *What it runs* row back from `verify.py`.** That row
  currently says `checks.py`, `trace.py`, `evalsuite.py`, `inject.py` — the
  board gate has been missing from it since `0013`. It gains `board.py`, and
  gains a gate.
- **`inject.py` gains `checks.py` as a fifth injectable gate**, with the fixture
  files that gate needs to pass on a synthetic tree, and faults for both new
  checks: a row deleted, a row naming a fault that does not exist, an *Expected*
  cell flipped from `fails` to `warns`, and a gate dropped from the *What it
  runs* row. `checks.py` fires against an injected fault for the first time, and
  `verify.py`'s closing sentence becomes true.
- **The four counts are deleted rather than corrected.** *"breaks it 25 ways,
  then breaks the release inputs 9 more"* and *"37 faults (28 against a fixture,
  9 against the release inputs)"* in `specs/setup/README.md`, *"34 of 34 faults
  produced the expected result"* above the record, and *"breaks every gate 37
  ways — 28 in a temporary fixture, and 9 against the release inputs"* in
  `CONTRIBUTING.md`. None of them tells a reader anything the table does not, all
  four were wrong, and `verify.py` prints the live count on every run. A number
  that only a gate can keep true, and that nobody needs, is better deleted than
  gated.
- **The record gains its six missing rows**, taken from `inject.py`.
- **`evals/README.md` gains rows for `21`, `22` and `23`** — correct while that
  table lives. What happens to the table itself is the next change; see below.

**Rules added or changed:** none. Livespec-local machinery, as in
[`0013`](0013-the-board-of-latest-measurements.md). The one sentence that ships —
`gates.md` saying a record of injected faults is read back from the injector
rather than typed — is guidance to a `setup` sitting, in the same register as the
paragraph it joins. A rule would need an eval case to claim it, and a case is a
measurement somebody pays for; that is not what this sentence is worth.

## What we are not doing

- **Not deleting the record table.** It was considered, and it is the most
  thorough answer — `inject.py` prints every fault and its result on every run,
  so a copy in the bindings is by definition redundant. Dropped because
  `gates.md` tells every consuming repository to keep exactly this record in its
  bindings, and because somebody checking `gates-are-proven` should not have to
  run Python to find out what was tried.
- **Not generating the table in place.** `inject.py --record` writing between
  markers in `specs/setup/README.md` is one command instead of a paste, and it
  gives a gate script the power to edit a spec file whose surrounding prose it
  must not touch. The gate prints the correct table; a human still puts it there.
- **Not moving the case table into the cases' own `tags:` — that is the next
  change, and the split is forced rather than chosen.** Six cases — `01`, `03`,
  `04`, `05`, `08` and `10` — name a skill and claim no rule at all, so the row
  in `evals/README.md` is the only record of what they hold. Deleting the table
  before those cases declare a rule destroys the only copy. Making them declare
  one means writing six rules that do not exist yet, for `refine-spec`,
  `refine-personas`, `refine-workflows`, `refine-journeys` and `record-clip` —
  and `measurement_inputs` hashes a case's own files, so editing six
  `prompt.md` frontmatters stales six board entries and `verify.py` stays red
  until every one is re-measured. At `runs: 3` that is roughly $10–11 billed to
  the maintainer's account, and
  [`evals/README.md`](../../evals/README.md) is unambiguous that the flag which
  spends it is the maintainer's signature and never an agent's. It gets its own
  issue and its own version.
- **Not gating the always-on budget figure.** `specs/setup/README.md` says
  *4315 across 8*; `checks.py` computes and prints that number on every run and
  it is currently right. One number, one file, already printed beside it.
- **Not adding faults for `checks.py`'s existing checks** — manifests agreeing,
  skill frontmatter, the budget, link resolution, unlinked payload. This change
  makes the gate injectable and pays only what the two new checks owe.
  Everything `checks.py` already did stays unproven, and that debt is named here
  rather than closed by implication in a green run.

## Data

No storage contract to touch; this repository has none. What a version leaves
behind is unchanged.

One line in the record stays a human's statement rather than a derived one: the
date and *"Run on … by `python3 .github/scripts/inject.py`"*. The table below it
stops being one.

## Risks

**`always-green` is not at risk** — nothing here runs in a user's build, and the
one file that ships is prose.

**`checks.py` importing `inject.py` couples two gates.** If `inject.py` ever
grows work at import time, `checks.py` fails for a reason that has nothing to do
with what it checks. `inject.py` keeps everything under `if __name__ ==
"__main__"` today and the import is a list of tuples; the coupling is worth one
line of comment at the import, and is cheaper than a third copy of the fault
names.

**The fixture now has to keep `checks.py` green as `checks.py` grows.** A new
check that the synthetic tree does not satisfy turns `inject.py` red, and the
person who added it will read that as a broken injector rather than an
incomplete fixture. That pressure is correct — it is the same pressure the other
three gates already apply — but it is new, and the fixture's docstring should
say so.

**A gate that reads prose is a gate that can be defeated by reformatting.** The
check parses a markdown table; somebody reflowing that section could make it
pass while saying nothing. The mitigation is that the fault injection tests the
parse in both directions — a deleted row and an invented one — rather than only
that a green tree stays green.

## Acceptance checks

1. `python3 .github/scripts/verify.py` is green, and its closing line —
   *5 gates, all fired against injected faults* — is now true.
2. Delete any row from the record in `specs/setup/README.md`. `verify.py` goes
   red, names the fault with no row, and prints the table as it should read.
   Restore it.
3. Add a fault to `inject.py`'s `FAULTS` and do not touch the record.
   `verify.py` goes red. Remove it.
4. Flip one *Expected* cell in the record from `fails` to
   **warns, does not fail**. `verify.py` goes red. Restore it.
5. Remove `board.py` from the *What it runs* row. `verify.py` goes red.
   Restore it.
6. `grep -n "34 of 34\|37 faults\|37 ways\|25 ways" specs/setup/README.md
   CONTRIBUTING.md` prints nothing.
7. `evals/README.md`'s *What each case is for* has a row for every directory
   under `evals/`.

# Spec 0087: a measurement is optional

- **Status:** approved — by the maintainer in advance, 2026-11-21 (*"Measurements run must be optional, that is no longer wanted"*), scoped in the same session to the method and livespec, with what it makes dead deleted; implemented end to end, reviewed at the pull request
- **Issue:** [#201](https://github.com/sargismarkosyan/livespec/issues/201)
- **Sketch:** skipped — approval was given in advance, so there was no decision left for one to support.

## Who this is for

**Ren — [`agent-accelerated-owner`](../personas/agent-accelerated-owner.md).**
Ren runs a graded suite only when they choose to, and is never made to pay
to merge. Nothing about who this is for moves.

**The workflow is [`adopt-the-process`](../workflows/adopt-the-process.feature),**
at *The changes after*, step 8 of [`trusting-the-spec-again`](../journeys/trusting-the-spec-again.md):
every change after the sitting meets verification.

## The job behind the request

To finish and merge a change without a purchase standing in the way, and
still be able to see which numbers no longer describe the files they measured.

## Why now

- **Every open pull request is red for a reason nobody in it can clear.**
  [#199](https://github.com/sargismarkosyan/livespec/pull/199) and
  [#200](https://github.com/sargismarkosyan/livespec/pull/200):
  - `verify.py` exits 2;
  - the `measurement board` job fails;
  - four rows went stale on `main` when the tier harness changed;
  - clearing them is a run of about $100.
- **A red that stands for days needed machinery of its own.** A second exit
  status, a `--local` that leaves the board out, a section of the method
  justifying gates that run after a standing red, a report that must survive
  it, five rules and a case to hold them. All of it exists because freshness
  is gated.

## The end value

Verification is green or broken, never "owed". A stale measurement is
reported on the change, and never asked for.

**How we would know it worked:**
- Here: `verify.py` exits 0 on a tree whose only difference from green is a
  stale tier row, and the report on the pull request still counts it.
- In a consuming repository: the sitting wires no freshness gate, and still
  keeps a graded suite out of the hook because a run of it costs money.

## What changes

1. **[`graded-cases.md`](../../method/graded-cases.md).**
   - *Freshness is gated; the score never is* becomes *Neither freshness nor
     the score is gated*.
   - A stale fingerprint is shown as stale and never presented as current. A
     run happens when the person paying chooses.
   - *Gate the freshness of what you can afford to keep fresh* keeps its two
     speeds and loses the gate.

2. **[`testing.md`](../../method/testing.md), *And again before it leaves
   this machine*.** The hook still keeps out what costs money per run. The
   second kind it kept out, a failure only a paid run can clear, no longer
   exists. That bullet goes, and so does the paragraph about running the free
   part by name.

3. **[`gates.md`](../../method/gates.md).**
   - *And it describes a red build too* goes.
   - *A gate that does not depend on a failing one* goes.
   - Both exist only because a red could stand.

4. **[`repository.md`](../../method/repository.md), *Commits*,** and
   [`setup`](../../skills/setup/SKILL.md): every reference to a sanctioned
   red, or to freshness as a gate, goes or is reworded.

5. **This repository.**
   - **`verify.py`:** the board leaves its gates. `COSTS_MONEY`, the second
     exit status, `verdict()` and `--local` go. The pre-push hook and CI run
     the one command.
   - **`board.py`:** reports, and exits 0. What it used to fail on, it prints
     as stale. The pull-request report reads it as before.
   - **CI:** the `measurement board` job goes. The comments in `checks.yml`
     that justified the standing red are cut to what is still true.
   - **`inject.py`:**
     - `verdict_control` and the verdict fault go;
     - the board's faults expect *warns*;
     - the fixture's *What it runs* follows `verify.py`.
   - **The bindings, `CLAUDE.md` and `CONTRIBUTING.md`** stop describing an
     exit 2.
   - **`report.py`** stops saying the two commands differ.

6. **[`what-costs-money-stays-out-of-the-hook`](../features/setup/before-the-push.feature)**
   is reworded in place and keeps its id: only checks that cost nothing per
   run run before a push. Its example about a check that needs a paid run to
   clear goes. Case 26's grader on it is brought to the same reading.

## What this removes

- **Five rules,** the whole of [`features/verification/which-red.feature`](../features/verification/which-red.feature):
  - `the-one-red-a-commit-may-carry`
  - `a-red-says-which-red-it-is`
  - `what-explains-a-red-survives-it`
  - `a-red-does-not-hide-the-gates-after-it`
  - `a-measurement-nobody-can-clear-does-not-block` (`@planned`)

  Their ids are not reused.
- **Case 27,** `a-red-nobody-here-can-clear`, which claims four of them and
  nothing else.
- **In `verify.py`:** `COSTS_MONEY`, `OWED`, `verdict()`, `--local` and the
  `measurement board` gate.
- **In `inject.py`:** `verdict_control`, `VERDICT_FAULTS`, and their row in
  the fault record.
- **In CI:** the `measurement board` job.
- **The method sections** in items 1–3.
- **Nothing that measures goes.**
  - `board.json`, `tiers.py`, `run.py` and their cost refusals stay: a run
    still costs money and still needs the payer's yes. It is just never owed.
  - The `!cancelled()` guards in CI stay as wiring. They are harmless, and
    cutting them is not this change.

## What we are not doing

- **Deleting the board or the tiers.** The maintainer chose *optional*, not *gone*.
- **Removing the cost refusal on `run.py` and `tiers.py`.** Optional is about
  being owed, not about who pays.
- **Changing the report's board section.** It already reports what is stale
  and decides nothing.

## Data

No storage contract moves. A consuming repository that wired a freshness gate
is told by the method that it need not. Nothing it has fails.

## Risks

- **A stale number gets read as current.** It is marked stale and left out of
  every mean, as the canary pool already is. That is the guard, not a gate.
- **Nobody runs the tiers again.** Then the numbers age in plain view, which
  is the trade the maintainer chose.

## Acceptance checks

1. Run `verify.py` on this branch: exit 0. Run `board.py` by hand: it lists
   the four stale rows and exits 0.
2. Read `.githooks/pre-push` and `checks.yml`: one command, no `--local`, no
   board job.
3. Search the method for *freshness is gated*: nothing.

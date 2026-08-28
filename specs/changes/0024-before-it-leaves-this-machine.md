# Spec 0024: before it leaves this machine

- **Status:** approved
- **Issue:** [#64](https://github.com/sargismarkosyan/livespec/issues/64)
- **Depends on:** nothing. It reads the one-command precondition that
  [`0001`](0001-the-gate-wiring-ledger.md) and setup's section 4 have both stated
  since 0.6.0, and takes the next sentence.

## Who this is for

[`@persona:agent-accelerated-owner`](../personas/agent-accelerated-owner.md), in
[`@workflow:adopt-the-process`](../workflows/adopt-the-process.feature), at the
point in a sitting where the gates have just been wired and nothing yet fires
them by itself. Ren is the person who does not read the docs — which is exactly
who a rule written as prose addressed to whoever remembers to read it does not
reach, and that is the whole defect here.

It also touches a promise that belongs to no workflow: **`always-green`**. A hook
is the one thing this plugin has ever proposed that runs on somebody's machine
without an agent in the room, so the question of whether it can break a build has
to be answered rather than assumed. It cannot: it is off until a person types a
line into their own clone, it runs only what the repository already runs, and CI
never sees it.

## The job behind the request

The literal ask, from the issue: the method never mentions a git hook, so nothing
offers to run the cheap checks before a push.

The job under it is in the reporter's own words — *"I would know on code push
before running claude pipeline."* The cost being avoided is not CI minutes. It is
a round trip through an agent session to be told something a two-second local
command already knew, and the second half of the sentence is the boundary: *"I
don't want to run expensive actions especially LLM once locally on every commit."*
So the job is **a fast local signal that cannot become an expensive one**, and
the reason nobody has built it is not that hooks are obscure.

**What is done today instead:** the method says it in prose, twice —
[`testing.md`](../../method/testing.md) *Before committing*, and
[`repository.md`](../../method/repository.md) *"finding out locally is cheaper"*.
This repository restates it a third time in `CLAUDE.md`. All three are addressed
to whoever remembers, and locally that is an agent's memory. **Eleven of the last
thirty-one `checks` runs here failed, and every one of the eleven was the `Verify`
step** — `verify.py`, which takes 2.3 seconds and which all three sentences
already name.

## Why now

**The precondition has been sitting finished for sixteen versions.** Section 4
ends on *"One command runs both, and CI runs that same command. Not a longer list
in CI than a person can run locally."* That sentence exists to make a hook
possible and stops one word short of offering one.

**The repository that ships the method has no hook either**, which is the tell
that this is a gap in the method rather than an adopter's oversight.
`git config --get core.hooksPath` is unset here and `.git/hooks/` holds nothing
but git's own samples.

**And the reason it was never built is a real one, not an omission.** This
method's model of enforcement is *the platform refuses the merge*: branch
protection, and the ledger's rule that a claim outside the tree is read back from
whatever enforces it. A hook is the opposite kind of object — local, opt-in, and
bypassed by a flag anybody can type. There was no shelf in `gates.md` for a thing
that is enforcement-shaped and not enforcement, so nothing could be put down. The
shelf is most of this change.

## The end value

A sitting that wires the gates ends by asking whether they should also fire
before a push, and the person who says yes finds out about a broken gate on their
own machine, for free, before it becomes anybody else's problem. The person who
says no has nothing installed. Neither of them has a ledger row that overstates
what their repository refuses.

**How we would know it worked:** in a repository whose one verification command
runs both free gates and a graded suite, the thing that comes out of the sitting
runs the free part, says why the paid part is not in it, and appears in no table
of gates. That is [`26`](../../evals/26-two-seconds-before-the-push/prompt.md),
and it is the fixture, not a hypothetical: `beacon`'s `make verify` bills $4.10 a
run and carries a freshness check whose only cure is one of those runs.

## What changes

### The method gains the shelf, and the granularity

- **[`testing.md`](../../method/testing.md) gains *And again before it leaves this
  machine*.** Committing is not the moment the work stops being yours; pushing
  is. The section says the run that has to happen is the one before the push,
  that it is offered rather than installed, and that **cost is the selection
  criterion** — with the two kinds that stay out named: anything that costs money
  per run, and anything whose failure cannot be cleared here for free. It keeps
  *Before committing* rather than replacing it; the discipline stands, and what
  changes is which moment gets automated.
- **[`gates.md`](../../method/gates.md) gains *And what is not wiring at all*,**
  under the second table. A local hook is neither a gate nor wiring that must
  never gate. **It gets no row, in either table** — a bypassable courtesy
  recorded as a refusal is the false green that page already names as its worst
  case, and a reader adding up rows would be counting a check anybody can walk
  past. If it is written down at all it goes in the bindings' prose, with the
  other things that are true of one machine.

### `setup` makes the offer

[Section 4](../../skills/setup/SKILL.md) gains *Then offer to run it before the
push*, immediately after the sentence that establishes the precondition. It says
what it would write and **waits**; it argues push over commit on the reason
rather than the preference; it names the two exclusions in the same breath as the
offer, because the first adopter with an expensive suite will otherwise wire it
in; it says the hook takes the free checks **from the list the command already
reads**, never a second copy; and it says the thing gets no ledger row and that
nothing comes out of CI for it. **Declining ends it** — nothing written, nothing
recorded.

The `description` does not move. Nothing about the trigger changes: this is
behaviour inside a sitting that has already started, so it is paid for in the
body, where it costs nothing until `setup` fires.

**[`doctor`](../../skills/doctor/SKILL.md) is not touched, deliberately.** Its
section 0 says the checklist is `gates.md` and not itself, and that a second copy
of that list is the drift this plugin exists to stop. The rule that a hook is not
coverage now lives on that page, which is where doctor reads it from. Editing
doctor to restate it would have broken doctor's own instruction and staled two
more measurements to say the same thing twice.

### The Gherkin

One new feature,
[`specs/features/setup/before-the-push.feature`](../features/setup/before-the-push.feature),
`@feature:setup-before-the-push` under `@workflow:adopt-the-process`, with three
live rules:

- `@rule:a-local-run-is-offered-before-the-push` — offered, waits for an answer,
  at push rather than per commit;
- `@rule:what-costs-money-stays-out-of-the-hook` — the graded suite, and the
  check whose failure only a paid run can clear;
- `@rule:a-local-hook-is-not-a-gate` — no row in either table, nothing removed
  from CI.

All three are claimed by one new case,
[`26-two-seconds-before-the-push`](../../evals/26-two-seconds-before-the-push/prompt.md),
with a scaffold. It is a new case rather than another claim on `12`, which
`evals/README.md` has now warned about growing for two versions running.

### And this repository does it to itself

- **`.githooks/pre-push`** — one line, `exec verify.py --local`. Committed and
  inert: nothing runs until somebody types `git config core.hooksPath .githooks`
  in their own clone.
- **`verify.py` takes `--local`**, and names the one gate it drops in a constant
  beside `GATES`: `COSTS_MONEY = {"measurement board"}`. A stale board is healed
  by an eval run the maintainer approves and pays for, so it is correctly red
  here and correctly CI's to fail — a hook that could not tell that from a broken
  gate would refuse every push over an unpaid bill until somebody turned the hook
  off. The subset is derived from `GATES` so the hook holds no second list.
- **The bindings** get a *Before the push* row in *The table*, and a paragraph
  under *The wiring that must never gate* saying the hook is in neither table on
  purpose, and that `checks.yml` still runs `verify.py` whole.
- **`CONTRIBUTING.md`** names the one-line opt-in beside the commands.

### One correction picked up in passing

`specs/README.md` said *"Six live rules, all under `setup/`"* and *"the nine eval
cases"*. There are thirty-five and twenty-six. Both had drifted six versions —
the same defect [`0022`](0022-nobody-types-the-record.md) went after — and this
change adds three more rules to the same sentence. Fixed by removing the counts
rather than by recounting, which is the only fix that stays fixed.

## What we are not doing

- **No template.** A hook is two lines and a path; a `templates/` file for it
  would be payload in every install to save a sentence.
- **No `pre-commit`, and no offer of one.** The reporter said no, and the reason
  they gave is right.
- **Nothing in `doctor` beyond what `gates.md` already gives it**, above.
- **Nothing about CI, branch protection, or what blocks a merge.** The issue puts
  that out of scope and it stays out: this adds a signal and takes nothing away.
- **No gate holding the hook.** The hook is not a gate and neither is anything
  watching it; `inject.py` gains no fault, because there is no refusal to prove.

## Data

Nothing. No storage contract here, and what a version leaves behind is unchanged.

## Risks

**`always-green` is the one to argue, and it holds.** The hook runs on a
contributor's machine, only after they opt in, and only the command the
repository already defines. It is not installed by an agent session, it is not
reachable from CI, and a clone that never ran the config line has nothing. What
it can do is annoy somebody, and `--no-verify` is the answer to that.

**`--local` is a second way to run the gates, and a second way is a second
answer.** Mitigated by deriving it from `GATES` rather than listing anything: the
only new statement is which gate costs money, and it is one line beside the list
it filters. If a future gate is expensive in the same way, it is added to
`COSTS_MONEY` and nothing else moves.

**A hook that people bypass teaches them to bypass hooks.** This is the real
cost, and it is why the exclusions are stated as rules rather than as advice: the
first time a hook refuses a push for a reason the pusher cannot fix, they learn
the flag, and after that it is decoration. Keeping the board gate out of it is
that risk being taken seriously rather than mentioned.

**Nobody has watched this hook stop a push.** It is not in the ledger, so there
is no row to read *unobserved* — which is correct, and also means the usual
mechanism for tracking that is unavailable by design. The acceptance check below
is what stands in for it.

**Six measurements go stale and one case has never been measured.** Every
`skill:setup` case moves because the skill body did. The numbers are not run
here — that flag is the maintainer's signature — and the gap is left open below.

## Acceptance checks

1. `python3 .github/scripts/verify.py --local` is green and prints that it left
   `measurement board` to CI. `python3 .github/scripts/verify.py` runs all five.
2. `git config core.hooksPath .githooks`, break a rule's traceability, and
   `git push` refuses in about two seconds. `git push --no-verify` goes through.
   `git config --unset core.hooksPath` and the same push is unchecked.
3. `grep -rn "pre-push\|hooksPath" specs/setup/README.md` finds it in *The table*
   and in the prose under *The wiring that must never gate*, and in **no ledger
   row** in either table.
4. `.github/workflows/checks.yml` is unchanged, and `verify.py` there still runs
   the full five.
5. `grep -ric hook method/ skills/` is no longer zero, and what it finds says in
   the same paragraph what may never be in one.
6. Case `26` runs and its three outcome graders discriminate — the fixture's
   `make verify` is the attractive wrong answer, so a passing run is one that
   split it on cost and said so.

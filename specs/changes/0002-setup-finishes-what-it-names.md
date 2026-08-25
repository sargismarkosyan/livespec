# Spec 0002: setup finishes what it names

- **Status:** approved
- **Issue:** [#9](https://github.com/sargismarkosyan/livespec/issues/9)

## Who this is for

**The persona layer is empty**, and that is [#14](https://github.com/sargismarkosyan/livespec/issues/14)
rather than something this spec may fix — writing a persona is
[`refine-personas`](../../skills/refine-personas/SKILL.md)' work and its own
version. So the person is named here in plain words and attaches to the file
when it lands: **somebody adopting livespec into a repository that already has
work in it** — an existing CLAUDE.md, an existing gate, an existing way of
filing issues. Not the greenfield case. [`setup`](../../skills/setup/SKILL.md)
sections 7 and 8 both already assume the occupied repository is the common one.

**It names no workflow because there are none**, not because it serves nobody.
That is a different thing from the documented case in
[process.md](../../method/process.md#a-technical-change-that-serves-no-workflow-is-correct-not-a-gap)
— a change that honestly serves no attempt — and the distinction matters, because
this one gets a `@workflow:` tag the moment the layer exists.

The always-promise most at risk is **`never-implements`**
([spec.md](../spec.md#the-promises-that-belong-to-no-single-workflow)). This
change has one skill start three others in the same sitting; a chain of
interviews that still writes no application code is the thing that has to stay
true.

## The job behind the request

Come out of the setup sitting with a repository that is **running** the process —
not one holding a correct skeleton plus a list of things to remember to do.

## Why now

Reported from a real run against an occupied repository (`triage-review` inside
`sargismarkosyan/wf-developer-agents`). Three places where setup marked a step
done because it had been *named*:

1. The hand-back names `refine-personas` as "the one next thing" and stops. The
   human has to type the next command, and the loop pauses on a suggestion.
2. Nothing in sections 1–6 ever goes looking for **how issues are filed in this
   repository**, so [`claude-md.md`](../../method/claude-md.md) requirement #10
   is stated as a requirement and silently skipped. Every other requirement has
   something in the skill that produces it; #10 has nothing.
3. Where a CLAUDE.md already exists, step 6 is treated as done by the file
   existing. Nothing makes a pass over it against the ten requirements.

What it costs is the state setup's own section 3 warns about — a process that
"reads as installed and never run". **This repository is the standing example:**
its persona layer has been "the next thing to run" since 0.6.0, which is what
[#14](https://github.com/sargismarkosyan/livespec/issues/14) is about.

## The end value

After a setup sitting, the spec layer has been **started rather than scheduled**,
and CLAUDE.md either meets all ten requirements or the hand-back says which ones
it does not and why. The person is not carrying homework they have to remember.

**How we would know it worked:** two things that are checkable by looking. A
repository set up today ends the sitting with a persona file — or with a recorded
point where the human stopped the chain — instead of an empty `specs/personas/`.
And its CLAUDE.md carries a line naming the tracker that repository actually
uses. Neither is true of a sitting run against the skill as it stands.

## What changes

- **Section 1 gains one discovery item: how issues are filed here.** A tracker,
  a `CONTRIBUTING.md` line, an issue template, a `/feedback` command — whatever
  the convention is. "There is no convention" is an answer too, and it is
  reported rather than left blank.
- **Section 6 becomes an audit, not a write.** All ten requirements, one at a
  time, against what is on disk. An existing CLAUDE.md is read line by line and
  scored against the list — met, missing, stale — and the result is reported
  before anything is written. Requirement #10 is called out by name as the one
  nothing else in the skill will surface. Existence stops counting as done.
- **Section 8's hand-back continues into the layers.** Setup does not stop at
  naming `refine-personas`: it says up front that three interviews follow, then
  runs `refine-personas`, `refine-workflows` and `refine-journeys` in that order,
  in the same sitting. **Each stays its own interview, its own numbered change
  spec and its own confirmation** — the sittings are chained, the approvals are
  not, which is what [process.md](../../method/process.md) requires of a personas
  or workflows change. The human can stop the chain at any point, and the
  hand-back then says where it stopped and what is left.

**Rules added or changed** — the `@rule:` ids in `specs/features/`:

| Rule id | Feature file | New or changed |
|---|---|---|
| `setup-continues-into-the-layers` | `features/setup/hand-back.feature` | new — **owed** |
| `setup-finds-where-issues-go` | `features/setup/hand-back.feature` | new — **owed** |
| `setup-audits-an-existing-claude-md` | `features/setup/hand-back.feature` | new — **owed** |

**The feature file cannot land yet, and this is the reason.** `trace.py` fails
any feature naming no live `@workflow:`, and
[workflows/](../workflows/README.md) is empty — so the Gherkin for these three
rules is blocked behind [#14](https://github.com/sargismarkosyan/livespec/issues/14),
not omitted. The ids above are **reserved by this spec** and are permanent from
here; the file that carries them lands in the change that follows #14, with the
rules live rather than `@planned`, because by then the behaviour will already be
built.

## What we are not doing

- **Not filling this repository's own persona, workflow or journey layers.** The
  chain is what setup does in a consuming repository. Running it here is
  [#14](https://github.com/sargismarkosyan/livespec/issues/14)'s decision.
- **Not touching [`claude-md.md`](../../method/claude-md.md).** Requirement #10
  is already stated there. The gap is in the skill that executes it, and a rule
  stated in two places is a rule that gets edited in one.
- **Not the gate wiring ledger
  ([#11](https://github.com/sargismarkosyan/livespec/issues/11), shipped in
  0.7.0 while this was in review), and not the `rule()` helper or the spec-bound
  coverage pass ([#13](https://github.com/sargismarkosyan/livespec/issues/13)).**
  Both are their own issues against the same file. What this change owes the
  ledger is one line: a skill in the chain that stops itself on a row deferred
  twice ends the chain there, and that is the ledger working.
- **Not teaching setup to file anything.** It records where issues go; it does
  not learn to post there. The tracker assumption inside `feedback` is
  [#10](https://github.com/sargismarkosyan/livespec/issues/10).
- **Not the offer-shaped hand-off** — setup asking "shall I start
  `refine-personas`?" and stopping on silence was the alternative considered.
  Rejected in favour of the chain, on the grounds that an offer is the same pause
  with a question mark on it. The cost is in *Risks*.
- **Not a new eval case.** See *Risks*.

## Data

None. There is no storage contract here — the plugin ships prose, and what a
version leaves behind is listed in [spec.md](../spec.md#what-a-version-leaves-behind).

## Risks

- **The sitting gets long.** A setup pass plus three interviews is a lot of one
  conversation. Mitigated by announcing the chain before it starts and stopping
  the moment the human says so. If people stop at personas every time, that is
  evidence the offer-shaped hand-off was right, and it comes back as feedback.
- **Approval fatigue is the real cost of chaining.** The rule that a personas or
  workflows change is confirmed on its own now gets exercised three times in one
  sitting. The chain does not merge those confirmations and each refine-\* skill
  still asks for its own — but a tired reader waving three through is the failure
  mode this trades for the loop moving, and it is taken deliberately.
- **`never-implements` is unmoved.** Nothing in the chain writes application
  code; every skill it starts already refuses to.
- **This behaviour ships unheld by an eval case, on purpose.** `setup` carries
  `disable-model-invocation: true`, so a fire case would have to be driven by a
  literal `/livespec:setup` in the prompt — and `claude plugin eval` is gated
  behind early access, so whether the runner accepts that cannot be checked. A
  case nobody can confirm is drivable is worse than an honest gap.
  [`09-neg-setup-not-self-started`](../../evals/09-neg-setup-not-self-started/prompt.md)
  stays setup's only case. **A driven-setup case is the first thing to write when
  the runner unblocks.**

## Acceptance checks

Run `/livespec:setup` against a repository that already has a CLAUDE.md and an
existing way of filing issues.

1. The hand-back lists which of the ten CLAUDE.md requirements the existing file
   meets and which it does not — and does not report the file as done because it
   is there.
2. CLAUDE.md ends the sitting with a line naming where issues actually go in that
   repository.
3. The sitting says three interviews follow, then continues into
   `refine-personas` without anybody typing the command.
4. Say "stop" partway. The chain ends there and the hand-back names what is left.
5. Nothing under that repository's source tree changed.

# Spec 0072: a cheap tier holds every edit; the sitting is a canary

- **Status:** approved — by the maintainer on 2026-09-27, holding the deck
  *Cheaper skill evals* ("I like it, please implement")
- **Issue:** none — the maintainer, on the suite's upkeep

## Who this is for

The maintainer, who pays for every measurement and has said, twice, that the
suite cannot be kept up at this price. Serves no workflow: this is the
measuring apparatus, and it says so.

## The job behind the request

*"We will not be able to maintain it, it's way too expensive to execute once
anything is changed."*

[`0070`](0070-half-a-row-goes-stale-not-a-whole-one.md) halved what a skill
edit cost and [`0071`](0071-one-judge-call-per-session-not-per-rubric.md)
batched the judge. Both made the same thing cheaper: **a whole sitting, owed on
every edit.** The job is not a cheaper sitting. It is being able to change a
skill and know, the same afternoon and for a few dollars rather than tens, whether
it still does what its rules promise, without that knowledge being fake.

## Why now

From the board and the grader files, 2026-09-27:

| | |
|---|---|
| a full run | 70 cases × 2 arms × 3 runs = **420 sittings**, ≈ $200 |
| on the board | $188 spent over 50 rows — **every one stale** |
| one skill-body edit | 6 cases, with-arm only ≈ **$9** |
| one case alone | `12`, $29.31 |
| the graders | 271: 70 skill-fired indicators, 34 rubrics on the last message, 54 regex, 16 command, **97 rubrics on the whole transcript** |
| real use | **52 sessions** in `toil-tracker` already called a livespec skill: `refine-spec` 44 times, `record-clip` 29, `todo` 11, `doctor` 11 |

The judge is not what costs. The sitting is: Claude Code's system prompt, a
scaffolded world, many turns, a person, three runs. And a good share of what
the graders ask needs far less than a sitting: whether the right skill loaded
at all, and what the first reply does with the request.

## The end value

An edit to a skill's body is measured for about $3.40 where it cost $9, a
description edit for about $8, and the board's freshness gate can be cleared by the person who made the
edit without a budget meeting. Nothing reads more true than it is: the
sittings stay, are shown as stale when they are, and are never averaged or
owed while stale.

**How we would know it worked:** the next skill edit's `tiers.py --changed`
refusal quotes under $4, and its run completes in one sitting of the account's
limit with room to spare.

## What changes

**Three tiers, in `evals/runner/tiers.py`, one call each.**

- **`route`** — one real turn of `claude -p`: Claude Code's own system prompt,
  the plugin loaded, only the `Skill` tool, one turn, in the case's world.
  Right when a skill the case holds fires, or — for a should-not-fire case —
  none of ours does. Three turns a case. Hashed on the case's files and **every
  skill's frontmatter**, so a description edit stales every routing row and a
  body edit stales none.
- **`first`** — one reply to a snapshot: the case's world laid down by its
  scaffold and shown as already read (with `git log` when it is a repository),
  the skill's body as already loaded (with-arm only), the prompt. A system
  prompt of our own, no tools. Judged by the case's **own llm rubrics** in one
  call, each marked as applying or not — a rubric only a later turn, a file on
  disk or a command could decide is marked not applying rather than failed. A
  rubric counts for the case when it applied in at least half the sessions,
  both arms together. Three replies an arm, **both arms**, so Δ survives.
  Hashed exactly as the canary's arms are (`measurement_inputs`), so a body
  edit stales the with-arm only, and on the rubrics.
- **`review`** — one reading of a skill's whole file beside the text of every
  rule the cases holding it claim: `held`, `weakened` or `missing`, quoted.
  Hashed on the skill and those rules.

**The board gains `route`, `first` and `review` sections**, each row with its
inputs hash, model, judge, cost, runs and a fingerprint of `tiers.py`.
`caselib.tier_why_stale()` decides staleness for the gate and the runner.

**The board gate moves its freshness to the tiers.** A stale tier row fails
(exit 2 through `verify.py`, as a stale row always has); a missing one warns. A
stale **canary** row — the sittings, `cases` — now **warns**: shown as stale,
left out of the canary's mean, owed by nothing. A canary case never sat is a
note.

**`tiers.py` is held like `run.py`**: refuses without `--i-approve-the-cost`,
asks `caselib.replaces()` before writing, defaults `--model` to
`caselib.SESSION_MODEL`; `evalsuite.py` fails any of them going missing, and
`evals/README.md` no longer documenting `tiers.py --changed`. A call the
account's limit refuses stops the run (exit 3) with every finished row written.

**The sessions already had.** `tiers.py --transcripts` reads
`~/.claude/projects` (not this repository's own), finds each livespec firing,
cuts it from the person's request to the next firing, and judges it against the
rules its skill answers for: held, broken, not tested. It reads each session's
messages for turns where a skill should have fired and did not. Judge calls
only; each firing graded once; results local in `evals/results/transcripts/`,
never on the board.

**Prose.** [`method/graded-cases.md`](../../method/graded-cases.md) gains *Gate
the freshness of what you can afford to keep fresh*, portable: two speeds, each
cheap measurement fingerprinted by what it can see, the faithful one shown and
never owed while stale, calibration of one against the other, and real sessions
as evidence kept local. `evals/README.md`, the bindings, `CLAUDE.md`,
`CONTRIBUTING.md` and `verify.py`'s note say where the freshness now lives.

## What we are not doing

- **Not deleting a single case or sitting.** The canary is the only thing that
  sees an interview through or a gate actually wired, and the tiers are
  believed only where they agree with it.
- **Not gating the canary's age.** Nothing can be owed that cannot be afforded;
  a stale sitting is shown, not failed. When the model moves it is due, and the
  README says so rather than a gate.
- **Not an API key.** Every call is `claude -p` on the maintainer's account,
  as the sittings are: one billing path, no credentials, standard library.
- **Not Haiku for the tiers.** The model under test is the one the bindings
  name; a cheaper model would be a measurement of a product nobody runs.
- **Not a hand-built router.** Routing is the one place Claude Code's own
  system prompt is the thing under test, so the routing turn keeps it.
- **Not putting real sessions on the board.** A row describes the files as they
  stand; a real session describes them as they stood.
- **Not converting rubrics to first-move rubrics.** The judge marks what does
  not apply; editing 131 rubrics would stale every row for a guess about which.

## Data

`evals/board.json` gains three top-level sections beside `cases`:

```json
"route":  {"<case>":  {"expected", "fired": [...], "hits", "runs", "score", "cost", "model", "inputs", "harness", "at", "sha"}},
"first":  {"<case>":  {"with", "without", "delta", "runs", "applicable", "rubrics": {"<grader>": {"with": {"pass", "applies", "n"}, "without": {...}}}, "cost", "model", "judge", "inputs", "inputs_without", "graders", "harness", "at", "sha", "carried"?}},
"review": {"<skill>": {"held", "rules", "not_held": [{"id", "verdict", "reason"}], "cost", "judge", "inputs", "harness", "at", "sha"}}
```

`board.py --json` gains `tiers` and `canary`; its top-level `measured`,
`stale` and `never` now count tier rows, and `mean_delta` is the first moves'.

## Risks

**A snapshot is not a session.** The first-move reply is written under a system
prompt of ours, about a world it was handed rather than explored, and it may
narrate where a session would act. The judge's *applies* is the guard against
scoring that as failure; the calibration read in `evals/README.md` — the same
cases both ways, verdict by verdict — is the guard against believing it where
it disagrees with a sitting. Until that read is done, a first-move Δ is a
direction.

**The judge decides applicability.** A judge that marks too much as not
applying makes every case easy. The row carries `applicable`, so a case whose
rubrics mostly stopped applying is visible; the calibration read looks at it.

**The canary may simply stop being run.** That is the cost of not owing it. The
README names when it is due — the model moves, a tier is being calibrated —
and the board keeps showing how many sittings are stale.

**The bootstrap is not free.** Every tier row starts empty: about $72 for all
three tiers at the smoke run's prices, and about $13 for the 104 real firings. It is the
maintainer's to approve, like any run.

## Acceptance checks

1. `python3 evals/runner/tiers.py --changed --scaffold` refuses with exit 2,
   naming the rows and a price, and spends nothing.
2. `python3 evals/runner/tiers.py --transcripts` refuses the same way, after
   finding the firings on this machine for free.
3. `inject.py`'s tiers control passes against the stand-in `claude`: routing,
   both arms of a first move, a review, rows written and fresh, a pilot
   refused a measurement's row, a body edit leaving routing fresh while a
   description edit stales it, the limit read, a real session's firing graded.
4. The board faults fire: a stale tier row fails for its inputs, a description,
   a body, a rubric, a model and a harness; a missing tier row warns; a stale
   canary row warns rather than fails.
5. The suite faults fire: `tiers.py` without its refusal, without
   `replaces(`, without the model default, and undocumented.
6. `python3 .github/scripts/verify.py` is green, with every tier row warned as
   never measured and the canary's fifty stale rows shown and not owed.

## The smoke run, 2026-09-27

Approved by the maintainer, one call a row: `route` on `01` and `06`, `first`
on `01` in both arms, `review` of `refine-spec`. **$0.62**, four rows, all
written; the real CLI took every flag as the stand-in does.

| | |
|---|---|
| `route 01` | fired `refine-spec` — right; $0.041 |
| `route 06` (should-not-fire) | fired nothing — right; $0.039 |
| `first 01` | with 1.00, without 1.00, Δ +0.00 over its one rubric; $0.36 for two replies and two verdicts |
| `review refine-spec` | 3 of 4 rules held; `the-job-is-found-under-the-request` **weakened** — the skill never says to ask and write nothing when the job cannot be told from the request; $0.18 |

**The first calibration finding is in `first 01`'s bare arm.** The canary
scored that arm 0.00 over three sittings. Here the bare reply drafted the
button's spec and Gherkin on its first move, and the judge passed it on
`finds-the-job` for a "so that" clause. The rubric says a reply that "simply
accept[s] the button as the requirement and move[s] to how to build it" fails.
One sample, and it is the leniency *Calibrating a tier against the canary*
exists to catch: the first-move judge is not trusted on `01` until the read is
done, and a first reply costs about twice the guess this spec was approved on,
which the figures above now use.


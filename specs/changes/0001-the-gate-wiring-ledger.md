# Spec 0001: The gate wiring ledger

- **Status:** proposed
- **Issue:** [#11](https://github.com/sargismarkosyan/livespec/issues/11), with
  [#7](https://github.com/sargismarkosyan/livespec/issues/7) closed into it

## Who this is for

**Not a persona — [personas/](../personas/README.md) is empty**, and this change
does not get to invent one. The person it is for is the one in the issue: they
ran `/livespec:setup` on a repository that already had a features↔tests trace
gate, and then landed personas, journeys and workflows in three separate change
specs months later. Naming them properly is
[`refine-personas`](../../skills/refine-personas/SKILL.md)'s work and
[#14](https://github.com/sargismarkosyan/livespec/issues/14)'s queue; this spec
says so out loud rather than filing itself under a workflow to fill the box —
see [process.md](../../method/process.md#a-technical-change-that-serves-no-workflow-is-correct-not-a-gap).

It serves no workflow because **the workflow layer does not exist**, which is a
different fact from serving nobody. When the layer lands, this belongs to the
attempt "adopt the process in a repository that already has one" and to the seam
after it — the months where layers arrive one at a time.

## The job behind the request

Not "write a log file". The job is **knowing, later, whether the specification
here is still actually being checked** — and being told when it stopped, rather
than reconstructing it from four files that each hold one honest quarter of the
answer.

The trigger was landing the third layer. `specs/personas/README.md`,
`specs/workflows/README.md` and `specs/journeys/README.md` each correctly
self-reported "not automated yet" for its own half of the gate. Nothing added
them up. The workaround is what the reporter did: read all four files and OR them
together in their head, every time, and take the result on trust in between.

## Why now

Three consecutive change specs (0005–0007 in `wf-developer-agents`,
`triage-review/`) each said *flagged, not built*, and nothing ever closed the
loop. That is a repository carrying an honestly-flagged, perpetually-unbuilt gate
while looking green — the failure this plugin exists to prevent, one level up:
not a spec that quietly stopped being true, but **the check on it** that did.

There is a sharper edge underneath. Every `refine-*` skill states its gate as
fact — `refine-personas` §4 *"The gate runs both ways"*,
`refine-workflows` §5, `refine-journeys` §6 — each printing a table of errors.
In that repository those tables were **false**: `setup` had wired the
features↔tests half and nothing else, correctly, because at the time nothing else
existed. The skills had no way to notice, and no way to say so. A skill asserting
a gate that nobody wired is worse than a missing gate, because it is read as
confirmation.

## The end value

One table, in the file every skill already reads, that answers *is this gate
wired, and if not, since when and why* — for every gate the method names. A
`refine-*` run reads it, checks it against what the layers actually contain now,
records the row it just made applicable, and cannot hand back quietly on a second
deferral. A later `setup` run diffs the plugin version stamped on that table
against its own and offers the upgrade instead of re-deriving the state.

**How we would know it worked:** the reporter's sequence stops at the second
change spec instead of the third. A deferred row cannot survive two changes
without somebody either wiring it or writing down, in the ledger, that it is
deliberately not automated and why.

## What changes

Behaviour of the skills, visible in the files they write into a consuming
repository:

- **`setup` writes a *Gate wiring* section** into `specs/setup/README.md`: one
  row per gate named in [gates.md](../../method/gates.md), each marked
  `automated` (naming the command that runs it), `not applicable` (with the
  reason), or `deferred` (since which change, and why) — plus the date and the
  plugin version the wiring was last reconciled against.
- **A `setup` re-run diffs that section rather than overwriting it.** It reports
  which rows the current method expects and the repository does not have, and
  offers the upgrade. Rows it cannot date honestly say *predates the ledger*
  rather than getting a made-up change number.
- **`refine-personas`, `refine-workflows` and `refine-journeys` read the section
  before asserting their gate tables**, and cross-check it against the tree: a
  row reading *not applicable — no personas exist* while persona files exist is
  a contradiction, and the skill says so instead of restating the table as fact.
- **The skill that lands a layer updates the rows it just made applicable**, in
  the same change as the layer.
- **A row deferred across two changes stops the skill for a decision** — wire it,
  or record it as deliberately not automated with the reason. Not a third
  *flagged, not built*. This is the same norm
  [gates.md](../../method/gates.md) already holds for warnings, applied to the
  gates themselves.
- **`method/gates.md` gains what the ledger has to mean** and that norm. Portable
  prose only: what a row asserts, the three states, and the two-change limit.
- **The version stamp is setup-level, and says so.**
  [spec.md](../spec.md) keeps its promise that nothing records which version of
  the method built a given *commit*; the ledger records what the *wiring* was
  last reconciled against, which is a fact about the installed process rather
  than about any commit. That distinction is written into `spec.md`,
  `method/README.md` and `CONTRIBUTING.md`, which all three carry the promise
  today.
- **This repository gets its own row set.** livespec ran `setup` on itself, so
  its bindings carry the ledger like any other consuming repository's — including
  the honest rows: coverage is not applicable here and the reason is already
  written down.

**Rules added or changed** — none can land yet. A `.feature` file must name a
live `@workflow:`, `specs/workflows/` is empty, and filling it is
[#14](https://github.com/sargismarkosyan/livespec/issues/14)'s job in another
branch. The rules this change would write, with their ids reserved so they are
stable when they land:

| Rule id | Feature file | New or changed |
|---|---|---|
| `gate-ledger-written-at-setup` | `features/setup/gate-ledger.feature` | new, blocked on #14 |
| `gate-ledger-rerun-diffs` | `features/setup/gate-ledger.feature` | new, blocked on #14 |
| `gate-ledger-cross-checked` | `features/refine/gate-ledger.feature` | new, blocked on #14 |
| `gate-deferral-expires` | `features/refine/gate-ledger.feature` | new, blocked on #14 |

Held instead by an eval case, which is what a rule is claimed by here — a case
may claim no rule while the layer is empty, and
[the bindings](../setup/README.md) say why. The case moves onto the rule ids the
moment the feature file can exist.

## What we are not doing

- **No new gate script, and nothing that can fail a build.** The ledger is prose
  an agent reads. `always-green` in [spec.md](../spec.md) is not negotiable: a
  plugin is available to an agent, not to a build runner.
- **The ledger is not generated.** [gates.md](../../method/gates.md) says the map
  of what implements what is generated, never typed — and it is right. This one
  is typed, because a record of what is *not* automated cannot be produced by the
  automation that does not exist. What stops it drifting is the cross-check
  above: the tree is the authority on what is *applicable*, the ledger only
  carries what is wired and why a gap is open.
- **No per-commit provenance.** Considered and dropped: the stamp answers "what
  was this wiring last checked against", never "which version wrote this line".
- **No dedicated `specs/setup/gates.md`.** Considered: it separates an
  append-updated ledger from a written-once reference. Dropped because every
  skill already reads the bindings before assuming a command, and the
  fault-injection record there is already exactly this kind of dated ledger —
  a second file is a second read, a link that can rot, and one more thing for a
  `setup` re-run to find.
- **The `refine-*` skills do not wire gates.** Considered as the strongest
  forcing function — the skill that lands a layer builds that layer's gate half
  before handing back. Dropped: gate wiring is `setup`'s job, and pushing it into
  three interview skills widens all three for a job one of them already owns.
- **No `description` is widened.** Every edit is in a skill body. The always-on
  budget does not move, so nothing here is paid for by every session.
- **`refine-spec` and `feedback` gain nothing.** Neither lands a layer, and a
  ledger step in a skill that cannot change a row is a step that gets skipped and
  then ignored elsewhere.

## Data

The storage contract here is *What a version leaves behind* in
[spec.md](../spec.md), and this adds one thing to it: a table in a consuming
repository's `specs/setup/README.md`.

Repositories already set up by an earlier livespec have no ledger. They are not
migrated and nothing backdates them — a `setup` re-run writes the section from
what is in the tree **today**, and every row it cannot date honestly reads
*predates the ledger*. An invented "deferred since 0003" would be the first lie
in a file whose whole job is to be the one place that is not guessing.

## Risks

- **`always-green`** — the promise most at risk, and the reason nothing here is a
  script. If a future change turns the ledger into something CI reads, that is a
  change to what livespec is and gets argued as one.
- **`context-budget`** — bodies grow. `setup` is `disable-model-invocation`, so
  its body costs nothing until someone types the command; the three `refine-*`
  bodies load only when they fire. Held to roughly a dozen lines each; if a
  section needs more than that, the method doc is where the length belongs.
- **A stop that always fires becomes wallpaper.** The two-change limit fires once
  per row, and recording a row as deliberately not automated closes it for good.
  If it starts firing on every run, it has become a warning that survived two
  versions, and the same norm applies to it.
- **A repository where nobody can change CI.** `setup` §2 already handles the
  unenforceable rule; the ledger must be able to say *not applicable — no CI
  here, and nobody can add one* as a permanent state rather than a deferral that
  can never expire.
- **The typed ledger going stale anyway.** Mitigated, not eliminated. The
  cross-check catches a row that contradicts the tree; it cannot catch a row that
  is merely out of date about a command that got renamed.

## Acceptance checks

There is no app and no moving picture — a version's deliverable here is the pull
request description. This is what the human does by hand:

1. `python3 .github/scripts/verify.py` — green, warnings read rather than
   skimmed.
2. Read the *Gate wiring* section this change adds to
   [specs/setup/README.md](../setup/README.md) against
   [gates.md](../../method/gates.md): every gate the method names has a row, no
   row is invented, and every `not applicable` carries its reason.
3. Read the `spec.md` / `method/README.md` / `CONTRIBUTING.md` diffs together and
   confirm the three still say the same thing about version provenance.
4. Read the new eval case's prompt and graders and answer: would this have failed
   before the change? A case that passes either way is holding nothing.
5. The real check is in the other repository — next time `refine-workflows` runs
   on `triage-review`, it should report the ledger state rather than restating
   its gate table as fact.

# Spec 0013: the board of latest measurements

- **Status:** approved
- **Issue:** [#39](https://github.com/sargismarkosyan/livespec/issues/39)
- **Depends on:** [0012](0012-a-runner-that-runs.md) — there is nothing to
  record until there is a runner that runs.

## Who this is for

[`@persona:agent-accelerated-owner`](../personas/agent-accelerated-owner.md).
Two lines of that file decide this design: they *read what a gate prints*, and
what they want is *to stop supplying what the repository already says*. Whether
the skills got better or worse since last time is something the repository
should say, and today it cannot — the answer lives in one machine's promptfoo
history and in nobody's head.

Livespec's own infrastructure throughout; no workflow is served and
[process.md](../../method/process.md#a-technical-change-that-serves-no-workflow-is-correct-not-a-gap)
says that is correct, not a gap.

## The job behind the request

The literal ask, in the maintainer's words: *"something to check the latest
eval results, to see the overall quality — basically when rule or eval case has
changed we can enforce to run it and have updated run data — don't full
pipeline, just what changed."*

Three jobs in one sentence, and they define the whole change:

1. **See the latest state, per case** — not a log of runs, a board of what each
   case last measured.
2. **Re-run only what changed** — the suite costs money per session; a rule
   reworded should cost re-measuring the cases that claim it, never all sixteen.
3. **Enforce it** — a case whose inputs changed while its measurement stood
   still is a stale number wearing a fresh face, and nothing should merge on it.

## Why now

[`0012`](0012-a-runner-that-runs.md) produced the first measurement the suite
has ever had — and threw it away, because `evals/results/` is gitignored on a
decision written before any run existed: *"a measurement of one moment, not a
record the repository keeps."* That decision was right then and is half-wrong
now: right about the transcripts, wrong about the summary. Each Δ is currently
compared against nothing.

## The end value

Open one committed file and know, per case: the last Δ, both arms' scores, when
it was measured, at what commit, and — the part nothing else can say —
**whether that measurement still describes the current files.** When a rule, a
case or a skill moves, the affected cases go visibly stale, CI refuses to ship
them stale, and one command re-runs exactly that set.

**How we would know it worked:** edit one grader, watch `verify.py` name that
one case and print the one command that heals it, run it, watch the board
update and the gate go green — while the other fifteen cases were never run and
never blocked anything.

## What changes

**The board — `evals/board.json`, committed.** One entry per case: `delta`,
`with`, `without`, `runs`, `at`, `sha`, `cost`, and the **measurement inputs** —
a hash over what the number was a measurement *of*: the case's own files, the
text of every rule it claims, and the body of every skill it holds. The user
named rules and cases; skills are added because the suite exists to hold skill
changes — a measurement that survived a skill edit unexamined is the staleness
that matters most.

**`run.py` records and scopes.**

- Every completed run updates the board entries for the cases it ran —
  automatic, no flag to forget. A `--case` smoke updates one entry; the entry's
  own `runs` field says how much weight it deserves.
- New `--changed`: compute the stale set — inputs-hash mismatch, or never
  measured — and run exactly those cases. This is *"don't full pipeline, just
  what changed"* as a flag.
- The hashing lives in `caselib.py`, next to the case reader, so the runner and
  the gate cannot disagree about what a measurement covers — the same argument
  that put the reader there in 0008.

**The staleness gate — `board.py`, gate five.** Stdlib only, wired into
`verify.py` and proven to fire by new `inject.py` faults:

- a case whose current inputs-hash mismatches its board entry **fails** — a
  rule, case or skill changed and nobody re-measured. The failure names the
  case and prints the healing command.
- a case with no board entry **warns** — the bootstrap state; all sixteen start
  here, and a warning that lists them is the to-do list for the first pilot.
- **the score is never gated.** A Δ of zero ships; a stale Δ of one does not.
  This is `method/testing.md`'s reported-never-gated line applied one level up:
  gate the bookkeeping, never the number.

**The report grows one row.** `report.py` reads the board at head and base and
prints measured / stale / never-run counts and the mean Δ over measured cases,
dated — a pull request rarely re-runs the suite, and the row must say so rather
than look current. Reading a committed file, recomputing nothing, gating
nothing: exactly what `method/gates.md` already requires of it.

**Docs.** `evals/README.md` gains the board section (and the results-directory
paragraph stops implying nothing survives a run); `.gitignore` keeps ignoring
`evals/results/` — the transcripts and workspaces stay local, the summary is
what gets kept; the bindings name the board and the gate.

**Rules added or changed:** none. Livespec-local machinery; if a consuming
repository ever wants a board, that is `setup`'s change with its own spec.

## What we are not doing

- **Not committing runs.** No transcripts, no `results.json`, no sessions. The
  board is the summary; the evidence stays local and reproducible.
- **Not gating on the score**, in any direction, ever. Stated twice because it
  is the first thing a future change will be tempted to do.
- **Not requiring the full suite.** The opposite: partial re-measurement is the
  feature. The floor (`runs: 3`) still applies to a *trusted* number; a smoke
  entry is visible as a smoke by its `runs` field.
- **Not putting the board in consuming repositories.** `setup` does not learn
  about it in this change.
- **Not failing on never-measured.** Warns until the first pilot fills the
  board; whether it should ratchet to fail afterwards is a later, one-line
  decision recorded here as open.

## Data

- `evals/board.json` is versioned data with a `format` field, so the shape can
  move without archaeology.
- The inputs-hash is content-addressed (file bytes, rule text, skill body) —
  never mtimes, never git metadata — so two machines agree about staleness.
- `sha` records provenance of the measurement; it does not participate in
  staleness. Rewording a README does not stale anything.

## Risks

- **Judge noise shakes the board.** Re-measuring unchanged prose can move Δ;
  the board records latest, not best, and a jitter can look like a regression.
  Mitigation: `runs` is recorded per entry, and the calibration rule stands —
  no number is acted on before its verdicts are read.
- **Enforcement makes skill edits cost money.** Every SKILL.md change stales
  its cases; merging then requires a local paid run of them. This is asked for
  — *"we can enforce to run it"* — and it is the method's own discipline
  (descriptions are paid for in evals/), but it is a real toll named plainly
  here rather than discovered at the first red build.
- **The board can be hand-edited green.** A hash is not a signature; someone
  can paste hashes without running anything. The gate proves freshness of
  bookkeeping, not honesty of numbers — same trust model as every other file
  in the repository.

## Acceptance checks

1. `python3 .github/scripts/verify.py` green; `inject.py` proves the new gate
   fires both ways (stale fails, unmeasured warns) — faults 34 → 36 at least.
2. The end-value walk, literally: touch a fixture grader, see the named case
   and the healing command, run `--changed`, see green.
3. The smoke entry from a real `--case 01 --runs 1` run sits in the board with
   `runs: 1` visible, and `git status` shows only `evals/board.json` changed.
4. `report.py` renders the row from a board with mixed measured/stale/never
   states, and exits 0 with the board missing entirely.
5. The score-is-never-gated sentence appears in the gate's own failure text or
   docstring, so the temptation meets the refusal where it will be felt.

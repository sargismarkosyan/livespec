# Spec 0032: the repository does not know it is owed one

- **Status:** proposed
- **Issue:** [#78](https://github.com/sargismarkosyan/livespec/issues/78), returning.
  The sketch shipped into one skill body and into nothing a repository keeps.
- **Depends on:** [`0029`](0029-drawn-before-it-is-built.md), which introduced the
  sketch. Independent of [`0031`](0031-a-missing-tool-is-not-a-missing-page.md) —
  that one is about the session's mechanism, this one about the repository's
  record, and either can ship first.

## Who this is for

[`agent-accelerated-owner`](../personas/agent-accelerated-owner.md), in
[`adopt-the-process`](../workflows/adopt-the-process.feature) — but not at step 4
this time. **At the seam between having adopted the process and the process
moving on underneath them**, which is the situation the whole `doctor` skill
exists for.

The persona line is the one at the top of the file: *more than one repository at
once.* Every repository they run this in was set up on the version that existed
that week. There are several. A requirement added on 2026-09-01 reaches the
skills in all of them on the next `/plugin update` and reaches the *record* in
none of them, and nothing about that is visible from inside any one repository.

The other line that decides this: *they read the spec layer and not the
documentation.* Whatever carries this has to be in the files they open and the
files a skill is required to read, not in a release note.

## The job behind the request

Have a repository that adopted the process a month ago still be running the
process as it now is — without reading a changelog to find out what moved.

## Why now

Because the artefact this is about is the one they singled out as the thing they
wanted most, and it arrived by luck.

The sitting they quoted is `toil-tracker`'s spec 0037. The sketch was published,
they read it, and they said so. **Nothing in that repository asked for it.**
`refine-spec` carried the instruction and that session happened to have a tool
that publishes pages. Their own words on what is missing:

> most of the implementations of the livespec which used the old setup and
> doctor does not include this artifact, during the approval of what will be
> built

That is checkable, and it checks out. Read on 2026-09-02:

- The sketch shipped in **0.27.0, on 2026-09-01**.
- `toil-tracker`'s bindings are stamped *"Reconciled against livespec **0.25.0**
  on **2026-08-30**"* — two versions and two days before the sketch existed. The
  word *sketch* appears **0 times** in its bindings and **0 times** in its
  `CLAUDE.md`.
- `todo-change`: **0** and **0**.
- `toil-tracker`'s `CLAUDE.md` walks the loop, and its step 4 reads in full:
  **"Human approves, or asks for changes."** That file is loaded by every
  session in that repository. The method's own step 4 has said *holding the spec
  and the sketch drawn from it* since 0.27.0.

**And the bindings there do not merely omit it — they contain the sentence that
argues against it.** `toil-tracker`'s deliverable section carries the picture's
exemption, *"**A line of text** is right when there is nothing to see"*. A
session reading the bindings for what this repository owes finds that and finds
nothing else. This repository had to head off exactly that confusion in its own
bindings, in as many words — *"The sketch is not covered by that exemption, and
does apply here"* — because the two are one word apart. Every repository set up
before 0.27.0 has the exemption and not the fence.

**`doctor` is the skill this belongs to and it has no line for it.** Its section
3 already carries the pattern, for the two things that can never gate: *"Neither
can fail a build, so neither ever announces its own absence. Check the second
table exists and holds both; where the bindings predate it, that is the offer to
make."* A sketch can never fail a build either. It is a third item on a list that
already exists, and it is not on it.

## The end value

Running `doctor` in a repository set up before the sketch existed comes back with
it as an open item and the row written — so the next `refine-spec` sitting there
reads *this repository owes a sketch* in the file it is already required to read
first, instead of depending on which tools that session happens to have.

**How we would know it worked:** `doctor` in `toil-tracker` names it, and after
the correction the word appears in its bindings where it appears zero times
today. The behavioural signal is one step further out — a sketch arriving in a
repository whose sittings were not producing one.

## What changes

- **`setup` writes the sketch into the bindings**, beside the row it already
  writes for what a version must show. Which changes here owe one before
  approval, and that it is drawn from the change spec rather than recorded from
  the app.
- **A repository with nothing on a screen writes that it still owes one.** This
  is the half that gets lost: the *nothing to see* line is the picture's, the
  sketch is drawn from a spec, and a repository with no app still has change
  specs. Where the bindings record a standing exemption for the picture, they
  record beside it that it does not reach this.
- **`setup`'s `CLAUDE.md` audit checks the approval step.** Where that file walks
  the loop, step 4 says what the person holds. A repository whose own account of
  the loop stops at *human approves* is describing the process as it was before
  0.27.0, to every session that opens it.
- **`doctor` gains the third structural item in section 3**, on the same footing
  as the pull-request report and the rule-bound measure: it can never fail a
  build, so nothing announces its absence, and the audit is the only place it
  surfaces. Where the bindings predate it, the row is offered as it will read.
- **The picture row is not read as covering it.** `doctor` reports them as two
  rows, because a repository that has one and not the other looks, at a glance,
  like a repository that has been asked this question already.

**Rules added or changed** — the `@rule:` ids in `specs/features/`:

| Rule id | Feature file | New or changed |
|---|---|---|
| `the-bindings-say-a-sketch-is-owed-here` | `features/showing/owed-in-this-repository.feature` | new, `@planned` |
| `what-arrived-after-the-bindings-were-written-is-caught` | `features/showing/owed-in-this-repository.feature` | new, `@planned` |

`the-bindings-say-what-a-change-here-must-show` is untouched. It is the picture's
row and it stays the picture's row; the confusion this change is about is what
happens when a reader takes it for both.

### Why this is one change and not two

`setup` and `doctor` are two skills and this moves both, which normally splits.
It does not split here: the requirement is *the repository records that a sketch
is owed*, and the two skills are the two ways a repository can come to hold that
record — written at the sitting, or found missing at the audit. Shipping either
alone leaves the other half saying the process is fine. And the cost below is
paid per skill touched, not per version, so splitting buys two versions and no
saving.

## What we are not doing

- **Teaching `doctor` to compare the ledger's stamp against the installed
  version.** This is the durable version of the fix — *your bindings say 0.25.0,
  the plugin here is 0.28.0, here is what a repository owes that it did not
  then* — and it would have caught this one without being told. It is also its
  own design problem: something has to say what each version *obliges a
  repository to hold*, and a changelog read as a to-do list is a worse answer
  than no answer. Worth its own spec, and worth it soon; this change is what the
  reported gap needs today.
- **Auditing whether a sitting actually drew one.** Unchanged from
  [`0031`](0031-a-missing-tool-is-not-a-missing-page.md) and from the issue that
  raised it: `doctor` reads repository state, and an instruction skipped inside a
  session leaves none. What this change does is give it repository state to read.
- **Making it a gate.** Nothing can check whether a sketch carried evidence, and
  a gate that checks a row exists would be satisfied by a row somebody typed.
  Same reasoning as the report and the rule-bound measure, which is precisely why
  it belongs on their list rather than in the gate table.
- **`doctor` correcting `CLAUDE.md`.** Its subject is `specs/setup/README.md`,
  and widening it to a second file widens what "the record" means for a skill
  whose whole safety comes from not building anything. `setup` already audits
  that file and that is where the loop step goes.
- **Backfilling the repositories by hand.** They are somebody else's tree. What
  ships is a `doctor` that says so when it is run there.
- **A new skill, or any description widening.** Both skills already fire on
  exactly the request that needs this. Body text only.

## Data

No storage contract moves. `specs/spec.md` needs no new vocabulary — **sketch**
and **picture** are already separated there, and this change is enforcing that
separation in a second place rather than amending it.

`evals/board.json` gains no field, and **this spec commit stales nothing**: it
writes one new feature file whose rules are `@planned` and claimed by nobody, and
this file. `verify.py` is green on it.

**The implementing change is expensive, and the number is the point.**
`measurement_inputs` hashes the body of every skill a case holds, so moving
`setup` and `doctor` stales every case that holds either — eleven rows, all of
them measured:

| Case | Skill | Runs | Δ | Last cost |
|---|---|---|---|---|
| `09-setup-confirms-before-writing` | setup | 1 | +0.00 | $0.99 |
| `11-neg-setup-adjacent-request` | setup | 1 | +0.00 | $0.30 |
| `12-setup-drives-the-sitting` | setup | 1 | +0.14 | $0.82 |
| `16-setup-with-no-app-code` | setup | 1 | +0.00 | $0.63 |
| `17-wiring-nobody-watched-run` | setup | 1 | −0.50 | $1.65 |
| `23-what-a-change-here-must-show` | setup | 1 | −0.50 | $2.44 |
| `24-a-ledger-nobody-read-back` | doctor | 1 | +0.00 | $0.93 |
| `25-neg-a-red-job-is-not-an-audit` | doctor | 1 | +0.00 | $0.18 |
| `26-two-seconds-before-the-push` | setup | 3 | +0.22 | $7.27 |
| `27-a-red-nobody-here-can-clear` | setup | 1 | +0.75 | $2.19 |
| `28-a-hook-is-not-a-row` | doctor | 3 | +0.83 | $3.45 |

**$20.85 at what those runs cost last time, and that understates it**: nine of
the eleven were measured at `runs: 1`, below the floor of 3, so they carry the
board's *fewer runs than the floor* warning already. Re-measuring them properly
costs more than re-measuring them as they stand.

Two new cases are owed on top, one per rule, at roughly $1.80 each. And
`30-a-threshold-nobody-chose` holds `setup` and has never been measured at all.

**None of that is this session's to spend.** The implementing commit and its pull
request finish with a gap where the numbers go: `verify.py` exits **2**, the red
that means nothing is broken and a run is owed. Which of the eleven are worth
re-measuring, and at what `runs`, is a decision for whoever is paying — and
"re-measure the two doctor cases and leave the nine setup rows stale" is a
legitimate answer that the board will keep reporting until it is taken.

## Risks

- **The bindings row becomes a row somebody typed.** The failure this method
  keeps finding: a line asserting something nobody checked. It is why the row is
  offered by `doctor` as it will read, rather than asserted, and why nothing here
  claims a repository *does* produce sketches — only that it records owing them.
- **Eleven stale rows is a lot of red to carry.** A board that stays stale stops
  being read, and this change puts more on it in one commit than any before it.
  The mitigation is that the split is stated: the two `doctor` rows are the ones
  this change is actually about, and the nine `setup` rows are collateral from a
  paragraph added beside an existing one.
- **`setup` sittings get longer.** They are already the longest thing this plugin
  runs, and every row added is paid in every future sitting. This is one row in a
  section that already exists, written next to the row it is most confused with —
  which is the cheapest place it could go and still not free.
- **The exemption gets copied anyway.** A repository with no app has one honest
  standing exemption already; adding a second thing that looks exempt and is not
  invites the agent to write *not applicable* on both. The example about a
  repository with nothing on a screen exists for exactly this and is the one most
  worth a hostile case.
- **`context-budget` is untouched** — no description moves, body text only.
- **`always-green` and `never-implements` are untouched.** A row in a bindings
  file gates nothing and builds nothing.

## Acceptance checks

1. Run `doctor` in `toil-tracker`, whose bindings are stamped 0.25.0. The report
   names the missing sketch row, says what closes it, and shows the row as it
   will read.
2. `grep -c sketch specs/setup/README.md` there afterwards — non-zero, where it
   is 0 today.
3. Run `doctor` in a repository that has the row already. It is not reported
   again, and the picture row is not conflated with it.
4. Run `setup` in a repository with no screen at all. The bindings record the
   picture's standing exemption **and** that the sketch is still owed.
5. Read that repository's `CLAUDE.md` after `setup` audits it. Step 4 says what
   the person holds.
6. Run `refine-spec` there on a change with a real before and after. It reads the
   row in its required reading before it starts.
7. `python3 .github/scripts/verify.py` — green on this spec commit; exit 2 on the
   implementing commit until the rows in *Data* are re-measured, which is the
   maintainer's spend to approve.

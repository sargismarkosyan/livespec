# Spec 0021: asked, not assumed

- **Status:** proposed
- **Issue:** [#56](https://github.com/sargismarkosyan/livespec/issues/56)

## Who this is for

[`agent-accelerated-owner`](../personas/agent-accelerated-owner.md) — Ren, some
time after a sitting rather than during one. The persona file already lists this
miss, in the form it had last time: *"a claim written into a bindings file that
nobody had ever run."* [`0015`](0015-the-sitting-uses-the-pipeline.md) answered
that one by making the sitting land its own work and mark what it could not
watch. This is the same miss one turn on, and the turn is the interesting part —
the claim that went wrong here was not *unwatched*. It was **answerable at the
time, by one command, and inferred from a file in the tree instead.**

The persona is also why the failure is expensive rather than annoying: this is
somebody who *"read[s] the spec layer and not the documentation"* and comes back
days later to *"act on it without checking it first."* A bindings file is the one
part of that layer describing things which are not in the repository at all —
branch protection, a required check, a credential — so it is the one part where
reading cannot catch a lie.

It sits in [`adopt-the-process`](../workflows/adopt-the-process.feature), whose
*Where it breaks* list already names *"bindings asserting a behaviour nobody has
run."* **The honest version:** a re-audit run months later is past that
workflow's *Ends when*, and it is not one of the
[three attempts not yet interviewed](../workflows/README.md#three-more-attempts-not-written-yet)
either — it is a fourth, and this spec does not cut it. The feature is tagged
with the only live workflow, the way
[`0016`](0016-captured-or-built.md) and [`0020`](0020-enough-to-say-yes.md) were,
and gains a second tag when that attempt is interviewed.

The always-promise most at risk is **`context-budget`**, and it is at risk
because of what this change is rather than in spite of it — see *Risks*.

## The job behind the request

**To not have to work out, months later, whether anybody ever checked.**

The bindings hold two kinds of sentence that look identical on the page: one
somebody verified, and one somebody wrote down because it seemed to follow. A
year on there is no way to tell them apart, and the only person who could have
is the one who wrote it. What is wanted is not a longer bindings file — it is
for the difference to survive in writing.

## Why now

Three things went wrong in one sitting on an occupied repository, and each one
took a separate prompt from the human to find:

**The branch protection row was written from the CI config.** It named a required
check. The platform hosting that repository had merge-on-green switched off at
the project level, so nothing blocked a merge on a failing gate — and the tree
could not have said so, because the setting is not in the tree.
[`repository.md`](../../method/repository.md#branches-and-pull-requests) already
says this table *"is the only record of a setting somebody could quietly
change"* — and then never says to go and read the setting before recording it.
The same sitting asserted that no token existed for posting the report; it
existed, inherited from a parent group.

**The coverage gate covered one language of two**, and the row said *automated*.
Not wrong about what was wired; wrong about what that reaches.

**And the third one is structural, which is why it survived.** The rule-bound
measure — the second coverage pass that
[`testing.md`](../../method/testing.md#measure-the-rule-bound-tests-on-their-own-and-never-gate-it)
says to build and never gate — was written into the bindings as *not built yet*
and left there. It could not have become a row: the ledger in
[`gates.md`](../../method/gates.md#what-is-wired-and-what-is-not) is *"one row
per gate named on this page, and nothing in it that is not one"*, and a measure
that must never gate is not one. The pull-request report is excluded for exactly
the same reason — this repository's own bindings say so in as many words. **So
the two pieces of wiring the method insists must never fail a build are the two
it has no way to track**, and both went unfinished in the same sitting they were
named in.

The ledger's four states say what state a gate is in. None of them says how
anybody knows.

## The end value

Ren types one thing in a repository they set up months ago and gets back: what
the bindings claim, which of those claims were read from the thing that owns the
answer, and what is still open. Without holding `gates.md` in one hand and the
bindings in the other.

**How we would know it worked:** a claim in a bindings file that was never
checked stops being indistinguishable from one that was — and a gap that is named
gets closed or written off within two changes instead of surviving as a sentence
nobody re-reads.

## What changes

An eighth skill, two method edits, and the wiring that follows from having an
eighth skill. **One `description` moves — a new one.** That is the expensive part
and *Risks* prices it.

1. **`skills/doctor/SKILL.md` — the eighth skill.** Runnable at any time and
   independent of the interviews: it reads
   [`gates.md`](../../method/gates.md)'s checklist and this repository's ledger
   and bindings, checks each claim against whatever owns the answer, and prints
   the open items. What it audits is the list the issue asked for — traceability
   in both directions, the shape of the coverage gate, the rule-bound measure,
   the report, and branch protection **as the platform reports it** rather than
   as the bindings describe it.

   **It changes the record and never the wiring.** A row that overstates gets
   corrected, a gap gets a row; wiring what is missing is
   [`setup`](../../skills/setup/SKILL.md), which already offers exactly that.
   That line is what stops the eighth skill becoming a second copy of the fifth.

   It does not restate the checklist in its own body. It reads `gates.md`, which
   is the payload every consuming repository already has, and a second copy of
   that list in a skill body is the drift this plugin exists to stop.

2. **[`gates.md`](../../method/gates.md) — the ledger section gains three
   things.** A row about something that does not live in the repository names how
   it was read back, and the command that reads it again — a row inferred from
   the tree is not evidence about a setting the tree does not hold. A row says
   what it leaves uncovered, so a gate wired over part of a repository is not
   recorded as covering it. And a **second, short table** for wiring that must
   never gate — the report and the rule-bound measure — with the same four states
   and the same two-change clock. The gate table keeps its *nothing in it that is
   not a gate* line; the second table is what that line was displacing.

3. **[`repository.md`](../../method/repository.md#branches-and-pull-requests)**
   gains one sentence where it already explains why the protection table is
   written down: it is read back from whatever enforces it, and what CI config
   says about a check is not that. Portable — the command is a binding.

4. **[`setup`](../../skills/setup/SKILL.md) picks both up**, briefly. Section 5's
   ledger paragraph gets the read-back requirement and the never-gates table;
   section 8 names `doctor` as what re-runs this later, in place of the
   re-derivation it currently implies.

5. **Seven skills becomes eight** in `README.md` and
   [`method/README.md`](../../method/README.md) — both gated by `checks.py` — and
   in [`CLAUDE.md`](../../CLAUDE.md), [`spec.md`](../spec.md),
   `CONTRIBUTING.md` and [`README.md`](../README.md). **Not** in
   [`changes/`](.), which is history, and **not** at
   [setup/README.md](../setup/README.md)'s two mentions, which record what one
   session was observed to load and would become false if edited.

6. **This repository's own bindings gain the never-gates table**, because this
   repository is its own consumer: the report reads *automated*, the rule-bound
   measure reads *not applicable* — there is no coverage here at all — and the
   paragraph explaining why the report has no row is replaced by the row.

7. **Two eval cases**, written in the implementing change. One holds the three
   rules and the skill, reusing
   [`17-wiring-nobody-watched-run`](../../evals/17-wiring-nobody-watched-run/scaffold.sh)'s
   fixture — a repository at the end of a sitting with an over-claiming ledger —
   against a prompt that asks for the wiring to be checked rather than for the
   sitting to be finished. One is **should-not-fire**, which is what this
   repository charges for a new `description`: *"why did my build go red"* is not
   this skill, and neither is a request that belongs to `setup`.

**Rules added or changed** — the `@rule:` ids in `specs/features/`:

| Rule id | Feature file | New or changed |
|---|---|---|
| `a-claim-outside-the-tree-is-read-back` | `features/wiring/ledger-claims.feature` | new |
| `a-row-says-what-it-leaves-uncovered` | `features/wiring/ledger-claims.feature` | new |
| `a-gap-is-a-row-not-a-sentence` | `features/wiring/ledger-claims.feature` | new |

All three are `@planned`, and the file — a new area, `wiring/`, for what the
record of the gates is allowed to say — is committed with this spec.

**The journey moves in the implementing change.**
[`trusting-the-spec-again`](../journeys/trusting-the-spec-again.md)'s first
opportunity currently reads *"Nothing says whether the install took... What still
arrives a change later is whether it goes on holding."* That last clause is what
this narrows, and the row is amended to say **narrowed, not closed** — nothing
here reaches a repository whose owner never runs it.

## What we are not doing

- **Wiring anything from `doctor`.** It reports and it corrects the record.
  A skill that both audits the gates and builds them has no way to be wrong out
  loud, and `setup` already owns the building.
- **A fifth ledger state.** *automated*, *not applicable*, *deferred* and
  *unobserved* say what state a gate is in; **how it was established** is a
  second axis, not a fifth value — a branch protection row can be read back from
  the platform *and* have blocked nothing yet. It goes in the row's third column,
  which is where [this repository's own bindings](../setup/README.md#branch-protection-and-the-one-credential-that-bypasses-it)
  already put it.
- **A gate over the ledger.** It is typed on purpose, and `gates.md` already says
  why: a record of what is *not* automated cannot be generated by the automation
  that does not exist.
- **Extending [`17-wiring-nobody-watched-run`](../../evals/17-wiring-nobody-watched-run/prompt.md)
  itself.** Its fixture is reused; its prompt is not. That prompt asks for a
  sitting to be finished, which fires `setup` — bolting `doctor`'s rules onto it
  would grade one skill's rules against another skill's transcript, and stale a
  $4.14 measurement to do it.
- **Naming a platform anywhere in `method/`.** This was found on a self-hosted
  GitLab; `gh`, `glab` and everything they print are bindings, and a method that
  learns one host's vocabulary has stopped being portable.
- **Re-cutting the workflows** to hold a re-audit attempt. It is real and it is
  uninterviewed, and a workflow cut from a guess has to be cut twice.

## Data

No change to what a version leaves behind
([spec.md](../spec.md#what-a-version-leaves-behind)) — the deliverable is still
the pull request description, and this change moves Gherkin, so that description
owes the block.

The ledger in every consuming repository gains a second table. Existing ledgers
stay readable and stay correct: the new table absent means *not reconciled since
this landed*, which is what the ledger's version stamp is already for, and
`doctor` offers it rather than requiring it.

## Risks

**`context-budget` is the promise this change spends, and it is the one I argued
against spending.** The always-on cost today is 3778 characters of 5000, across
seven skills; a `doctor` description in this repository's house style is 450–550,
leaving roughly 700 of headroom for everything after this. The recommendation
made when this was specced was to harden the ledger and `setup` and add no skill,
on the grounds that `setup` section 5 already diffs an existing ledger and that
the two defects were *unreadable from the tree* and *unrepresentable in the
ledger* rather than *unrepeatable*. **That recommendation was heard and
overruled, deliberately, in favour of something a person can type.** Both method
edits above land either way, so what the eighth skill buys is the re-run being a
command rather than a re-invocation of `setup` — and what it costs is a line in
every session of every user forever. The should-not-fire case is the instrument
that says whether the description stayed inside its lane; a `doctor` that starts
answering *"my pipeline is red"* is the failure to watch for, and it is watched
in `evals/` rather than in a hunch.

**Two skills describing one checklist is the second risk.** `doctor` reading
`gates.md` rather than restating it is the whole mitigation, and it is worth
saying that this is exactly the trap `gates.md` warns about for reports: *"a
second copy of the gate's logic waiting to drift out of sync."*

**`gates-are-proven` is what the first rule is really defending.** A gate the
platform does not enforce was never proven to fire *there*, whatever the fault
injection showed locally — and that gap is invisible from inside the repository,
which is the only reason it needs a rule at all.

**The measurement cost is real and it is the maintainer's.** The implementing
change stales nothing already on the board, and adds two entries: roughly $4 for
the case holding the rules at `runs: 3`, and well under $1 for the should-not-fire
case. Neither runs in CI, neither runs unasked.

## Acceptance checks

1. In a repository set up months ago, run the skill and read what comes back:
   the open items are concrete, and every claim about a setting outside the tree
   says whether it was read or not read.
2. Point it at a repository whose CI config names a required check the platform
   does not enforce. It reports the row as false, and names what it read.
3. Point it at a repository whose bindings say the rule-bound measure is *not
   built yet* in prose. It comes back as a row with a change number on it.
4. Ask it to fix what it found. It declines, and hands the wiring to `setup`.
5. Ask `doctor`'s neighbours: *"the build went red, what happened"*. It does not
   fire.

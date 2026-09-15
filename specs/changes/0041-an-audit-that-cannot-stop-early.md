# Spec 0041: an audit that cannot stop early

- **Status:** proposed
- **Issue:** [#97](https://github.com/sargismarkosyan/livespec/issues/97)
- **Depends on:** [`0038`](0038-the-other-side-of-the-difference.md), which
  gave the audit a range to read; [`0039`](0039-the-world-a-test-runs-in.md),
  which gave it the boundaries table; [`0040`](0040-the-last-line-is-the-command.md),
  which gave it a last line. All three added checks to a list that has never
  existed as a list.
- **Written as one spec, at the maintainer's instruction, and shipped as three
  pull requests** — *the shape*, *the tool*, *the refusal* — each a version that
  merges on its own. The method prefers one change per spec; the maintainer
  asked for the whole of it in one place so the parts could be judged together,
  and the order below is the order they land.

## Who this is for

[`agent-accelerated-owner`](../personas/agent-accelerated-owner.md), in
[`adopt-the-process`](../workflows/adopt-the-process.feature), at the step
after the sitting — the re-reading of a ledger that was typed once and trusted
since. The workflow names the failure in its own words: *"Bindings asserting a
behaviour nobody has run."* This is the second half of that sentence: an audit
asserting it checked something nobody can show it checked.

Three persona lines decide the shape:

- **"A claim written into a bindings file that nobody had ever run"** is one of
  the four misses that made this persona. An audit is the thing that was
  supposed to catch it, and an audit that skips checks at random is the same
  miss one level up.
- **"They read what a gate prints."** Not the transcript, not the skill body.
  So the thing that says *every check was made* has to be something a gate
  prints — an exit code and a record — not a paragraph.
- **"Fix the pipeline error, not bypass."** A tool that refuses a thin audit is
  a pipeline error to fix, and this persona fixes those. A skill that merely
  asks the model to be thorough is not a thing anybody can fix.

**This does not lengthen adoption.** The sitting gains one column in three
tables it already writes. The audit runs after adoption, on a repository that
already has the process, and what it gains is a script that runs first.

Five always-promises are touched, and each is named where it bites:
`gates-are-proven` (every check the tool answers gets a fault),
`ids-are-permanent` (the id table), `always-green` (the tool never enters a
user's build), `never-implements` (the tool writes record and nothing else),
`context-budget` (no description moves).

## The job behind the request

The literal ask, verbatim from the maintainer, 2026-09-15:

> livespeck doctor is none deterministic, there is no check list over all items
> that he needs to take care of which are a lot because of that we ended up
> having sloppy implementation whihc harms the system. This must be more brutal
> and more determininstic

The job: **to trust that an audit of a repository's wiring was complete — every
check made, every skip named — without reading the transcript and without
re-deriving the list to see what was left out.**

The trigger: wiring that turned out sloppy after an audit had passed over it,
found later by its effects rather than by the audit.

What they do today instead: re-run the audit and hope a different subset
lands; re-derive the list by hand from four method pages; or distrust the
result and re-read the ledger themselves — which is the work the audit exists
to do.

**The proposed solution was the right shape and the first design was not.**
The first design put ids on the gates, an output contract in the skill body,
and an eval with a judge — prose asking prose to be careful, scored afterwards
for money. Nothing in it could *refuse* a thin run. What serves the job is a
loop nothing can skip, and the maintainer's own counter-proposal — one narrow
session per check — had that loop. The design here keeps the loop and gives
the iterations a script can answer to a script, because a script's answer is
the same every time and can be made to fail on purpose in CI for nothing.

## Why now

Because the symptom has already been measured, once, and it said so.
[`24-a-ledger-nobody-read-back`](../../evals/24-a-ledger-nobody-read-back/prompt.md)
— the only case that plants more than one defect in a ledger — sits on the
board at **with 0.33, without 0.33, Δ 0.00**: three planted defects, one found,
and the skill adds nothing over a bare session. That entry is dated 2026-08-26
and has been stale since. Six of the nine cases that hold `doctor` have never
been measured at all.

And because the list does not exist. [`doctor`](../../skills/doctor/SKILL.md)
refuses to hold it — *"the checklist is that page, not this one"* — and points
at [`gates.md`](../../method/gates.md), whose closest sentence, *"one row per
gate named on this page, and nothing in it that is not one,"* names no gates.
[`setup`](../../skills/setup/SKILL.md) derives the row set from the same
sentence. Two derivations, never compared, and nothing that could compare
them. Counted by hand for [#97](https://github.com/sargismarkosyan/livespec/issues/97),
the audit is thirty-nine checks, several of them per row, and every one is
performed or skipped at the model's discretion with no way to tell which
afterwards.

## The end value

An audit either accounts for every one of the thirty-nine or does not end.
Twenty-five of them are answered by code, identically on every run, and that
code is broken on purpose in CI to prove it fires. The fourteen that need a
mind arrive with their question and the command that answers it, and cannot be
left blank. Ren reads a record with thirty-nine lines and an exit code, not a
paragraph about thoroughness.

**How we would know it worked:**

1. A record with thirty-eight lines cannot exit 0 — an injected fault, run on
   every `verify.py`, for nothing.
2. A scaffold with a fault planted in every section of the ledger scores full
   coverage in the with-arm on a grader that runs the tool, not a judge.
3. Case `24`'s three graders pass with the skill loaded, which they do not
   today.

## What changes

Three parts. Each is a pull request, a version, and a `minor` label.

### Part 1 — the shape

1. **[`templates/bindings.md`](../../templates/) — the whole skeleton.** Every
   section a bindings file has: the key table the skills read (with one new
   row, *Audit record*), the stamp line verbatim, the three ledger tables with
   an id as their first column, the workarounds table, and the prose headings
   with placeholders. `setup` copies and fills it the way it does a persona or
   a workflow; the parser reads its headers and the stamp line and nothing
   else.
2. **[`gates.md`](../../method/gates.md) gains the id table** — the seventeen
   gates a ledger carries, the two pieces of wiring that never gate, and the
   thirty-nine checks an audit makes, each with a kind, the version it arrived
   in, a severity, and the labels older ledgers used for it (Appendix A and B
   below, proposed for review because ids are permanent). Its line *"nothing
   in it that is not one"* becomes *"…and a row for anything else carries the
   `local:` prefix."*
3. **`setup` writes the bindings from the template.** Section 5's prose about
   what to write shrinks to *copy it and fill it*. Every ledger row carries the
   id of the gate it is a row for. Installing over an existing ledger matches
   rows by their labels and writes the ids in; the sitting reshapes the tables.
4. **`checks.py` holds every `since` and `retired` in the table to a real
   entry in `CHANGELOG.md`.** Read through `releaselib.py`, the reader the
   release already uses; broken by a fault in `inject.py`.
5. **This repository's own ledger is migrated.** Ids on the seventeen rows;
   `local:` on the four that `gates.md` never named; four rows added for gates
   the ledger is missing — `planned-unclaimed`, `boundary-fake-suite`,
   `boundary-recorded-age`, `boundaries-table` — in whatever honest state they
   are in. The stamp does not move: the record moved, the wiring did not.
6. **Vocabulary** — *check*, *audit record*, *decided* — in
   [`spec.md`](../spec.md), and the substitution's one exception in
   [`README.md`](../README.md). Both in this spec's commit.

### Part 2 — the tool

7. **[`tools/doctor.py`](../../tools/)** — standard library, read-only,
   shipped like `clip.py`, located from its own file rather than an
   environment variable. Reads the bindings, the previous audit record, the
   spec tree's listing, `specs/changes/` for the latest change number, and
   the plugin's own files. Answers the twenty-five mechanical checks; writes
   the fourteen judgment lines as `unanswered` with the id, the question and
   the command the bindings name; prints the record; exits 0. Exits 3 with
   one line and the sitting's command where there are no bindings. Recognises
   the pre-template ledger header, matches rows by alias, and reports
   `ledger-shape` as open. `--reshape` prints the ledger in template shape,
   rows verbatim, for the sitting to apply. **It runs exactly two commands of
   its own** — `git diff --name-only` and `git rev-parse` — **and never a
   string it read from a file.**
8. **[`inject.py`](../../.github/scripts/inject.py)'s fixture becomes the
   template filled green**, and its table gains one fault per mechanical
   check, plus the planted-command fault, the unparseable-ledger fault, and
   the fault for a check no fault flips. `gates-are-proven` now covers the
   tool.
9. **`checks.py` holds the id table and the tool's registry equal** on every
   column — the move it already makes for the fault record. The tool never
   parses `gates.md` at runtime; the equality is the guard.
10. **The first tests in this repository.** `tests/` at the root, standard
    library `unittest`, each test naming its rule through `tests/rulelib.py`'s
    `rule()` — the method's own ordinary shape, which this repository exempted
    itself from only because it had no code. `trace.py` reads a second kind of
    claim; `verify.py` runs the tests as part of *repository checks*; the
    bindings' *What proves a rule* row gains its second answer.
11. **`doctor`'s body is rewritten around the tool.** The first instruction is
    the command. The reasoning in §1–§3 stays, as the index each judgment line
    points into, not as a list to work through. Every refusal stands.
12. **`setup` on a repository with a ledger runs `--reshape`** and applies it
    in the sitting, with the person present.

### Part 3 — the refusal

13. **`doctor.py --validate`** reads the record the model finished and refuses
    it — exit 1, naming the line — if any id is missing, any line still reads
    `unanswered`, any state is outside `clear · open · not-read · n/a`, an
    `open` line names nothing that closes it, a `not-read` line gives no
    reason, a judgment line reads `clear` with no command beside it, or the
    diff touched anything but the bindings, `CLAUDE.md` and the record.
14. **The record is committed** at the path the bindings name — the template's
    default is `specs/setup/audit.md` — replaced on every run, one line per id
    with the date it last changed state, carried forward from the previous
    record where the state is unchanged.
15. **The reply is generated from the record**: open lines in the order
    *platform › boundary › wiring › record*, then not-read lines in the same
    order, then the decided rows as a register, then the diff against the
    previous record, then — only if an open line names wiring — the line
    [`0040`](0040-the-last-line-is-the-command.md) specified.
16. **The runner gains a `command` grader** in `asserts.py` — runs a command
    against the session's workspace and passes on exit 0 — and
    `evalsuite.py` counts it as an outcome grader.
17. **One new case, `40-every-line-or-nothing`**: a ledger with a fault
    planted in every section, graded by `--validate` for coverage and by a
    grep per planted fault for detection. LLM graders only for the fourteen.

**Rules added or changed** — the `@rule:` ids in `specs/features/`, all new
and all `@planned`. *Proved by* says which kind of proof drops the tag: a
test under `tests/`, or a graded case.

| Rule id | Feature file | Proved by |
|---|---|---|
| `every-check-has-a-permanent-id` | `features/audit/the-list.feature` | test |
| `the-table-and-the-tool-agree` | `features/audit/the-list.feature` | test |
| `a-repository-may-add-rows-of-its-own` | `features/audit/the-list.feature` | test |
| `the-bindings-are-written-from-one-template` | `features/audit/the-shape.feature` | case `12`, one grader; the fixture half by `inject.py` |
| `a-ledger-not-in-shape-is-a-finding-not-a-crash` | `features/audit/the-shape.feature` | test |
| `old-rows-are-matched-by-alias` | `features/audit/the-shape.feature` | test for the match; case `40` for the write |
| `a-check-a-script-can-answer-is-answered-by-a-script` | `features/audit/the-tool.feature` | test |
| `the-tool-runs-nothing-it-read` | `features/audit/the-tool.feature` | test — `@refusal` |
| `a-judgment-line-arrives-with-its-command` | `features/audit/the-tool.feature` | test |
| `the-outcome-is-readable-from-the-exit-alone` | `features/audit/the-tool.feature` | test |
| `every-mechanical-check-is-proven-to-fire` | `features/audit/the-tool.feature` | test over `inject.py`'s table |
| `one-line-per-check-or-it-does-not-end` | `features/audit/the-record.feature` | test for the refusal; case `40` for the hand-back |
| `a-finding-carries-what-closes-it-and-a-skip-carries-why` | `features/audit/the-record.feature` | test |
| `the-record-is-kept-where-the-bindings-say` | `features/audit/the-record.feature` | test |
| `corrections-touch-only-the-record` | `features/audit/the-record.feature` | test — `@refusal`; case `39` already greps for it |
| `the-reply-is-generated-from-the-record` | `features/audit/the-reply.feature` | test |
| `a-decided-exception-is-reported-once-and-never-relitigated` | `features/audit/the-reply.feature` | test; case `40` plants one |
| `a-check-newer-than-the-stamp-is-reported-until-the-wiring-catches-up` | `features/audit/the-reply.feature` | test; case `36`'s fixture already has the range |
| `the-tree-is-inventoried-and-the-rows-are-held-to-it` | `features/audit/the-reply.feature` | test |

**No existing rule changes id or wording.** The nine rules under
`features/wiring/` say what a single finding must say; these say that every
finding is made. [`0040`](0040-the-last-line-is-the-command.md)'s
`the-last-line-is-the-command-to-run` remains the last line's rule; part 3
generates that line from the record rather than restating the promise.

**No description changes, so no should-not-fire case is owed.** `doctor`'s
description already says *check every claim its bindings make*; what moves is
who checks them. `context-budget` stays at 4321 of 5000.

### The decisions, and who made them

- **The record is committed, as markdown, at a path the bindings name** —
  maintainer, 2026-09-15. Transient would have left every open line without an
  age.
- **One bindings file per repository** — maintainer. A monorepo's rows name
  the packages they do not cover, and the inventory pre-fills the gap.
- **Four severities, in the order `doctor` §4 already argues** — maintainer.
- **The tool's rules are proved by tests, not cases** — maintainer. The
  substitution held while there was no code; this is code.
- **The template is the whole skeleton** — maintainer.
- **The ids** — the author, proposed in the appendices for review before they
  become permanent. This is the one decision in the spec that cannot be
  revisited after merge.
- **The `local:` prefix**, **the never-executes rule**, **the exit codes** and
  **the 25 / 14 split** — the author. The split was 26 / 13 until the
  never-executes rule was written down: the tool cannot run *their*
  traceability gate to look for doubles, so `real-not-doubled` is judgment.

## What we are not doing

- **No report in a consuming repository's CI.** The twenty-five need no model
  and could run on every pull request. They will not, here: `always-green`
  says the method is written so it never needs the plugin on a build runner,
  and a step that fetches it at a pinned version is a dependency to argue for
  on purpose, in its own spec, against that promise.
- **No per-package bindings.** One file; a row says what it does not cover.
- **No non-Gherkin writer.** The traceability gate reads whatever format the
  bindings name, because `setup` wires it in the repository's language.
  `refine-spec` writes `.feature` files. A repository that wants Markdown
  features is a separate issue.
- **Not making the fourteen mechanical.** No script can read the platform for
  the model. What is enforced is the receipt.
- **Not requiring subagents for the fourteen**, and not forbidding them. The
  record does not care who wrote the line.
- **Not parsing `gates.md` at runtime.** The tool carries its registry;
  `checks.py` holds it equal to the table. One list, two copies held equal by
  CI, is not the drift the skill body warns about — two derivations from prose
  was.
- **Not moving the stamp.** [`0038`](0038-the-other-side-of-the-difference.md)
  stands: the stamp follows the wiring.
- **Not a gate on the age of the record.** A repository that never runs the
  audit gets no audit. Slide 31 of the sketch names the CI report as the thing
  that would change that, and this spec declines it above.

## Data

**In a consuming repository:** one new committed file, the audit record, at
the path the bindings name; one new column in three tables. A ledger typed
before the template is read by alias, has its ids written in by the audit, and
is reshaped by the next sitting. Nothing already stored is lost — `--reshape`
carries every row verbatim. The evidence column of the record carries a first
line or a summary of what a command returned, never a raw credential.

**In this repository:** the ledger migrates in part 1 (above, item 5); the
bindings' *What proves a rule*, *How a test names its rule* and *Verification*
rows gain their second answers in part 2; the tag contract gains
`rule("<id>")` as a claim.

**The board.** This spec's commit stales nothing: nineteen `@planned` rules
claimed by nobody, three prose files, this file. `verify.py` exits **2** on it
for the rows already owed — *22 stale, 11 never measured* — and no other
reason.

Part 1 edits `setup`'s body, so every case holding `setup` goes stale: `09`,
`11`, `12`, `16`, `17`, `30` — all already stale or never measured. Part 2
edits `doctor`'s body: `24`, `25`, `28`, `32`, `34`, `35`, `36`, `37`, `39` —
same. Part 3 adds case `40` and a grader to `12`. The marginal bill is small
because the board is already mostly red; it is still the maintainer's to
approve, at about $1.80 a case, and no part of this runs it.

**What each pull request owes.** Part 1 moves `templates/`, `method/` and a
skill: `minor`, a `## Changelog` section, and the Gherkin block — the five
feature files land in this spec's commit, which rides in that pull request.
Parts 2 and 3 drop `@planned` tags, so each owes the Gherkin block too.

## Risks

- **An id wrong at spec time is wrong forever.** `ids-are-permanent` is the
  promise; Appendix A and B are the review. Argue with the names now.
- **The parser meets a ledger it cannot read.** That is a finding
  (`ledger-shape`), never a crash, and the rest of the audit goes on. The first
  run on an old repository says *not in shape* and matches what it can by
  alias — seventeen of seventeen, here.
- **The tool is code, and code has bugs.** Standard library, tested under
  `tests/`, and broken on purpose in CI one check at a time. As trustworthy as
  `trace.py`, and no more.
- **The tool executes something.** It must not. The rule is in the tool's
  docstring, in the skill, and in a fault that plants a command and checks
  for the mark. The commands on judgment lines are printed for the model,
  which runs them under the person's permission prompts.
- **The tool enters a user's build.** It must not, and nothing here wires it
  there. `always-green`.
- **`trace.py` reading a second kind of claim** is a change to this
  repository's traceability gate. It gets the fault every gate gets.
- **The fourteen are wrong.** Possible; they are judgment. What cannot happen
  is that they are silent — every line carries its command and its result or
  its reason.
- **The record carries something sensitive.** First line or summary, never a
  raw credential — one sentence in the tool and the skill.
- **Two specs' worth of change in one.** The three parts merge separately, in
  order, and each is green alone. Part 1 is useful with no tool: two
  derivations become one.

## Acceptance checks

There is no app; this repository's deliverable is the pull request description.

1. **Part 1.** `specs/setup/README.md`'s ledger rows carry ids; four rows are
   new and `local:` is on four. `python3 .github/scripts/verify.py` — exit 2
   for the rows already owed, nothing else red. `templates/bindings.md` exists
   and `setup` links it.
2. **Part 2.** `python3 tools/doctor.py specs/setup/README.md` prints
   thirty-nine lines, twenty-five answered, fourteen `unanswered` each with a
   command. Run it twice: identical. `verify.py` shows every new fault caught,
   including *a command planted in a bindings cell* leaving no mark.
   `python3 -m unittest discover tests` is green and every test names a rule.
3. **Part 3.** Delete one line from a finished record: `--validate` exits 1
   naming it. Run `doctor` here: `specs/setup/audit.md` is written, the reply
   opens with what opened and closed since the previous record. Run it again:
   the `since` dates are carried. Run the suite on case `40` when approved:
   the command grader passes in the with-arm.
4. **In `toil-tracker`**, the consuming repository the maintainer audits: the
   first run reports `ledger-shape` open, matches its rows by alias, and ends
   with `/livespec:setup`; after the sitting reshapes the ledger, the second
   run's record is clean of shape findings and the stamp has moved with the
   wiring.

## Appendix A — the ledger's row ids, proposed

Seventeen gates, in [`gates.md`](../../method/gates.md)'s order:

`gate:rule-to-test` · `gate:test-to-rule` · `gate:planned-unclaimed` ·
`gate:feature-to-workflow` · `gate:workflow-to-feature` ·
`gate:workflow-walked` · `gate:workflow-to-persona` ·
`gate:persona-to-workflow` · `gate:journey-to-workflow` ·
`gate:workflow-to-journey` (warns) · `gate:structure` · `gate:coverage` ·
`gate:boundary-double` · `gate:boundary-fake-suite` ·
`gate:boundary-recorded-age` · `gate:boundaries-table` ·
`gate:verified-to-fire`

Two that never gate: `wiring:pr-report` · `wiring:rule-bound-measure`.

Two prefixes a repository fills itself: `boundary:<name>` — one per thing the
app talks to, named in the sitting, never derived; `local:<name>` — a gate the
repository added that the method does not name, held to the same states,
required by nothing.

This repository's ledger, matched by alias, is short four gate rows on its
first audit — `planned-unclaimed` and the three boundary gates — and carries
four `local:` rows. Which is the point.

## Appendix B — the thirty-nine, proposed

*m* — a script answers it. *j* — a mind does, from the command the bindings
name. Severity sorts the reply. `since` is read from `CHANGELOG.md` in part 1,
from the change that introduced each check.

| # | id | kind | severity | | # | id | kind | severity |
|---|---|---|---|---|---|---|---|---|
| 1 | `check:stamp-present` | m | record | | 21 | `check:check-name` | j | platform |
| 2 | `check:stamp-range` | m | record | | 22 | `check:who-bypasses` | j | platform |
| 3 | `check:stamp-ahead` | m | record | | 23 | `check:credentials-present` | j | platform |
| 4 | `check:range-empty-said` | m | record | | 24 | `check:read-back-or-not` | m | record |
| 5 | `check:changelog-reachable` | m | record | | 25 | `check:prose-phrases` | m | record |
| 6 | `check:entry-moved-here` | j | record | | 26 | `check:second-table` | m | wiring |
| 7 | `check:row-state-legal` | m | record | | 27 | `check:pr-report-row` | m | wiring |
| 8 | `check:row-evidence` | m | record | | 28 | `check:rule-bound-row` | m | wiring |
| 9 | `check:row-uncovered` | j | wiring | | 29 | `check:sketch-row` | m | record |
| 10 | `check:number-from-config` | j | wiring | | 30 | `check:picture-row` | m | record |
| 11 | `check:demand-is-a-ratchet` | j | wiring | | 31 | `check:skill-names` | m | record |
| 12 | `check:exclusions-in-config` | j | wiring | | 32 | `check:word-not-a-skill` | j | record |
| 13 | `check:na-vs-tree` | m | record | | 33 | `check:loop-per-claude-md` | j | record |
| 14 | `check:row-per-gate` | m | wiring | | 34 | `check:deferred-clock` | m | wiring |
| 15 | `check:real-starts-here` | j | boundary | | 35 | `check:hook-no-row` | m | record |
| 16 | `check:real-not-doubled` | j | boundary | | 36 | `check:sorted-by-severity` | m | record |
| 17 | `check:fake-suite-green` | j | boundary | | 37 | `check:record-only` | m | record |
| 18 | `check:recorded-age` | m | boundary | | 38 | `check:last-line-command` | m | record |
| 19 | `check:mocked-clock` | m | boundary | | 39 | `check:no-line-when-clear` | m | record |
| 20 | `check:merge-blocked` | j | platform | | | | | |

Twenty-five *m*, fourteen *j*. Four of the *m* — 24, 36, 38, 39 — are
generated by `--validate` and the reply rather than read from a file, which is
why the tool has twenty-one functions and the record twenty-five answered
lines.

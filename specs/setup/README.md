# The bindings

Everything below is true of **this repository** and nothing else. A sentence here
that could survive being moved to another repository belongs in
[`method/`](../../method/README.md) instead, and putting it here is how two
copies of a method start disagreeing.

Every skill reads this file before it assumes a command.

## The substitution: eval cases instead of tests

This repository ships prose that a model reads. There is no application code to
assert against — the product is **judgment under pressure**, and the only way to
hold judgment is to run it against a prompt and grade what came back. So
wherever the method says *test*, this repository means **eval case**:

| The method says | Here that is |
|---|---|
| `tests/behaviour/` — a test naming the rule it exists for | an eval case tagged `rule:<id>` |
| `tests/workflows/` — one walkthrough per workflow | an eval case tagged `workflow:<id>` |
| `tests/unit/` — internals, exempt from rule references | the gate scripts, held by [`inject.py`](../../.github/scripts/inject.py) |
| the `rule()` helper | the case's `tags:` frontmatter — see below |
| coverage | **there is none.** See *What has no gate* |

## The table

| | |
|---|---|
| **Verification** | `python3 .github/scripts/verify.py` |
| **What it returns** | 0 green; **1** a gate is broken; **2** nothing is broken and a measurement run somebody pays for is owed. The split is `COSTS_MONEY` in `verify.py`, the same constant `--local` filters on, and the decision is `verdict()` — pure, so `inject.py` can break it without a fixture. A mixed failure is **1**: a defect never reports as a bill. `run.py` already exits 2 for the same sentence from the other side. **CI runs the two halves as two jobs** — `repository checks` runs `--local` and gates; `measurement board` runs the rest, fails visibly and is required by nothing. See [`0033`](../changes/0033-a-bill-nobody-approved-does-not-block.md) |
| **What it runs** | `checks.py`, `trace.py`, `tests.py`, `evalsuite.py`, `board.py`, `inject.py`, in that order |
| **Before the push** | `.githooks/pre-push` — one line, `exec verify.py --local`. **Off by default**: `git config core.hooksPath .githooks` turns it on in a clone, `git config --unset core.hooksPath` turns it off, and `git push --no-verify` walks past it. `--local` runs every gate but `board.py`, whose only cure is an eval run the maintainer pays for — see *The wiring that must never gate* below for why it has no row anywhere |
| **Language** | Python 3.12, standard library only. **No dependency may be added** — CI installs nothing to run the gates |
| **Package manager** | none |
| **Traceability gate** | `.github/scripts/trace.py [root]` |
| **Eval-suite gate** | `.github/scripts/evalsuite.py [root]` |
| **Fault injection** | `.github/scripts/inject.py` — builds a synthetic fixture and breaks every gate in it one fault at a time, then breaks the release inputs, which need no fixture. *The fault injection record* below is generated from its three lists and checked against them by `checks.py`, so it cannot fall behind. Two of the three are pure and need no fixture: the release inputs, and `verify.py`'s `verdict()`. It also holds three **controls**: that the unbroken release inputs release, that `report.py` exits zero on every degenerate input, which is what `always-green` rests on, and that a run whose only failure is the board reads as a bill rather than a defect |
| **Release-input gate** | `.github/scripts/version_gate.py [base]` — CI only, on pull requests. Fails a change to `skills/`, `method/`, `templates/`, `tools/` or `.claude-plugin/` that carries no `patch`/`minor`/`major` label, or two, or no `## Changelog` section in the body. Since [`0042`](../changes/0042-the-release-writes-the-list.md) it also fails a change on the audit surface with no `## Ids` section, one that says *unchanged* while the id table moved, a new id row with a typed version, or an id deleted rather than retired |
| **Spec-surface check** | the same gate, asked separately. Fails a change to a `.feature` under `specs/features/` or `specs/workflows/` whose body carries no ` ```gherkin ` block and no link to a `.feature` pinned at a 40-character SHA. A layer README is not a `.feature` and does not trigger it |
| **Release** | `.github/workflows/release.yml` on push to `main`, running `.github/scripts/release.py`. Bumps `version`, writes the `CHANGELOG.md` entry, stamps every `next` in `method/gates.md`'s id table with the version — the third file it owns, since [`0042`](../changes/0042-the-release-writes-the-list.md) — stamps this ledger's *Reconciled against* line with the version and the date — the fourth, since [`0044`](../changes/0044-the-release-stamps-its-own-ledger.md) — runs `verify.py --local`, commits all four, pushes, tags with `claude plugin tag --push`, opens the GitHub Release |
| **Release reader** | `.github/scripts/releaselib.py` — the one reader the gate, the release job and the changelog-shape check share, and pure, so `inject.py` can break it |
| **Repository checks** | `.github/scripts/checks.py [root]` — manifests, skill frontmatter, always-on budget, link and payload checks, the two enumerations in this file that restate what another script owns, and — since [`0038`](../changes/0038-the-other-side-of-the-difference.md) — that `CHANGELOG.md` keeps the shape an audit in a consuming repository reads by: at the plugin root, every heading `## <version> — <date>`, the manifest's `version` with an entry. It takes a root so `inject.py` can break it |
| **Pull-request report** | `.github/scripts/report.py <head.json> <base.json>`, fed by `trace.py --json` run against this tree and against a worktree of the base. Posted by `.github/workflows/checks.yml` as one comment per pull request, `--edit-last --create-if-none`. **Every report step is `continue-on-error`** — it is not a gate and may never fail the build. Since [`0025`](../changes/0025-which-red-it-is.md) each is guarded `!cancelled()` rather than left to stop with the job, so the report is built and posted **on a red build too** — the run where its *Stale* row is the thing worth reading, and the run it was previously skipped on. No coverage section: there is no coverage gate here, and *What has no gate* says why. Since [`0052`](../changes/0052-the-run-beside-the-claim.md) it also prints *The run*: the body's run block beside the last lines of the `Verify` step's own output, handed over as two files |
| **Audit record** | `specs/setup/audit.md` — written by `tools/doctor.py --validate` on every audit, one line per check with the date it last changed state, replaced each run; git history is the archive. First written by the audit that closed [`0041`](../changes/0041-an-audit-that-cannot-stop-early.md) part three |
| **Case discovery** | `evals/*/` holding `prompt.md` or `case.yaml`, plus `graders/*.md`. A `case.yaml` may name a `scaffold_script` — bash in the case directory, run by `run.py --scaffold` in the session's fresh workspace, both arms alike. Since [`0054`](../changes/0054-a-case-names-the-world-it-runs-in.md) every case declares its world — a `scaffold_script`, or `workspace: empty — <why>` in its frontmatter — and `evalsuite.py` fails one that says neither, or says empty and not why. `evals/results/` is ignored and gitignored |
| **Rule claiming** | `tags:` in the case's frontmatter. `caselib.py` is the one reader the gates and the runner use |
| **Always-on budget** | 5000 chars across model-invocable skills; currently 4321 across 8 — every skill is model-invocable, and `USER_INVOKED_ONLY` in `checks.py` is empty and checked both ways |
| **What proves a rule** | **graded cases** for the skills — the product is judgment, so behaviour is run against a prompt and scored; the full argument is *The substitution* above and [`0011`](../changes/0011-how-a-test-claims-a-rule.md), and [`testing.md`](../../method/testing.md#first-what-proves-a-rule-is-true-here) states what that proves less of. **Ordinary tests** for the one thing here that is code, `tools/doctor.py`: standard-library `unittest` under `tests/`, since [`0041`](../changes/0041-an-audit-that-cannot-stop-early.md) part two — and, since [`0048`](../changes/0048-the-file-every-session-reads-first.md), for the context-file checks in `trace.py`, held by `tests/test_context_file.py`, which runs the gate against the injector's fixture |
| **How a case names its rule** | `tags: [rule:<id>]` in the case's frontmatter, read by `caselib.py`. A test names its rule with `@rule("<id>")` from `tests/rulelib.py`, which refuses an id that does not exist or is still `@planned`; `trace.py` reads both as claims, and `.github/scripts/tests.py` refuses a test bound to no rule. Since [`0051`](../changes/0051-a-test-that-did-not-run-claims-nothing.md) a test under `unittest`'s `skip`, `skipIf`, `skipUnless` or `expectedFailure` claims nothing, and `tests.py` fails a run that reports fewer tests than the tree holds |
| **Spec-bound coverage** | **not applicable.** It is a split of a coverage run, and there is no coverage gate here to split |
| **Coverage thresholds** | none — see below |
| **Required checks** | `repository checks` and `plugin validate` — the `name:` of each job in `.github/workflows/checks.yml` |
| **Tracker** | GitHub Issues on `sargismarkosyan/livespec`, via `gh`. No `--repo` is passed: `gh` resolves it from the working directory, which is this repository. **This is the degenerate case** — the repository a session works in and the plugin's own repository are the same place here, and a skill must not read that as the normal shape |
| **Where the app runs** | nowhere. There is no app |
| **A sketch is owed** | by every change spec, before approval — there is no app here, and the sketch is drawn from the spec, never recorded; *What does not apply here* below says why the two rows are not one |
| **CLAUDE.md ceiling** | **138 lines**, read with `wc -l CLAUDE.md`; set at [`0046`](../changes/0046-a-number-and-no-file-to-copy.md) to the size the file was that day, per [`claude-md.md`](../../method/claude-md.md#length), and under the two hundred that page allows since [`0049`](../changes/0049-the-readers-own-limit.md). Raised only in the change that needs the room, with the reason written here beside the number. Read by `trace.py` since [`0048`](../changes/0048-the-file-every-session-reads-first.md): a file past it fails the build, and so does this table without the row. `check:loop-per-claude-md` still hands the prose to a mind |
| **Deliverable of a version** | the pull request description. No picture in any form — see *What does not apply* |
| **Manifest validation** | `claude plugin validate . --strict`, `./.claude-plugin/plugin.json`, `./skills` — offline, no credentials |
| **What a contributor owes a release** | one `patch`/`minor`/`major` label on the pull request, and a `## Changelog` section in its body — plus the Gherkin block when the change moves a `.feature`, and an `## Ids` section when it moves the audit surface (`skills/doctor/`, `tools/doctor.py`, `templates/bindings.md`, `method/gates.md`): *unchanged*, or the ids added and retired, held to the id table's diff. Nothing else — `version`, `CHANGELOG.md` and every `since` in `gates.md` are written by the pipeline and must not be typed in a branch; a new id row reads `next`. Since [`0042`](../changes/0042-the-release-writes-the-list.md). And since [`0052`](../changes/0052-the-run-beside-the-claim.md), **the run block** when the change touches `tests/`, `evals/` or `.github/scripts/`: a fenced block opening with `python3 .github/scripts/verify.py` — the *Verification* row above, which is where `version_gate.py` reads it — and the runner's own output beneath |

## The tag contract

A case declares what it holds in its own frontmatter. `tags` is a first-class
field of the eval format — the runner filters on it with `--tag` — so this adds
no file the tooling does not already understand.

```yaml
---
tags: [skill:refine-spec, rule:add-goes-to-top]
runs: 3
---
```

| Tag | Means | Enforced by |
|---|---|---|
| `skill:<name>` | this case holds that skill's judgment | `evalsuite.py` — a skill no case names fails the gate |
| `rule:<id>` | this case is the answer to that Gherkin rule | `trace.py`, both directions |
| `@rule("<id>")` on a test under `tests/` | this test is the answer to that rule — the same claim, for the code this repository ships | `trace.py`, both directions; `tests.py` fails a test bound to no rule |
| `rule:<id>` on a `should-not-fire` case | only legitimate where the rule is tagged `@refusal` | `trace.py` — otherwise a warning, because a case asserting nothing fires cannot verify a rule that promises a behaviour |
| `workflow:<id>` | this case walks that workflow end to end | `trace.py` — a workflow nothing walks fails |
| `should-not-fire` | this case asserts nothing fires | `evalsuite.py` — the suite must always keep at least one |
| a `command` grader | this case is scored by a script run in the session's workspace, exit 0 to pass — the deterministic grader, since [`0041`](../changes/0041-an-audit-that-cannot-stop-early.md) part three | `evalsuite.py` — counts as an outcome grader; one with no `command:` fails |

**A case is not required to claim a rule**, and the cases that predate this layer
do not — see *The spec layer starts today* in [`../README.md`](../README.md). The direction that
carries the value — `rule → case` — needed no exemption to work: it had nothing
to fail on while the layer was empty and armed itself the moment the first rules
landed in [`0008`](../changes/0008-the-gate-gets-something-to-hold.md). What is
enforced besides is that a claim *resolves*: a case naming a rule or workflow
that does not exist fails, on a should-not-fire case as much as any other.

What stops a case being filler is the eval-suite gate, not a claim: every case
carries `skill:<name>` and at least one outcome grader.

**Unverified against the native runner.** `claude plugin eval` will not start
on this account (below), so the `tags:` keys have never been round-tripped
through it — the runner that does run, `evals/runner/run.py`, reads them through
the same `caselib.py` the gates use. If the native runner ever rejects one, the
claim moves to a `case.yaml` — `caselib.py` already reads both — and only that
reader changes.

## What has no gate, and what that misses

**There is no coverage gate.** Lines, branches and functions are meaningless
against eight markdown files, and a coverage number over `.github/scripts/`
alone would measure the gate rather than the product. Rather than name a
threshold nobody measures, this repository does not have one.

What replaces it is the eval-suite gate: every skill held by at least one case,
every case scored on what came out rather than on what fired, `runs: 3` as a
floor, and at least one should-not-fire case always present. **What that misses**
is depth — it proves a skill is held, never that it is held *well*. A case
softened until it always passes still counts here, which is why
[`evals/README.md`](../../evals/README.md) puts that in writing and
`evalsuite.py` fails if the documented invocation loses `--ablation with-without`.

**And what a case runs against is a stand-in in two places** — the judge for the
reader, the scaffold's fixture for a repository — which *The boundaries* under
*Gate wiring* now says with a state and a date, rather than this paragraph
saying it once and nothing asking again.

**And it misses whatever needs a tool the runner's sessions do not have.**
Asked on **2026-09-01** — `claude -p "List the exact names of every tool
available to you, one per line, no commentary." --model haiku` — a headless
session listed 40 tools and no way to render a page among them. That is not a
grant `--allow-tools` withholds; the tool is absent from the session, so neither
arm of an ablation can reach behaviour that needs one. Two rules in
[`before-it-is-built`](../features/showing/before-it-is-built.feature) ship
`@planned` for that reason and say so in the file — the same shape as
[`the-sitting-ends-by-using-the-pipeline`](../features/setup/demonstration.feature),
which no workspace with a live remote could be built for. Both are recorded
rather than softened; see [`0029`](../changes/0029-drawn-before-it-is-built.md),
*What no case reaches*.

**The cases are not run by any gate.** They cost money per session, and CI
installs and pays for nothing. The maintainer step that runs them, since
[0012](../changes/0012-a-runner-that-runs.md):

```
python3 evals/runner/run.py --ablation with-without --judge-model sonnet --allow-tools Write Edit --scaffold
```

**It refuses unless the maintainer approves that run.** `--i-approve-the-cost`
is required and deliberately absent from every command quoted here, so copying
one refuses rather than spends; `evalsuite.py` fails the build if the refusal
is removed. Six sessions per case plus judge calls bill the maintainer's
account and draw down its session limit — three runs in one sitting exhausted
it outright on 2026-08-25. A stale board entry is a reason to stop and ask,
never a licence to run.

It compiles the case folders into a promptfoo config (pinned `promptfoo@0.122.0`,
run via `npx` — node is a maintainer-machine prerequisite, never CI's), drives
each arm through `claude -p` (`--plugin-dir` present or absent is the ablation),
and scores `llm` graders through the judge model with a `--json-schema` verdict.
The format stays native to `claude plugin eval`, which is compiled into the CLI
but gated per organisation during early access — on this account it prints
`` `plugin eval` is currently in early access `` and exits before case
discovery. Nothing local causes it; enablement arrives server-side, and if it
ever lands, both runners read the same folders.

**`--allow-tools` is an operator grant.** `Write`, `Edit`, `Bash`, `WebFetch`,
`WebSearch` and `mcp__*` are refused unless the person running the suite grants
them, whatever a case's own `allowed_tools` says — so a grader checking what the
agent created is inert without it. `evalsuite.py` fails when the invocation
documented in `evals/README.md` does not grant what the cases ask for.

The gate proves a case **exists, claims a live rule, and can fail**. It does
not prove it passes, and no output from `verify.py` should be read as saying it
does — that is what running the suite is for, and no number from a run is
trusted before the calibration pass `evals/README.md` describes.

**What survives a run is the board.** `evals/board.json`, committed, one entry
per case: the last measurement and a hash of its inputs — the case's files, the
rules it claims, the skills it holds, computed in `caselib.py` so the runner
and the gate cannot disagree. `board.py` (gate 5, in `verify.py`) **fails** a
case whose inputs changed after its measurement and **warns** on one never
measured; `run.py --changed` re-runs exactly the stale set. The score is never
gated — only its bookkeeping. The pull-request report reads the counts from
`board.py --json`, which always exits 0: in that mode it is a hand-over, not a
gate.

**The floor is `MIN_RUNS = 3` in `caselib.py`, and it binds both ends.**
`evalsuite.py` fails a case declaring fewer runs than that; `board.py` **warns**
on an entry that came back from fewer, keeps it, shows it, and leaves it out of
both the measured count and the mean. `run.py` calls `caselib.replaces()` before
every write and will not put a below-floor number into a row a measurement
holds — `evalsuite.py` fails if that call goes missing, the same way it fails if
`--i-approve-the-cost` does. Added by [`0028`](../changes/0028-below-the-floor.md)
after a `--runs 1` pilot overwrote a three-run entry, flipped its sign and
cleared the freshness gate in one write, on
[#75](https://github.com/sargismarkosyan/livespec/issues/75). On the day it
landed the board read **5 measured, 23 below the floor, mean Δ +0.44**, where it
had read *28 measured, mean Δ +0.29* the day before; no session was run, and
what moved was what the numbers were allowed to be called.

## Gate wiring

**Reconciled against livespec 1.14.0 on 2026-09-16.** One row per gate named in
[`gates.md`](../../method/gates.md#what-is-wired-and-what-is-not) — including the
ones that are not wired, which is the half a repository otherwise forgets. This
repository *is* the plugin, so the stamp above is the version in the same commit
as the method it was reconciled against; anywhere else the two move apart, and
that gap is the thing a later `setup` run offers to close.

| id | gate | state | evidence |
|---|---|---|---|
| `gate:rule-to-test` | rule → case | automated | `trace.py` — a live rule no case and no test claims fails; tests claim through `rule()` since [`0041`](../changes/0041-an-audit-that-cannot-stop-early.md) part two |
| `gate:test-to-rule` | case → rule | automated | `trace.py` — a case or a test claiming an id that does not exist fails |
| `gate:feature-to-workflow` | feature → workflow | automated | `trace.py` |
| `gate:workflow-to-feature` | workflow → feature | automated | `trace.py` |
| `gate:workflow-walked` | workflow → case (walked end to end) | automated | `trace.py` |
| `gate:workflow-to-persona` | workflow → persona | automated | `trace.py`, live personas only — a `@retired` one does not count |
| `gate:persona-to-workflow` | persona → workflow | automated | `trace.py` |
| `gate:journey-to-workflow` | journey → workflow | automated | `trace.py` |
| `gate:workflow-to-journey` | workflow → journey | automated | `trace.py`, as a **warning** — where an attempt sits in the arc is a judgment |
| `gate:structure` | structure — one feature per file, unique ids, every rule with an example, no example outside a rule | automated | `trace.py` — and the soft limits, six rules and 120 lines per file, **warn and do not fail**, broken by two faults since [`0047`](../changes/0047-a-warning-that-has-never-fired.md), each expected to warn |
| `gate:verified-to-fire` | both gates verified to fire | automated | `inject.py` — every gate broken in a fixture and the release inputs broken as pure functions, re-run by every `verify.py`. **`checks.py` is in that set only since [`0022`](../changes/0022-nobody-types-the-record.md)**, which is when it first took a root and could be pointed at a fixture at all; before that it was the one gate here never known to fire |
| `local:enumerations-read-back` | the enumerations in this file read back from what owns them | automated | `checks.py`, added by [`0022`](../changes/0022-nobody-types-the-record.md) — *The fault injection record* against `inject.py`, *What it runs* against `verify.py`. Both were typed, and both had drifted |
| `local:record-shape` | the record an audit reads by keeps its shape | automated | `checks.py`, added by [`0038`](../changes/0038-the-other-side-of-the-difference.md) — `CHANGELOG.md` at the plugin root, every heading a release and a date, the manifest's `version` with an entry. Read through `releaselib.py`, which is also what writes it, and broken by two faults in `inject.py`. Every version *reaching* an entry was already held by the release faults; this holds the shape the reading depends on |
| `gate:coverage` | coverage — lines, branches, functions | **not applicable** | there is no application code to measure; the eval-suite gate stands in its place, and *What has no gate* above says what that misses |
| `local:journey-freshness` | a journey looked at since the workflows under it moved | **not applicable** | a git question, and CI checks out one commit — it would pass forever while looking enforced |
| `local:features-piled-up` | features piled up under a workflow since its file was last edited | **not applicable** | same, and `gates.md` leaves both out for that reason |
| `gate:boundary-double` | a rule-bound test doubling a boundary declared real | **not applicable** | there are no rule-bound tests here to read — the cases are the tests, and what they run against is *The boundaries* below, added by [`0039`](../changes/0039-the-world-a-test-runs-in.md) |
| `gate:planned-unclaimed` | a `@planned` rule or workflow that is claimed | automated | `trace.py` — the tag should have come off in the change that made it true; broken by *@planned rule that has a case* |
| `gate:boundary-fake-suite` | a fake row naming no suite against the real thing | **not applicable** | there are no rule-bound tests here for the gate to read — the cases are the tests, and *The boundaries* below is what they run against |
| `gate:boundary-recorded-age` | a recorded row past its age | **not applicable** | same — and no row below reads *recorded* |
| `gate:boundaries-table` | rule-bound tests present and no boundaries table | **not applicable** | same; the table exists since [`0039`](../changes/0039-the-world-a-test-runs-in.md) and nothing here is a rule-bound test that would fail for its absence |
| `gate:crossing-names-a-boundary` | a rule tagged `@crosses:` a boundary the bindings have no row for | automated | `trace.py`, since [`0053`](../changes/0053-a-rule-names-what-it-crosses.md) — reads each `@crosses:<id>` against the `boundary:<name>` rows in *The boundaries* below, fails one naming a boundary no row declares, and warns a crossing rule with a single example. One live rule carries it: [`a-claim-outside-the-tree-is-read-back`](../features/wiring/ledger-claims.feature) crosses `boundary:platform` and shows it unreachable. Broken by *a rule crossing a boundary the bindings have no row for*; the warn by *a crossing rule with a single example* |
| `gate:context-file-ceiling` | the context file past the ceiling the bindings name, or with no ceiling row | automated | `trace.py`, since [`0048`](../changes/0048-the-file-every-session-reads-first.md) — reads *CLAUDE.md ceiling* in *The table* above, in lines, and fails a file past it or a table without the row; broken by *a context file past its ceiling* and *a context file with no ceiling row*. Since [`0049`](../changes/0049-the-readers-own-limit.md) it also fails a ceiling above the two hundred the method allows, broken by *a ceiling above the reader's limit* |
| `gate:context-file-shape` | the context file missing, or without its loop, its commands, or its pointer to the bindings | automated | `trace.py`, since [`0048`](../changes/0048-the-file-every-session-reads-first.md) — the root, the longest numbered run outside fenced blocks between one and eight, at least one fenced block, a relative link resolving to this file; broken by five faults. What it leaves unread is the prose, which `check:loop-per-claude-md` hands to a mind |
| `gate:skipped-test-claims-nothing` | a rule-bound test marked skipped or expected to fail claims no rule | automated | `trace.py`, since [`0051`](../changes/0051-a-test-that-did-not-run-claims-nothing.md) — reads the tests by their syntax and empties a claim under `unittest`'s `skip`, `skipIf`, `skipUnless` or `expectedFailure`, on the method or on its class, naming the test, the marker and the rule; broken by *a skipped rule-bound test claiming a rule* |
| `gate:fewer-ran-than-exist` | the runner reporting fewer rule-bound tests than the tree holds | automated | `tests.py`, since [`0051`](../changes/0051-a-test-that-did-not-run-claims-nothing.md) — counts the `test_*` methods under `tests/` against the *Ran N* `unittest` prints and fails on fewer with both numbers; more is inheritance and passes; broken by *the runner ran fewer rule-bound tests than the tree holds*. The cases have the same reconciliation from the board's own faults, *a case with no row in the table* and *a row for a case nobody has* |

**No row is deferred**, so nothing in this table is on the two-change clock; the
two rows in *The boundaries* below that read *mocked* from 0039 passed it at
0042 and were written off as *unreachable — decided* at the audit of
2026-09-16, so nothing is on the clock now. Every automated row
that carries no change number was wired by the `setup` run in 0.6.0 and
predates this ledger.

**The ids arrived with [`0041`](../changes/0041-an-audit-that-cannot-stop-early.md),
part one**, matched to these rows by the labels they carried. Four rows carry
`local:` because [`gates.md`](../../method/gates.md#the-ids) names no such gate
— they are this repository's own, held to the same states and required by
nothing. Four rows were added for gates this ledger had been missing —
`planned-unclaimed`, and the three boundary gates `0039` named without giving
rows — which is the first thing the id column found, and the reason it exists.
The stamp did not move: the record moved, the wiring did not.

### The wiring that must never gate

The second table [`gates.md`](../../method/gates.md#the-wiring-that-must-never-gate)
asks for, added by [`0021`](../changes/0021-asked-not-assumed.md). Neither line in
it is a gate — that is the point of it being a separate table, and the reason
both were previously tracked by nothing.

| id | wiring | state | evidence |
|---|---|---|---|
| `wiring:pr-report` | the pull-request report | automated | [`report.py`](../../.github/scripts/report.py), posted by [`checks.yml`](../../.github/workflows/checks.yml). **Watched arriving on [#55](https://github.com/sargismarkosyan/livespec/pull/55)**, read back with `gh pr view 55 --json comments` rather than inferred from the workflow file. It takes its counts from `board.py --json` and recomputes nothing. **Watched arriving on a *red* build on [#69](https://github.com/sargismarkosyan/livespec/pull/69)**, read back with `gh run view 33245320389 --json jobs`: `Verify` failed with exit 2 and *Build the report* and *Comment it on the pull request* both ran, where run `33140790702` had skipped both. The comment carried `Stale — inputs changed since | 0 | 7 | +7`, a row that had never once been reachable before [`0025`](../changes/0025-which-red-it-is.md) guarded the steps `!cancelled()` |
| `wiring:rule-bound-measure` | the rule-bound measure, beside the gated number | **not applicable** | there is no coverage here at all, gated or otherwise — *What has no gate* above says what stands in its place and what that misses |
| `wiring:run-beside-claim` | the run beside the claim | automated | [`report.py`](../../.github/scripts/report.py) prints the last lines of the `Verify` step's `verify.py --local` beside the run block the body carries, since [`0052`](../changes/0052-the-run-beside-the-claim.md). **Watched disagreeing on [#118](https://github.com/sargismarkosyan/livespec/pull/118)**, 2026-09-16, read back with `gh pr view 118 --json comments`: under *The run*, the body's block ended *waiting on a measurement run: measurement board* and the pipeline's tail ended *local checks green — 5 of 6 gates*, both on the page and nothing gated. They differ by that one line by design: a person runs the whole of verification, which exits 2 for the board, and the required check leaves the board to its own job |

**The pre-push hook is in neither table, and that is the decision rather than an
omission.** It runs the free four fifths of `verify.py` before a push, it is off
until somebody types the `core.hooksPath` line into their own clone, and
`--no-verify` skips it. A row claiming it — in either state, in either table —
would credit this repository with a refusal that nothing enforces, which is the
false green [`gates.md`](../../method/gates.md#and-what-is-not-wiring-at-all)
names as the worse outcome than no record at all. What it runs is in *The table*
above, where the bindings keep what is true of one machine. `doctor` reads it as
prose and does not count it as coverage.

**Nothing came out of CI for it.** `checks.yml` still runs `verify.py` whole,
board gate included, and that is still the required check.

**It has been watched, and watching it changes nothing about where it belongs.**
On 2026-08-29 a `doctor` run pushed this tree to a throwaway local bare
repository: a clean tree went through, a tree with one unclaimed live rule
appended was refused — `✘ verification failed: traceability, gate fault
injection`, and `git push` exited non-zero with the ref never created on the
remote. Then the same broken tree was pushed again with `--no-verify` and landed.
Both halves were the point of the exercise. The hook does what the row above says
it does, on the machine it was run on, and the second half is why it still gets
no row: a check that the person it constrains can decline in four extra
characters is a courtesy, and a courtesy counted as a refusal is the false green
this ledger exists to prevent. The observation belongs here, in prose, and is not
coverage.

The report's row used to be a paragraph explaining why it had none: it is
declared in `gates.md` as *not a gate*, so a row for it in the table above would
have been the first thing there that was not one. That reasoning was sound and
the conclusion was wrong — the thing it argued out of the ledger is exactly the
thing nothing else tracks. It has a table now.

**The stamp moved to 1.1.0**, because
[`0038`](../changes/0038-the-other-side-of-the-difference.md) gave `checks.py` a
check and `inject.py` two faults that prove it — a gate gained a check, which is
[`0022`](../changes/0022-nobody-types-the-record.md)'s test, and the table above
gained a row for it. The number is the one this change ships as under its
`minor` label, written before the release job writes it, the way `0025` and
`0026` did. By the reading `0038` itself introduced, nothing between 0.25.0 and
here asked wiring of this repository that it lacks — there is no coverage gate to
have ratcheted, and the sketch row was already here — and the one line of
*record* the range found behind, step 4 of this repository's own `CLAUDE.md`
naming the spec and not the sketch, is corrected in the same change.

**It had moved to 0.25.0 before that**, because
[`0026`](../changes/0026-what-else-is-wrong.md) changed when four gates run —
which is wiring by the same reading `0025` established below, and by a wider
margin: three of the four had never once executed on a failing run. Nothing was
added, removed or made to cover new ground, so no row above changes state. What
changed is that rows already reading *automated* are now reachable on the runs
where they were skipped, and a row is a claim about what this repository refuses
rather than about what it refuses on a good day.

**It had moved to 0.24.0 before that**, because [`0025`](../changes/0025-which-red-it-is.md)
rewired three things rather than describing them: `inject.py` gained a third list
of faults and a third control, `checks.py` gained the check that reads that list
back, and the report stopped being skipped on a failing build. That last one is a
change to *when* wiring runs, which is wiring — a row that only ever ran on green
was covering less than it read as covering.

**The previous stamp, and why it is the test for moving one.** It sat at
0.9.0 through the change that added the second table — that was new bookkeeping,
with no gate added, removed or rewired, and
[`setup`](../../skills/setup/SKILL.md) says to re-stamp only when the wiring
actually moved. [`0022`](../changes/0022-nobody-types-the-record.md) moved it to 0.22.0: a
gate gained a check and another gate became injectable for the first time.
[`0024`](../changes/0024-before-it-leaves-this-machine.md) then left it alone, and
was right to — a pre-push hook is not a gate and rewired nothing. A ledger
re-stamped for a change that rewired nothing has learned to lie, and one left
unstamped through a change that rewired something has learned it the other way
round.

### The boundaries

The third table [`gates.md`](../../method/gates.md#the-boundaries) asks for,
added by [`0039`](../changes/0039-the-world-a-test-runs-in.md): what world the
cases here run in. There are no rule-bound tests in this repository — the cases
are the tests, and a case runs a real model session against a stand-in for a
consuming repository, scored by a model standing in for a reader. The rows say
which of those is which, with a date, which is more than the prose above ever
did.

| id | boundary | state | since | evidence |
|---|---|---|---|---|
| `boundary:model-session` | the model session | **real** | 0012 | `claude -p` through promptfoo, started by `python3 evals/runner/run.py --ablation with-without --judge-model sonnet --allow-tools Write Edit Bash --scaffold --i-approve-the-cost` — the maintainer's to run, paid per run. Leaves uncovered: the account's session limit, which three runs in one sitting have exhausted |
| `boundary:judge` | the judge | **unreachable** — decided | 0042 | a model standing in for the human who would read what came out. It read *mocked* from 0039 and passed the two-change clock at 0042; written off at the audit of 2026-09-16 rather than left as an apology: the calibration set that would make it a *fake* — verdicts a person has scored, re-scored by the judge on a schedule, [`evals/README.md`](../../evals/README.md#calibration) — is real work nobody has scheduled, and every change touching the judge says so where the change is decided. Leaves uncovered: everything a person would have scored differently |
| `boundary:consuming-repository` | the consuming repository a case runs in | **unreachable** — decided | 0042 | a scaffold script's fixture, a stand-in for a repository somebody set up. It read *mocked* from 0039 and passed the two-change clock at 0042; written off at the audit of 2026-09-16: a case against a live remote, CI and a real tracker is a repository nobody has set aside for it, the reference repository is read by hand, and every change touching the runner says so where the change is decided. Leaves uncovered: a live remote, CI, a real tracker — which is why [`the-sitting-ends-by-using-the-pipeline`](../features/setup/demonstration.feature) stays `@planned` |
| `boundary:platform` | the platform | **real** | 0021 | `gh` against `sargismarkosyan/livespec`, read back 2026-08-29 with the commands under *Branch protection* below. Leaves uncovered: nothing named |

**The stamp stayed at 1.1.0 through 0039**, because a table was added and
nothing was rewired. **Since the audits of 2026-09-16 it follows every
release** — 1.6.0, 1.7.0, 1.7.1 — because in this repository the wiring is
the plugin's own: a release that moves the method moves the gates here in
the same merge, so the ledger is level with the plugin by construction. What
is not level is the *line*: the release commit bumps the version after the
audit, so the moment a release landed the stamp read one behind, and the next
audit moved it by hand — three times in one day, each time finding nothing
else. **Since [`0044`](../changes/0044-the-release-stamps-its-own-ledger.md)
the release writes it**, in the same commit as the version, the entry and the
id table; a fact about this repository, not about the method, because here
the wiring is the plugin's own. The record of each audit is
`specs/setup/audit.md`.

## The fault injection record

Run on **2026-08-29** by `python3 .github/scripts/inject.py`, which is part of
`verify.py` and therefore of every CI run — so this record is re-made rather than
remembered. **Every fault below produced the expected result**, and
`verify.py` prints the count on every run.

**`checks.py` reads this table back from `inject.py`.** A fault with no row, a
row naming a fault nobody injects, or an *Expected* cell that disagrees fails the
build, and the gate prints the table as it should read. Before that check existed
this record was six faults behind the injector and said so in three different
numbers, which is [`0022`](../changes/0022-nobody-types-the-record.md).

| Injected fault | Expected | Result |
|---|---|---|
| live rule with no case | fails | ✔ |
| case claims a rule that does not exist | fails | ✔ |
| @planned rule that has a case | fails | ✔ |
| feature naming no workflow | fails | ✔ |
| feature naming a workflow that does not exist | fails | ✔ |
| workflow claimed by no feature | fails | ✔ |
| workflow walked by no case | fails | ✔ |
| workflow naming a persona that does not exist | fails | ✔ |
| workflow naming no persona | fails | ✔ |
| persona named by no workflow | fails | ✔ |
| persona retired while a workflow still names them | fails | ✔ |
| workflow naming a journey that does not exist | fails | ✔ |
| duplicate rule id | fails | ✔ |
| rule with no example | fails | ✔ |
| example outside any rule | fails | ✔ |
| refusal rule losing the tag that makes its case legitimate | **warns, does not fail** | ✔ |
| workflow naming no journey | **warns, does not fail** | ✔ |
| a feature holding more rules than the soft limit | **warns, does not fail** | ✔ |
| a feature longer than the soft limit | **warns, does not fail** | ✔ |
| a context file past its ceiling | fails | ✔ |
| a context file with no ceiling row | fails | ✔ |
| a ceiling above the reader's limit | fails | ✔ |
| no context file at the root | fails | ✔ |
| a context file with no numbered list | fails | ✔ |
| a loop of nine steps | fails | ✔ |
| a context file with no fenced block | fails | ✔ |
| a context file that does not link to the bindings | fails | ✔ |
| a rule crossing a boundary the bindings have no row for | fails | ✔ |
| a crossing rule with a single example | **warns, does not fail** | ✔ |
| case graded only by what fired | fails | ✔ |
| case run fewer times than the floor | fails | ✔ |
| a case that declares no workspace | fails | ✔ |
| a case that says empty and not why | fails | ✔ |
| the last should-not-fire case removed | fails | ✔ |
| a skill held by no case | fails | ✔ |
| the documented invocation loses its baseline | fails | ✔ |
| a scaffold_script that names no file | fails | ✔ |
| a scaffolded case whose documented invocation never lays the fixture down | fails | ✔ |
| a gated tool a case asks for is never granted | fails | ✔ |
| a case with no row in the table | fails | ✔ |
| a row for a case nobody has | fails | ✔ |
| the runner losing its refusal of an unapproved run | fails | ✔ |
| the runner letting a run below the floor take a measurement's row | fails | ✔ |
| a measurement whose inputs moved on | fails | ✔ |
| a measurement whose rule was reworded | fails | ✔ |
| a case the board has never measured | **warns, does not fail** | ✔ |
| a board entry from fewer runs than the floor | **warns, does not fail** | ✔ |
| an llm grader with an empty rubric | fails | ✔ |
| every case removed | fails | ✔ |
| the fault injection record losing a row | fails | ✔ |
| the record naming a fault nobody injects | fails | ✔ |
| a recorded fault whose expected result was flipped | fails | ✔ |
| the bindings losing a gate verify.py runs | fails | ✔ |
| a changelog heading the reader cannot parse | fails | ✔ |
| a manifest version with no changelog entry | fails | ✔ |
| an id whose since names a release the changelog does not have | fails | ✔ |
| the same id twice in the id table | fails | ✔ |
| a check the tool answers that the id table does not name | fails | ✔ |
| an id in the table no function answers | fails | ✔ |
| a test claiming a rule that does not exist | fails | ✔ |
| a test outside any rule | fails | ✔ |
| a failing test | fails | ✔ |
| a test naming a rule that is still @planned | fails | ✔ |
| a skipped rule-bound test claiming a rule | fails | ✔ |
| the runner ran fewer rule-bound tests than the tree holds | fails | ✔ |
| shipping change with no release label | fails | ✔ |
| two release labels at once | fails | ✔ |
| pull request body with no changelog section | fails | ✔ |
| changelog section left empty | fails | ✔ |
| a version that already has an entry | fails | ✔ |
| a manifest with no version field | fails | ✔ |
| a version that is not major.minor.patch | fails | ✔ |
| spec-moving change whose body carries no gherkin | fails | ✔ |
| a gherkin block with nothing in it | fails | ✔ |
| a new id row with a typed version | fails | ✔ |
| the audit surface moved with no ## Ids section | fails | ✔ |
| ## Ids reading unchanged while a row was added | fails | ✔ |
| ## Ids naming an id the table does not have | fails | ✔ |
| a row still reading next after the release | fails | ✔ |
| a ledger whose stamp the release cannot find | fails | ✔ |
| a bullet list that retires what the table added | fails | ✔ |
| a change to the tests whose body carries no run block | fails | ✔ |
| a run block quoting a different command | fails | ✔ |
| a run block with no output under the command | fails | ✔ |
| a broken gate underneath a stale measurement | fails | ✔ |
| a ledger in the shape it had before ids | fails | ✔ |
| a ledger with no stamp line | fails | ✔ |
| a stamp behind the plugin installed | fails | ✔ |
| a stamp ahead of the plugin installed | fails | ✔ |
| a stamp that is not at the plugin installed | fails | ✔ |
| a changelog the tool cannot read | fails | ✔ |
| a row in a state of somebody's own | fails | ✔ |
| an automated row naming no command | fails | ✔ |
| a not-applicable reason the tree contradicts | fails | ✔ |
| a gate with no row | fails | ✔ |
| a recording past its age | fails | ✔ |
| a mocked row two changes old | fails | ✔ |
| no table for the wiring that must never gate | fails | ✔ |
| the second table losing the report's row | fails | ✔ |
| the second table losing the measure's row | fails | ✔ |
| the second table losing the run's row | fails | ✔ |
| no row saying a sketch is owed | fails | ✔ |
| the sketch row and the picture row saying one thing | fails | ✔ |
| a record instructing by a skill this plugin no longer has | fails | ✔ |
| a row deferred across two changes | fails | ✔ |
| a local hook given a row | fails | ✔ |
| a change outside the record in the working tree | fails | ✔ |
| a record one line short | fails | ✔ |
| a judgment nobody made | fails | ✔ |
| a state of somebody's own | fails | ✔ |
| an open line naming nothing that closes it | fails | ✔ |
| a not-read line with no reason | fails | ✔ |
| a judgment clear with no command beside it | fails | ✔ |
| a fix that strayed into the wiring | fails | ✔ |

**Three controls sit alongside the table and are not faults.** One checks the unbroken release inputs still release; one checks the report cannot fail a build — there is nothing to break there, because the whole promise is that nothing breaks, so what is asserted is that every degenerate input still exits zero. It was confirmed by making `report.py` able to fail and watching the control report it. The third, added by [`0025`](../changes/0025-which-red-it-is.md), asserts the two reds from the side no fault can reach: a green run says nothing, and a run whose only failure is the board exits 2, does not say *verification failed*, and names who can approve the run that clears it.

The release faults need no fixture. `releaselib.py` is pure — a label list and a pull
request body in, a decision out — which is the whole reason it is a module rather
than two copies of a regex. The gate it replaced was **not** injectable and
shipped for three versions without ever being known to fire; that was the
`gates-are-proven` debt spec
[`0003`](../changes/0003-main-releases-itself.md) inherited and paid.

The injector was itself checked by making one fault a no-op: it reported the row
as not firing and exited 1. A fault table that cannot fail is worth as little as
a gate that cannot.

## Branch protection, and the one credential that bypasses it

Migrated from classic branch protection to a **repository ruleset** on
**2026-08-25**. This is the one gate that does not live in the repository, so
this table is the only record of a setting somebody could quietly change — and
the only thing keeping it honest is somebody re-running the commands at the end
of this section. **Last read back on 2026-08-29**, with all three; every value
below matched what was already written, and nothing here is a memory of the
sitting that set it up.

**Everything below was read from GitHub rather than inferred from
[`checks.yml`](../../.github/workflows/checks.yml)**, which is what
[`repository.md`](../../method/repository.md#branches-and-pull-requests) requires
of this table and what the commands at the end of this section are for. A
workflow file naming a job says a job runs; it says nothing about whether this
repository will let a red one merge.

**Why it moved.** Classic protection with `enforce_admins` on a *personal*
repository has no bypass list at all — its push allowlist is organisation-only —
so nothing could push to `main`, the owner's own token included. That was correct
while releases were typed by hand and fatal once
[`release.yml`](../../.github/workflows/release.yml) had to write the version.
Rulesets support `bypass_actors` on personal repositories; classic protection
does not, and the two stack, so the classic rule had to go rather than be
relaxed. The ruleset was created first and the classic protection deleted second:
`main` was never unprotected.

Ruleset **21391215**, `main is production`, targeting `~DEFAULT_BRANCH`,
enforcement `active`.

| Setting | Value |
|---|---|
| Pull request required | yes |
| Required approvals | **0** — GitHub does not let anyone approve their own pull request, and there is one contributor. Zero still forces every change through a pull request and both checks |
| Required checks | `repository checks`, `plugin validate`, both matched to the GitHub Actions app (`integration_id` 15368) |
| Strict (up to date with `main`) | yes |
| Applies to admins | yes — no role, team or user is on the bypass list, and the API answers `current_user_can_bypass: never` for the owner's own token |
| Force pushes | blocked (`non_fast_forward`) |
| Deletion | blocked |
| Conversation resolution required | yes |
| Dismiss stale reviews | yes |
| **Bypass** | one entry: `actor_type: DeployKey`, `bypass_mode: always` |

**The credential.** One write-enabled deploy key, titled `livespec release`
(id 161238524, ed25519, added 2026-08-25). Its private half is the repository
secret `RELEASE_DEPLOY_KEY`, read only by the release job, which hands it to
`actions/checkout` as `ssh-key`. A deploy key is the narrowest credential that
can do this job: it reaches this repository and nothing else, it is not tied to
anybody's account, and it does not expire — so unlike a token it cannot stop the
pipeline on a date nobody wrote down.

**The caveat worth knowing before adding a second one.** `DeployKey` bypass takes
no `actor_id`: it means *any* write-enabled deploy key on this repository, not
this one. There is exactly one today. **Adding another write deploy key silently
grants it the right to push to `main`** — so a new deploy key is a decision about
branch protection, and read-only is the default to reach for.

**The built-in `GITHUB_TOKEN` cannot bypass**, even though the GitHub Actions app
is what reports the required checks. That is documented behaviour and it is why
this key exists at all; granting the workflow `contents: write` is not a
substitute.

Read it back with:

```sh
gh api repos/sargismarkosyan/livespec/rules/branches/main   # what applies
gh api repos/sargismarkosyan/livespec/rulesets/21391215     # the rules and the bypass
gh api repos/sargismarkosyan/livespec/keys                  # the deploy key
```

`gh api repos/sargismarkosyan/livespec/branches/main/protection` now returns
**404 Branch not protected**, and that is expected: it reports classic protection
only. `repos/.../branches/main` still reports `protected: true`.

## Release labels

`patch`, `minor` and `major`, created 2026-08-25. Exactly one goes on every pull
request that changes what ships; `version_gate.py` fails on none or on two, and
`release.py` reads the one that is there.

## CI

[`.github/workflows/checks.yml`](../../.github/workflows/checks.yml), two jobs,
on push to `main` and on every pull request:

- **`repository checks`** — Python 3.12, runs `verify.py --local`, then the
  release-input gate on pull requests only.
- **`plugin validate`** — Node 22, installs `@anthropic-ai/claude-code` from npm
  and runs the three offline schema validations.

**Four steps across the two jobs carry `!cancelled()` and are still gates**,
added by [`0026`](../changes/0026-what-else-is-wrong.md): the release-input gate,
and the three validations. None of them can fail because an earlier gate did —
one reads the pull request where `verify.py` reads the tree, and the three read
three different files — so a job stopping at its first failure was costing a
round trip and hiding nothing that was not already failing. **Neither the guard
nor anything else gives them `continue-on-error`**, which is the line between
these and the three reporting steps below them in the same job. The three
validations are additionally conditioned on `steps.install.outcome == 'success'`:
they do depend on the CLI being installed, and without that clause one missing
install is reported three times as three failures.

**The pull-request trigger names its types**, which a workflow rarely needs to
do: `opened, synchronize, reopened, labeled, unlabeled, edited`. The first three
are the default; the last three are there because the release-input gate reads
the label and the body out of the **event payload**, and a payload is a snapshot
of the moment the event fired. Without them, a label added at creation is not in
the snapshot the check reads, the check fails asking for a label that is visibly
on the pull request, and adding or re-adding one re-runs nothing. Re-running the
job replays the same payload and fails identically — the only route to green was
an unrelated commit. Anything a gate here reads off the pull request rather than
off the tree has to be in this list, or the gate has a failure state nothing can
clear.

[`release.yml`](../../.github/workflows/release.yml) is a **third workflow and
not a required check** — it runs after the merge, on push to `main`, and there is
nothing left to gate by then. It is serialised by a `concurrency: release` group,
because two jobs computing "the next version" from the same base is how two
versions claim the same number. Its own push lands back on `main`; it skips a
commit made under the release identity rather than using `[skip ci]`, which would
also skip `repository checks` and leave the one commit nobody reviewed as the one
commit nothing verified.

The job `name:` is what branch protection matches, not the filename and not the
command. Renaming a job silently un-requires the check.

## What does not apply here

- **[`record-clip`](../../skills/record-clip/SKILL.md)** and
  `docs/screenshots/`. There is no app to record. A version's deliverable is its
  pull request description, and the exemption in
  [`repository.md`](../../method/repository.md#every-pull-request-shows-what-it-did)
  — a change with nothing to see says so in a line — is the standing case here
  rather than the exception. The skill still ships, is still held by a case, and
  is simply never used on this repository.

  **That covers the form too, and it is worth saying once.**
  [`0020`](../changes/0020-enough-to-say-yes.md) made the picture's form follow
  what the change was — moving for a thing happening, a still where the whole
  result is a screen sitting there. Neither branch will ever be taken here: there
  is no screen, so the question never arises rather than always resolving to one
  answer. It is the first rule in the method that no version of this repository
  will exercise, and it ships on the strength of its eval cases and the pilots
  rather than on having been lived here.
**The sketch is not covered by that exemption, and does apply here.** It is
drawn *from a change spec*, at step 4, and needs no app — where `record-clip`
needs one and therefore never runs. So a change here owes one whenever its spec
argues from something the prose cannot carry at a glance:
[`0028`](../changes/0028-below-the-floor.md)'s before-and-after of the board is
the worked example, and it was already drawn in prose because the spec could not
be read without it. The two are separated in
[`spec.md`](../spec.md)'s vocabulary for exactly this reason — one word away
from being confused, and this section is where the confusion would have landed.

- **`docs/feedback/`.** Issues here are filed from reading, not from using an
  app, so there are no screenshots to attach or to `git rm` on close.

## Why one validation is not `--strict`

`CLAUDE.md` is at the repository root, where a project's CLAUDE.md belongs and
where every consuming repository will have it. This root is also a **plugin
root**, and `claude plugin validate ./.claude-plugin/plugin.json` warns about
that:

```
❯ root: CLAUDE.md at the plugin root is not loaded as project context.
```

The warning is right for a consumer — nobody installing livespec gets that file
as context — and wrong here, where it is project context for people working in
this repository. `--strict` turns warnings into errors, so that one call runs
without it. **The other two validations keep `--strict`**, and the job still
fails on any warning that is not this exact one; the workflow greps for it by
name rather than trusting that nothing else will ever warn.

Trading one narrowed flag for a conventionally placed `CLAUDE.md` is the better
side of that deal: this repository should look like the repositories it sets up.

## Running the plugin on itself

`.claude/settings.json` enables the plugin and **names no marketplace**:

```json
{ "enabledPlugins": { "livespec@livespec": true } }
```

Registering the checkout is a per-machine step, run once by hand:

```
/plugin marketplace add .
```

Until it is run, a session here has no `livespec:` skills — which is the intended
failure. The file used to carry `extraKnownMarketplaces` pointing at `"."`, and
that is what [#6](https://github.com/sargismarkosyan/livespec/issues/6) was
about: a marketplace name is machine-wide, so a committed project file naming a
directory source **repoints `livespec` for every repository on the machine of
whoever clones this one**, silently and without their asking. A project file may
enable a plugin; it should not be able to move a global name out from under the
repositories nobody in this checkout is looking at.

Pointing it at `sargismarkosyan/livespec` instead is the other wrong answer: that
loads the *published* skills while you are editing the working tree — two copies
of the method disagreeing inside the repository whose whole purpose is to stop
that.

### What loads here, and how that was established

[#6](https://github.com/sargismarkosyan/livespec/issues/6) was filed because the
paragraph that used to stand here described a behaviour **nobody had ever run**.
It has been run now — 2026-08-25, Claude Code 2.1.245 — and what it found is
below, because a binding that cannot say how it knows is the defect that issue
was about.

**The method.** Put a skill in `skills/` that exists in no published version, so
the working tree is the only copy that can produce it, and ask a session which
skills it can see:

```sh
claude -p "List the exact names of every skill available to you, one per line, no commentary." --model haiku
```

**The copy that loads in this repository is the working tree.** The session
listed every skill then shipping — seven at the time; `doctor` has since made it
eight — *and* the marker. That is the claim this section always made, and it is
now an observation. The count is of the day it was run and is not maintained
here; `ls skills/` is the answer to how many there are now.

**The declaration above is not what makes that true.** Run from a copy of this
repository at a different path — its own `.claude/settings.json`, its own
marker — the same session still returned *this* checkout's marker. Resolution
went through the machine-wide marketplace registry
(`~/.claude/plugins/known_marketplaces.json`), where `livespec` points at
`/home/sargis/Projects/livespec`, and not through the project file at all.

### The three mechanics that follow

- **A marketplace is named by its own `marketplace.json`, and the name is
  machine-wide.** `claude plugin marketplace add <dir>` registers a directory
  under the `name` its manifest declares, whatever the directory is called —
  verified with a throwaway copy whose manifest said `livespec-probe`. Claude
  Code registers one marketplace per name per user, and
  [adding a second under the same name replaces the first](https://code.claude.com/docs/en/plugin-marketplaces).
- **A project's `extraKnownMarketplaces` applies only after the folder is
  trusted**, and never in a `claude -p` session — headless runs registered
  nothing.
- **An `enabledPlugins` id whose marketplace is not registered is skipped in
  silence.** Not a warning, not an error; a `--debug` line, and no skills:

  ```
  [DEBUG] Skipping orphaned enabledPlugins entry livespec@livespec-local: marketplace not registered
  ```

### Why the rename in #6 is not the fix it looked like

That issue chose to rename the project marketplace to `livespec-local` so it
could not collide. Renaming the key in `.claude/settings.json` and enabling
`livespec@livespec-local` **loads no livespec skills at all** — the debug line
above is from exactly that configuration. The name is not the key's to choose:
it comes from `.claude-plugin/marketplace.json`, which says `livespec` because
that is what the published marketplace is called and what every consumer's
`/plugin install livespec@livespec` names. A second manifest under a local
directory cannot stand in for it either — a marketplace may not source a plugin
outside its own root, which `claude plugin validate` refuses:

```
❯ plugins[0].source: Path contains "..": ./../..
```

So the collision is not a naming mistake here. It is the product's model — one
marketplace per name per machine — meeting a repository that is both the
published marketplace and a checkout of it.

### What this costs, and the check that shows it

**Registering this checkout moves `livespec` for every repository on the
machine.** Every other project enabling `livespec@livespec` then gets the working
tree, on whatever half-finished skill edit is sitting in it — the reference
repository too, if it enables the plugin that way. Dropping
`extraKnownMarketplaces` means this repository no longer does that *to whoever
clones it*; it does not stop the person who runs `/plugin marketplace add .` here
from doing it to their own other repositories, because that is a fact about where
marketplace names live rather than something a file here can decide.

`/plugin marketplace list` says which copy is current. One line under `livespec`,
and it is one of these two:

```
  Source: Directory (/home/sargis/Projects/livespec)   the working tree
  Source: GitHub (sargismarkosyan/livespec)            the published plugin
```

`/plugin marketplace add sargismarkosyan/livespec` puts it back to the published
copy for every repository at once, and `/plugin marketplace add .` from this root
takes it again. **Neither is per-project, and the skill names cannot tell you
which one you are on** — they are `livespec:refine-spec` either way. Only the
marker method above, or that list, can.

**A session here with no `livespec:` skills means the marketplace is not
registered on this machine yet** — the ordinary state of a fresh clone, and the
one `/plugin marketplace add .` fixes. Verified on 2026-08-25 with the marker
method: with `extraKnownMarketplaces` gone and the marketplace registered, a
session still listed the skills of that day and the marker, so the enable alone
is what this file has to carry.

### What ships beside the skills, and how that was established

`doctor` reads two files from the plugin root — `CHANGELOG.md`, for what the
method changed between a consuming repository's stamp and the version installed,
and `.claude-plugin/plugin.json`, for that version — two levels up from its own
skill file. That the cache carries them is the packaging's, not this
repository's, so it cannot be gated from here; it is recorded instead. Read on
**2026-09-02**: `~/.claude/plugins/cache/livespec/livespec/0.27.0/` holds
`CHANGELOG.md`, `CLAUDE.md`, `CONTRIBUTING.md`, `LICENSE`, `README.md` and every
directory at this root — everything, which is what [CONTRIBUTING.md](../../CONTRIBUTING.md)
says and is now an observation rather than a description. A directory
marketplace is this working tree itself, so the same files are there by
construction. What *is* gated from here is the shape of the file the audit reads
by — see *Repository checks* in the table and the two faults in the record above.
A local `.claude/skills/` copy of a skill has nothing two levels up; the skill
says so once and audits the ledger without it.

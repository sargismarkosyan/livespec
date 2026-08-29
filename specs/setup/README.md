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
| **What it returns** | 0 green; **1** a gate is broken; **2** nothing is broken and a measurement run somebody pays for is owed. The split is `COSTS_MONEY` in `verify.py`, the same constant `--local` filters on, and the decision is `verdict()` — pure, so `inject.py` can break it without a fixture. A mixed failure is **1**: a defect never reports as a bill. `run.py` already exits 2 for the same sentence from the other side. **CI is red either way** — this distinguishes the red, it does not soften it |
| **What it runs** | `checks.py`, `trace.py`, `evalsuite.py`, `board.py`, `inject.py`, in that order |
| **Before the push** | `.githooks/pre-push` — one line, `exec verify.py --local`. **Off by default**: `git config core.hooksPath .githooks` turns it on in a clone, `git config --unset core.hooksPath` turns it off, and `git push --no-verify` walks past it. `--local` runs every gate but `board.py`, whose only cure is an eval run the maintainer pays for — see *The wiring that must never gate* below for why it has no row anywhere |
| **Language** | Python 3.12, standard library only. **No dependency may be added** — CI installs nothing to run the gates |
| **Package manager** | none |
| **Traceability gate** | `.github/scripts/trace.py [root]` |
| **Eval-suite gate** | `.github/scripts/evalsuite.py [root]` |
| **Fault injection** | `.github/scripts/inject.py` — builds a synthetic fixture and breaks every gate in it one fault at a time, then breaks the release inputs, which need no fixture. *The fault injection record* below is generated from its three lists and checked against them by `checks.py`, so it cannot fall behind. Two of the three are pure and need no fixture: the release inputs, and `verify.py`'s `verdict()`. It also holds three **controls**: that the unbroken release inputs release, that `report.py` exits zero on every degenerate input, which is what `always-green` rests on, and that a run whose only failure is the board reads as a bill rather than a defect |
| **Release-input gate** | `.github/scripts/version_gate.py [base]` — CI only, on pull requests. Fails a change to `skills/`, `method/`, `templates/`, `tools/` or `.claude-plugin/` that carries no `patch`/`minor`/`major` label, or two, or no `## Changelog` section in the body |
| **Spec-surface check** | the same gate, asked separately. Fails a change to a `.feature` under `specs/features/` or `specs/workflows/` whose body carries no ` ```gherkin ` block and no link to a `.feature` pinned at a 40-character SHA. A layer README is not a `.feature` and does not trigger it |
| **Release** | `.github/workflows/release.yml` on push to `main`, running `.github/scripts/release.py`. Bumps `version`, writes the `CHANGELOG.md` entry, runs `verify.py`, commits, pushes, tags with `claude plugin tag --push`, opens the GitHub Release |
| **Release reader** | `.github/scripts/releaselib.py` — the one reader the gate and the release job share, and pure, so `inject.py` can break it |
| **Repository checks** | `.github/scripts/checks.py [root]` — manifests, skill frontmatter, always-on budget, link and payload checks, and the two enumerations in this file that restate what another script owns. It takes a root so `inject.py` can break it |
| **Pull-request report** | `.github/scripts/report.py <head.json> <base.json>`, fed by `trace.py --json` run against this tree and against a worktree of the base. Posted by `.github/workflows/checks.yml` as one comment per pull request, `--edit-last --create-if-none`. **Every report step is `continue-on-error`** — it is not a gate and may never fail the build. Since [`0025`](../changes/0025-which-red-it-is.md) each is guarded `!cancelled()` rather than left to stop with the job, so the report is built and posted **on a red build too** — the run where its *Stale* row is the thing worth reading, and the run it was previously skipped on. No coverage section: there is no coverage gate here, and *What has no gate* says why |
| **Case discovery** | `evals/*/` holding `prompt.md` or `case.yaml`, plus `graders/*.md`. A `case.yaml` may name a `scaffold_script` — bash in the case directory, run by `run.py --scaffold` in the session's fresh workspace, both arms alike. `evals/results/` is ignored and gitignored |
| **Rule claiming** | `tags:` in the case's frontmatter. `caselib.py` is the one reader the gates and the runner use |
| **Always-on budget** | 5000 chars across model-invocable skills; currently 4315 across 8 — every skill is model-invocable, and `USER_INVOKED_ONLY` in `checks.py` is empty and checked both ways |
| **What proves a rule** | **graded cases.** There is no application code to call — the product is judgment, so behaviour is run against a prompt and scored. The full argument is *The substitution* above and [`0011`](../changes/0011-how-a-test-claims-a-rule.md); [`testing.md`](../../method/testing.md#first-what-proves-a-rule-is-true-here) states what that proves less of |
| **How a case names its rule** | `tags: [rule:<id>]` in the case's frontmatter, read by `caselib.py`. **Not** a `rule()` helper — there is no test runner here to wrap |
| **Spec-bound coverage** | **not applicable.** It is a split of a coverage run, and there is no coverage gate here to split |
| **Coverage thresholds** | none — see below |
| **Required checks** | `repository checks` and `plugin validate` — the `name:` of each job in `.github/workflows/checks.yml` |
| **Tracker** | GitHub Issues on `sargismarkosyan/livespec`, via `gh`. No `--repo` is passed: `gh` resolves it from the working directory, which is this repository. **This is the degenerate case** — the repository a session works in and the plugin's own repository are the same place here, and a skill must not read that as the normal shape |
| **Where the app runs** | nowhere. There is no app |
| **Deliverable of a version** | the pull request description. No picture in any form — see *What does not apply* |
| **Manifest validation** | `claude plugin validate . --strict`, `./.claude-plugin/plugin.json`, `./skills` — offline, no credentials |
| **What a contributor owes a release** | one `patch`/`minor`/`major` label on the pull request, and a `## Changelog` section in its body — plus the Gherkin block when the change moves a `.feature`. Nothing else — `version` and `CHANGELOG.md` are written by the pipeline and must not be edited in a branch |

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
| `rule:<id>` on a `should-not-fire` case | only legitimate where the rule is tagged `@refusal` | `trace.py` — otherwise a warning, because a case asserting nothing fires cannot verify a rule that promises a behaviour |
| `workflow:<id>` | this case walks that workflow end to end | `trace.py` — a workflow nothing walks fails |
| `should-not-fire` | this case asserts nothing fires | `evalsuite.py` — the suite must always keep at least one |

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

## Gate wiring

**Reconciled against livespec 0.24.0 on 2026-08-29.** One row per gate named in
[`gates.md`](../../method/gates.md#what-is-wired-and-what-is-not) — including the
ones that are not wired, which is the half a repository otherwise forgets. This
repository *is* the plugin, so the stamp above is the version in the same commit
as the method it was reconciled against; anywhere else the two move apart, and
that gap is the thing a later `setup` run offers to close.

| Gate | State | Wired by, or why not |
|---|---|---|
| rule → case | automated | `trace.py` — a live rule no case claims fails |
| case → rule | automated | `trace.py` — a case claiming an id that does not exist fails |
| feature → workflow | automated | `trace.py` |
| workflow → feature | automated | `trace.py` |
| workflow → case (walked end to end) | automated | `trace.py` |
| workflow → persona | automated | `trace.py`, live personas only — a `@retired` one does not count |
| persona → workflow | automated | `trace.py` |
| journey → workflow | automated | `trace.py` |
| workflow → journey | automated | `trace.py`, as a **warning** — where an attempt sits in the arc is a judgment |
| structure — one feature per file, unique ids, every rule with an example, no example outside a rule | automated | `trace.py` |
| both gates verified to fire | automated | `inject.py` — every gate broken in a fixture and the release inputs broken as pure functions, re-run by every `verify.py`. **`checks.py` is in that set only since [`0022`](../changes/0022-nobody-types-the-record.md)**, which is when it first took a root and could be pointed at a fixture at all; before that it was the one gate here never known to fire |
| the enumerations in this file read back from what owns them | automated | `checks.py`, added by [`0022`](../changes/0022-nobody-types-the-record.md) — *The fault injection record* against `inject.py`, *What it runs* against `verify.py`. Both were typed, and both had drifted |
| coverage — lines, branches, functions | **not applicable** | there is no application code to measure; the eval-suite gate stands in its place, and *What has no gate* above says what that misses |
| a journey looked at since the workflows under it moved | **not applicable** | a git question, and CI checks out one commit — it would pass forever while looking enforced |
| features piled up under a workflow since its file was last edited | **not applicable** | same, and `gates.md` leaves both out for that reason |

**No row is deferred**, so nothing here is on the two-change clock. Every
automated row but the last was wired by the `setup` run in 0.6.0 and predates this
ledger, which is why they carry no change number.

### The wiring that must never gate

The second table [`gates.md`](../../method/gates.md#the-wiring-that-must-never-gate)
asks for, added by [`0021`](../changes/0021-asked-not-assumed.md). Neither line in
it is a gate — that is the point of it being a separate table, and the reason
both were previously tracked by nothing.

| Wiring | State | How, or why not |
|---|---|---|
| the pull-request report | automated | [`report.py`](../../.github/scripts/report.py), posted by [`checks.yml`](../../.github/workflows/checks.yml). **Watched arriving on [#55](https://github.com/sargismarkosyan/livespec/pull/55)**, read back with `gh pr view 55 --json comments` rather than inferred from the workflow file. It takes its counts from `board.py --json` and recomputes nothing. **Arriving on a *red* build is unobserved** — [`0025`](../changes/0025-which-red-it-is.md) guarded the steps `!cancelled()` for exactly that case and the only evidence so far is the workflow file, which is the kind of evidence this table exists to refuse. Its own pull request is the first run that can settle it |
| the rule-bound measure, beside the gated number | **not applicable** | there is no coverage here at all, gated or otherwise — *What has no gate* above says what stands in its place and what that misses |

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

The report's row used to be a paragraph explaining why it had none: it is
declared in `gates.md` as *not a gate*, so a row for it in the table above would
have been the first thing there that was not one. That reasoning was sound and
the conclusion was wrong — the thing it argued out of the ledger is exactly the
thing nothing else tracks. It has a table now.

**The stamp moved to 0.24.0**, because [`0025`](../changes/0025-which-red-it-is.md)
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
| case graded only by what fired | fails | ✔ |
| case run fewer times than the floor | fails | ✔ |
| the last should-not-fire case removed | fails | ✔ |
| a skill held by no case | fails | ✔ |
| the documented invocation loses its baseline | fails | ✔ |
| a scaffold_script that names no file | fails | ✔ |
| a scaffolded case whose documented invocation never lays the fixture down | fails | ✔ |
| a gated tool a case asks for is never granted | fails | ✔ |
| a case with no row in the table | fails | ✔ |
| a row for a case nobody has | fails | ✔ |
| the runner losing its refusal of an unapproved run | fails | ✔ |
| a measurement whose inputs moved on | fails | ✔ |
| a measurement whose rule was reworded | fails | ✔ |
| a case the board has never measured | **warns, does not fail** | ✔ |
| an llm grader with an empty rubric | fails | ✔ |
| every case removed | fails | ✔ |
| the fault injection record losing a row | fails | ✔ |
| the record naming a fault nobody injects | fails | ✔ |
| a recorded fault whose expected result was flipped | fails | ✔ |
| the bindings losing a gate verify.py runs | fails | ✔ |
| shipping change with no release label | fails | ✔ |
| two release labels at once | fails | ✔ |
| pull request body with no changelog section | fails | ✔ |
| changelog section left empty | fails | ✔ |
| a version that already has an entry | fails | ✔ |
| a manifest with no version field | fails | ✔ |
| a version that is not major.minor.patch | fails | ✔ |
| spec-moving change whose body carries no gherkin | fails | ✔ |
| a gherkin block with nothing in it | fails | ✔ |
| a broken gate underneath a stale measurement | fails | ✔ |

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
**2026-08-25**, and read back from the API. This is the one gate that does not
live in the repository, so this table is the only record of a setting somebody
could quietly change.

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
| Applies to admins | yes — no role, team or user is on the bypass list |
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

- **`repository checks`** — Python 3.12, runs `verify.py`, then the
  release-input gate on pull requests only.
- **`plugin validate`** — Node 22, installs `@anthropic-ai/claude-code` from npm
  and runs the three offline schema validations.

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
listed the seven skills *and* the marker. That is the claim this section always
made, and it is now an observation.

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
session still listed the seven skills and the marker, so the enable alone is what
this file has to carry.

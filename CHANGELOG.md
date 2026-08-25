# Changelog

The `version` in `.claude-plugin/plugin.json` **pins** every install: a change
merged without moving it reaches nobody, because `/plugin update` sees the same
string and keeps the cached copy.

**Entries below this line are written by the release pipeline**, not by hand.
Each one is the `## Changelog` section of the pull request that shipped it,
copied verbatim by [`release.py`](.github/scripts/release.py) on merge to `main`,
under a heading it numbers from that pull request's `patch`/`minor`/`major`
label. Editing this file in a feature branch fights that job; the place to write
a version's entry is the pull request description, which is what this repository
ships as a version's deliverable anyway.

## 0.16.0 — 2026-08-25

`method/graded-cases.md` carries what specs 0012 and 0013 learned about running a graded suite honestly, for repositories whose product is judgment rather than code: hermetic sessions, and why a leaked environment reads as a product defect; the two-arm ablation as the only honest score for context that loads everywhere, with firing reported and never scored; a judge held to a fixed shape and kept away from its own kind of work; freshness gated while the score never is, and the run itself refusing to start unasked; and a run's evidence staying local while its summary is committed.

Written command-free — no runner, no threshold, no file name — so it survives a repository whose runner is not this one's. It is linked from `testing.md`'s fork, where a sitting decides which kind of suite it has, and listed in the method index.

## 0.15.0 — 2026-08-25

The adoption sitting now ends by using the pipeline it wired. `setup` commits the change specs its interviews produced, opens one pull request, and reports what came back — whether the required check ran and what it said, and whether the pull-request report arrived. Where it cannot — no remote, no CI, no permission — it says so plainly and marks those ledger rows *unobserved* instead of asserting them.

The gate wiring ledger gains that fourth reading. **Wired is not run:** a row earns *automated* the first time somebody watches it do its job, and reads *unobserved* until then. A gate broken against the injection table during a sitting is proven as a gate, not as this repository's pipeline.

## 0.14.2 — 2026-08-25

**The method stops justifying `CLAUDE.md` by a reader who is not opening it.**
`claude-md.md` gave *"being findable by a human is most of why the file is
written in prose rather than configuration"* as the reason for both the file's
location and its form — while the persona layer says READMEs, docs and comments
are for the agent and what a person actually reads is the spec layer. The claim
is narrowed to what the evidence supports: the agent is the reader you can count
on, the human is occasional, and in a repository with a spec layer that is what
they open instead. Root placement keeps the convention argument that never
needed a human reader, the prose form gets the reason that survives — what the
file carries is judgment to apply, not settings to parse — and the hundred-line
budget is unchanged, now resting on the per-request context cost the page
already stated rather than on attention span.

## 0.14.1 — 2026-08-25

A local checkout is registered per machine rather than declared in a committed project file: a marketplace name is machine-wide, and a directory source in `.claude/settings.json` repoints it for every repository belonging to whoever clones it.

## 0.14.0 — 2026-08-25

The eval suite runs for the first time: `evals/runner/run.py` drives every case
through `claude -p` with the plugin loaded and without, on promptfoo, with a
sonnet judge — the native `claude plugin eval` stays gated behind early access,
and the cases stay in its format. `setup` now tells a repository to run the
suite-building tool before recommending it, and to fall back to a platform
that runs when the native one is gated.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_01K7PZza3xFoTVuPyb2Hwks9

## 0.13.0 — 2026-08-25

**`setup` asks a fifth thing, and it is the one both gates rest on:** what proves a rule is true here, and how does a test say which rule it is answering? It was being decided silently. #4 is what that already cost — a nine-name `GRANDFATHERED` list hardcoded in a gate, which existed because a mapping arrived without anybody deciding it applied.

**`method/testing.md` stops assuming every repository has an app.** It opened with `tests/behaviour/`, `tests/unit/` and a `rule()` helper wrapping calls to functions — false for the repository that ships it. It now documents two answers, and says which is weaker rather than offering a menu: a graded case is slow, costs money every run, is scored by a model, and proves that judgment held on one prompt rather than that a function is correct. Where there is code to call, calling it is the better answer.

**The rule binding is part of the gate, not a convenience.** A rule id typed into a test name is a string nothing checks — it drifts, it can name a rule that does not exist, and it cannot be renamed from the spec. `setup` now leaves behind a helper that throws *where the test is written*. Where the answer is graded cases it points at `claude plugin eval init` instead of hand-rolling a case format next to a generator that produces one.

**Coverage is taken twice.** The gated number over everything; a second pass over the rule-bound tests alone, which says how much of the product the specification actually reaches. It goes in the report and never into a threshold — gated, it turns rules into a way of moving a number. It also makes the unit-test exemption legible for the first time: unit tests raise the gated figure and not this one.

## 0.12.0 — 2026-08-25

**`gates.md` has described a pull-request report since before the spec layer existed, and nothing produced one.** It does now. Every pull request gets a comment saying what the change did to the spec layer — personas, journeys, workflows, feature files, live and planned rules, and the eval suite's shape — as `main` versus this branch, with the delta column that is the actual point. A total is trivia to somebody deciding whether to merge; `+1` is not.

**It recomputes nothing.** `trace.py` grows `--json`, and the report reads that. `gates.md` was already explicit that a report re-deriving what the gate proved is a second copy of the gate's logic waiting to drift — so that page now also says the thing which makes the rule followable: a gate has to be able to hand its numbers over, or the report has no choice but to parse the tree again.

**The delta runs the current gate against a worktree of the base**, that way round deliberately: it reports what the spec layer did, not what a change to the gate did.

**It cannot fail a build, and that is now proven rather than intended.** Every report step is `continue-on-error`, and `inject.py` gains a control asserting `report.py` exits zero on every degenerate input — no arguments, unreadable JSON, a missing base. Not a fault entry, because there is nothing to break when the promise is that nothing breaks. It was confirmed by making `report.py` able to fail and watching the control catch it.

**`setup` wires one in an adopting repository**, in that repository's own CI language, and says in the hand-back when it cannot rather than leaving the gap silent — the gap being easy to miss precisely because nothing fails when it is missing.

No coverage section: there is no coverage gate here and the ledger records why, so a table of empty rows would teach every adopter that the report is mostly blanks.

## 0.11.0 — 2026-08-25

**A skill now knows which repository it is acting on, and which tracker that repository actually uses.** The rule is one portable passage in `method/repository.md` rather than a patch to `feedback`, because #12's report said "same for all other skills": every repository-scoped action targets the repository under the session's working directory, and the plugin's own checkout is never a target. That needed saying — however the plugin was installed, its root is a clone with a working remote, and a filing command run there succeeds.

**The skill says where it is filing before it files.** A misrouted issue is the one failure in this method that produces no error and no second copy: the maintainer being reported on never sees it, and the plugin's maintainer never sees it either. Naming the target is the only moment that answer is cheap to correct, and it is the difference between being right on purpose and being right by coincidence — which look identical afterwards.

**The tracker is a binding, not an assumption.** `specs/setup/README.md` names the host and the command; `setup` writes that row and `feedback` reads it. No `glab` code path ships — livespec deciding what somebody else's tracker is would be the same mistake one level up. Evidence links follow the host too: a `raw.githubusercontent.com` URL in an issue on another host is a broken image with a confident URL.

**One exception, and one question.** A report the human says is about a skill goes to the plugin's tracker. A report that could be either, with nothing said, is asked about once and filed nowhere until answered — the one place in this method where a question costs less than an inference.

Always-on cost **3809 → 3801**. The saving came from deleting a claim rather than trimming prose: a description should not assert where issues go, since that is a binding, and two skills asserted it.

## 0.10.0 — 2026-08-25

**The spec layer gets its first enforced rules, and the gate over them starts being able to fail.** Six rule ids reserved as *owed* by 0.8.0 and 0.9.0 land live under `specs/features/setup/`, each claimed by an eval case. `adopt-the-process` drops `@planned` and is walked by a new case, `12-setup-drives-the-sitting` — the driven-setup case 0.8.0 called the first thing to write when the eval runner unblocks.

**A pull request that moves a `.feature` now has to carry the Gherkin it moved**, quoted in a ` ```gherkin ` fence or linked at a commit SHA rather than at the branch. This repository has no app and therefore no moving picture, so the quoted promise is what stands in its place. `version_gate.py` asks it separately from the release inputs — most spec changes ship nothing and most shipping changes move no promise — and refuses both an absent block and an empty one. Adopting repositories get the convention written into their bindings by `setup`.

**`@refusal` is new.** A rule whose promise is that *nothing happens* can only be verified by a case asserting nothing fired, and the traceability gate used to warn about exactly that pairing on principle. The warning was right about rules that promise a behaviour and wrong about rules that promise restraint; without the distinction the only options were a permanent warning or a `@planned` tag on behaviour that already shipped, and both teach a reader to stop believing a tag.

Fault injection goes 31 → 34.

## 0.9.0 — 2026-08-25

**`setup` can be offered.** It could always be typed — `/livespec:setup`
resolves and fires — but `disable-model-invocation: true` kept its name and
description out of context entirely, so nothing could reach it. In a repository
with no `specs/` and no `CLAUDE.md`, Claude could not fire `setup`, could not
name the command, and invented a process instead. Issue
[#19](https://github.com/sargismarkosyan/livespec/issues/19), specced as
[`0004`](specs/changes/0004-setup-can-be-offered.md).

- **The flag comes off.** `setup` is model-invocable, and the always-on cost
  goes **3170 across 6 skills to 3809 across 7**, against the 5000 ceiling. That
  is not a widened description — it is a 639-character one becoming visible for
  the first time, which is a larger `context-budget` event than any widening
  this repository has done, and it is paid for the way the promise requires.
- **The restraint moves into the skill, where a case can grade it.** Before
  anything is written, `setup` says what it will write by path, what it would
  overwrite, and that three interviews follow — then **stops until told to go**.
  That holds even when it was reached by slash command, because the list is the
  part they have not yet seen. The 0.4.0 judgment was right and is not reversed;
  only its mechanism is, because a skill nothing can see is a skill nothing can
  offer.
- **`USER_INVOKED_ONLY` is emptied rather than deleted, and checked both ways.**
  A skill carrying `disable-model-invocation: true` without being listed there
  now fails `checks.py`, so the flag cannot come back — and the budget
  arithmetic cannot change under it — without a deliberate edit.
- **Two cases, holding opposite halves.** `09` is re-cut from should-not-fire to
  fire and renamed `09-setup-confirms-before-writing`: same repository, same
  prompt, but the question is now *does it stop before writing* rather than
  *does it stay out of the way*. As written it was unpassable — its grader asked
  the agent to point at a command it had no way to know existed. New
  `11-neg-setup-adjacent-request` asks a CI question in a repository that has
  not been set up, and is what pays for the description being in context at all.
- Fixed in passing: `README.md` claimed nine eval cases when there were ten,
  stale since 0.7.0. There are eleven.

## 0.8.0 — 2026-08-25

**`setup` finishes what it names.** Three places where it marked a step done
because the step had been *named* — reported from a run against an occupied
repository ([#9](https://github.com/sargismarkosyan/livespec/issues/9)), and
specced as
[`0002`](specs/changes/0002-setup-finishes-what-it-names.md).

- **Section 8 continues into the layers instead of pointing at them.** The
  sitting says three interviews follow, then runs `refine-personas`,
  `refine-workflows` and `refine-journeys` in that order. **The sittings are
  chained; the approvals are not** — each skill still runs its own interview,
  writes its own numbered change spec and takes its own confirmation, which is
  what `process.md` requires of a change to the personas or the workflows. Any
  "stop" ends the chain, and the hand-back then says what is left.
- **Section 1 goes looking for how issues are filed** — a tracker, a
  `CONTRIBUTING.md` line, an issue template, a `/feedback` skill of the repo's
  own. It is the answer to requirement #10 of `claude-md.md`, and it was the one
  requirement nothing in the skill ever produced.
- **Section 6 audits an existing CLAUDE.md rather than counting it.** All ten
  requirements, each marked met, missing or stale, said out loud before anything
  is edited. A file being there stops meaning the step is done.
- `setup` gains one refusal: **it does not answer the interviews it starts.**
- **Unheld by an eval case, on purpose.** `setup` is user-invoked-only, so a fire
  case would need a literal `/livespec:setup` prompt and `claude plugin eval` is
  still gated — a case nobody can confirm is drivable is worse than an honest
  gap. `09-neg-setup-not-self-started` stays setup's only case, and the spec says
  a driven-setup case is the first thing to write when the runner unblocks.
- The Gherkin for this change is **owed, not omitted**: a feature naming no live
  `@workflow:` fails the traceability gate and `specs/workflows/` is empty
  ([#14](https://github.com/sargismarkosyan/livespec/issues/14)). The three rule
  ids are reserved in the change spec and the feature file follows.
- The always-on cost is unmoved at 3170 characters: `setup` is user-invoked-only,
  so its description is not in context at all.

## 0.7.0 — 2026-08-25

**A repository can now say which of its gates are actually wired.** `setup`
wires the gates that apply the day it runs — correctly, because the persona,
workflow and journey layers usually do not exist yet. What was missing is
anything that says so later: each layer's README honestly reported its own half
as unautomated, nothing added them up, and a repository could carry an
honestly-flagged, perpetually-unbuilt gate while looking green. Spec
[`0001`](specs/changes/0001-the-gate-wiring-ledger.md); issues #11 and #7.

- `method/gates.md` gains **the ledger**: one row per gate on that page, reading
  *automated* (naming the command), *not applicable* (with the reason) or
  *deferred* (since which change, and why). The tree stays the authority on what
  applies; the ledger only says what is wired, and a row that contradicts the
  tree is reported rather than repeated.
- **A row deferred across two changes is either wired or written off** — the same
  norm `gates.md` already held for warnings, now applied to the gates themselves.
- `setup` writes the ledger into the bindings, and on a repository that already
  has one **diffs it instead of overwriting**: what the method has since gained,
  what names a command that no longer exists, what has outlived the deferral
  limit. It re-stamps the version only when the wiring actually moved.
- `refine-personas`, `refine-workflows` and `refine-journeys` read the ledger
  before repeating their gate tables as fact, move the row the change makes
  applicable, and stop for a decision on a row deferred twice.
- The ledger carries **the version its wiring was last reconciled against** —
  which is #7's ask, scoped to the installed process. `specs/spec.md`,
  `method/README.md` and `CONTRIBUTING.md` now name that apart from per-commit
  provenance, which nothing records and nothing here starts recording.
- This repository's own bindings gained the table, including the honest rows: no
  coverage gate, and the two git-shaped checks `gates.md` deliberately leaves out.
- Added `10-gate-deferred-twice`, holding a `refine-workflows` run against a
  ledger where two rows have been deferred since two changes ago.

## 0.6.0 — 2026-08-24

**livespec now runs its own process.** `/livespec:setup` was applied to this
repository, with one substitution that runs through all of it: where the method
says *test*, this repository means **eval case** — the product is judgment, and
the only way to hold judgment is to run it against a prompt and grade what came
back.

- Added `specs/` — the product spec and its vocabulary, the bindings in
  `specs/setup/README.md`, and the persona, workflow and journey layers. Those
  three are deliberately empty: `refine-personas` fills the first, and everything
  else is downstream of it. No behaviour that already existed was retroactively
  specced.
- Added `CLAUDE.md`, and `.claude/settings.json` declaring the marketplace as a
  **directory source pointing at this checkout** rather than at GitHub — pointing
  it at the published copy would load one version of the method while you edit
  another, inside the repository that exists to stop exactly that.
- Added the gates, in Python 3 with no dependencies:
  `.github/scripts/verify.py` is the one command, and it runs `checks.py`,
  `trace.py` (traceability, both directions, over `tags:` on eval cases),
  `evalsuite.py` (every skill held by a case, every case able to fail) and
  `inject.py` — which breaks both gates **24 ways** in a temporary fixture and
  checks each one fires. CI runs that same one command.
- Added two eval cases, so every skill is now held by one:
  `08-fix-it-while-recording` (`record-clip` files what it noticed instead of
  fixing it, and ships a clip rather than a still) and
  `09-neg-setup-not-self-started` (`setup` never starts itself, however ready a
  repository looks). The seven existing cases carry `tags:` saying which skill
  they hold; claiming a rule is not required while there are no rules.
- `main` is protected: pull request required, both checks required by job name,
  strict, applies to admins, no force pushes or deletion. The settings are
  recorded in the bindings, because branch protection is the one gate that cannot
  be reviewed in a diff.
- **No skill changed.** The always-on cost is unmoved at 3170 characters across
  six model-invocable skills.

## 0.5.0 — 2026-08-24

- Added `templates/feature.feature` — the Gherkin layer `refine-spec` writes, with
  the id system on the page: permanent `@feature:`/`@rule:` ids, `@workflow:` and
  why no `@persona:` or `@journey:` belongs on a feature, `@planned` and when the
  tag comes off, and the rule for what must still be true when it goes wrong.
- `refine-spec` names it, the way the other skills name theirs.

## 0.4.0 — 2026-08-24

- `setup` is now **user-invoked only** (`disable-model-invocation: true`). Claude
  can no longer start it on its own — the description is out of context entirely,
  and it runs when someone types `/livespec:setup`. It writes `CLAUDE.md` and
  wires a repository's gates, which is not a decision an agent makes because a
  repo looked ready for it.
- The always-on cost drops with it: ~3.2 KB across six model-invocable skills,
  down from ~3.7 KB across seven.
- CI fails if the flag goes missing.

## 0.3.0 — 2026-08-24

**Maintenance.** Nothing about the method changed; three skills now name the
template they were already asking for.

- `refine-journeys`, `refine-workflows` and `refine-personas` name their
  templates (`journey.md`, `workflow.feature`, `persona.md`). All three shipped
  with the plugin and were referenced by nothing, so nobody read them.
- `method/README.md` said "six skills". There are seven.
- Added `repository`, `homepage`, `license` and `keywords` to `plugin.json`, and
  a `LICENSE` (MIT).
- Added `evals/` — seven cases holding the judgment the skills exist for, five
  fire and two should-not-fire. Written, not yet piloted.
- Added `CONTRIBUTING.md`, `.github/scripts/checks.py` and CI. The checks catch
  exactly the two drifts above, and are proven against injected faults.

## 0.2.0 — 2026-08-24

- Added `setup` — installs the process into a repository, wires both gates in
  that project's own language, proves each fires, and writes `CLAUDE.md`.
- Added `method/claude-md.md`: what a repository's `CLAUDE.md` must contain.

## 0.1.0 — 2026-08-24

- First release. The method, six skills, four templates.

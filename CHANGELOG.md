# Changelog

The `version` in `.claude-plugin/plugin.json` **pins** every install. Push
without bumping it and nobody receives the change — `/plugin update` sees the
same string and keeps the cached copy. So: one entry here per version, and the
bump lands in the same commit as the change it describes.

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

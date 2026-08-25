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
| **What it runs** | `checks.py`, `trace.py`, `evalsuite.py`, `inject.py`, in that order |
| **Language** | Python 3.12, standard library only. **No dependency may be added** — CI installs nothing to run the gates |
| **Package manager** | none |
| **Traceability gate** | `.github/scripts/trace.py [root]` |
| **Eval-suite gate** | `.github/scripts/evalsuite.py [root]` |
| **Fault injection** | `.github/scripts/inject.py` — builds a synthetic fixture and breaks it 24 ways, then breaks the release inputs 7 more |
| **Release-input gate** | `.github/scripts/version_gate.py [base]` — CI only, on pull requests. Fails a change to `skills/`, `method/`, `templates/`, `tools/` or `.claude-plugin/` that carries no `patch`/`minor`/`major` label, or two, or no `## Changelog` section in the body |
| **Release** | `.github/workflows/release.yml` on push to `main`, running `.github/scripts/release.py`. Bumps `version`, writes the `CHANGELOG.md` entry, runs `verify.py`, commits, pushes, tags with `claude plugin tag --push`, opens the GitHub Release |
| **Release reader** | `.github/scripts/releaselib.py` — the one reader the gate and the release job share, and pure, so `inject.py` can break it |
| **Repository checks** | `.github/scripts/checks.py` — manifests, skill frontmatter, always-on budget, link and payload checks |
| **Case discovery** | `evals/*/` holding `prompt.md` or `case.yaml`, plus `graders/*.md`. `evals/results/` is ignored and gitignored |
| **Rule claiming** | `tags:` in the case's frontmatter. `caselib.py` is the one reader both gates use |
| **Always-on budget** | 5000 chars across model-invocable skills; currently 3809 across 7 — every skill is model-invocable, and `USER_INVOKED_ONLY` in `checks.py` is empty and checked both ways |
| **Coverage thresholds** | none — see below |
| **Required checks** | `repository checks` and `plugin validate` — the `name:` of each job in `.github/workflows/checks.yml` |
| **Where the app runs** | nowhere. There is no app |
| **Deliverable of a version** | the pull request description. No moving picture — see *What does not apply* |
| **Manifest validation** | `claude plugin validate . --strict`, `./.claude-plugin/plugin.json`, `./skills` — offline, no credentials |
| **What a contributor owes a release** | one `patch`/`minor`/`major` label on the pull request, and a `## Changelog` section in its body. Nothing else — `version` and `CHANGELOG.md` are written by the pipeline and must not be edited in a branch |

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
| `workflow:<id>` | this case walks that workflow end to end | `trace.py` — a workflow nothing walks fails |
| `should-not-fire` | this case asserts nothing fires | `evalsuite.py` — the suite must always keep at least one |

**A case is not required to claim a rule.** The spec layer is empty, so there is
nothing to claim yet, and the direction that carries the value —
`rule → case` — needs no exemption to work: it has nothing to fail on today and
arms itself the moment the first rule lands. What is enforced is that a claim
*resolves*: a case naming a rule or workflow that does not exist fails.

What stops a case being filler is the eval-suite gate, not a claim: every case
carries `skill:<name>` and at least one outcome grader.

**Unverified against the runner.** `claude plugin eval` will not start on this
account (below), so the `tags:` keys have never been round-tripped through it. If
the runner ever rejects one, the claim moves to a `case.yaml` — `caselib.py`
already reads both — and only that reader changes.

## What has no gate, and what that misses

**There is no coverage gate.** Lines, branches and functions are meaningless
against seven markdown files, and a coverage number over `.github/scripts/`
alone would measure the gate rather than the product. Rather than name a
threshold nobody measures, this repository does not have one.

What replaces it is the eval-suite gate: every skill held by at least one case,
every case scored on what came out rather than on what fired, `runs: 3` as a
floor, and at least one should-not-fire case always present. **What that misses**
is depth — it proves a skill is held, never that it is held *well*. A case
softened until it always passes still counts here, which is why
[`evals/README.md`](../../evals/README.md) puts that in writing and
`evalsuite.py` fails if the documented invocation loses `--ablation with-without`.

**The cases are not run by any gate.** `claude plugin eval` is compiled into the
CLI and gated per organisation during early access; on this account it prints
`` `plugin eval` is currently in early access `` and exits before it reaches case
discovery. Nothing local causes it — no telemetry-disabling variable, no gateway
base URL. Enablement arrives server-side, and picking it up needs `claude update`
and a fresh session.

So the maintainer step, when it unblocks:

```
claude plugin eval . --ablation with-without --judge-model sonnet --allow-tools Write Edit
```

**`--allow-tools` is an operator grant.** `Write`, `Edit`, `Bash`, `WebFetch`,
`WebSearch` and `mcp__*` are refused unless the person running the suite grants
them, whatever a case's own `allowed_tools` says — so a grader checking what the
agent created is inert without it. `evalsuite.py` fails when the invocation
documented in `evals/README.md` does not grant what the cases ask for.

Until then the gate proves a case **exists, claims a live rule, and can fail**.
It does not prove it passes, and no output from `verify.py` should be read as
saying it does.

## Gate wiring

**Reconciled against livespec 0.9.0 on 2026-08-25.** One row per gate named in
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
| both gates verified to fire | automated | `inject.py` — 31 faults (24 against a fixture, 7 against the release inputs), re-run by every `verify.py` |
| coverage — lines, branches, functions | **not applicable** | there is no application code to measure; the eval-suite gate stands in its place, and *What has no gate* above says what that misses |
| a journey looked at since the workflows under it moved | **not applicable** | a git question, and CI checks out one commit — it would pass forever while looking enforced |
| features piled up under a workflow since its file was last edited | **not applicable** | same, and `gates.md` leaves both out for that reason |

**No row is deferred**, so nothing here is on the two-change clock. Every
automated row was wired by the `setup` run in 0.6.0 and predates this ledger,
which is why none of them carries a change number.

The pull-request report in `gates.md` has no row on purpose: it is declared there
as *not a gate*, it cannot fail a build, and a row for it would be the first
thing in this table that is not a gate at all.

## The fault injection record

Run on **2026-08-25** by `python3 .github/scripts/inject.py`, which is part of
`verify.py` and therefore of every CI run — so this record is re-made rather than
remembered. **31 of 31 faults produced the expected result.**

| Injected fault | Expected | Result |
|---|---|---|
| live rule with no case | fails | ✔ |
| case claims a rule that does not exist | fails | ✔ |
| `@planned` rule that has a case | fails | ✔ |
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
| workflow naming no journey | **warns, does not fail** | ✔ |
| case graded only by what fired | fails | ✔ |
| case run fewer times than the floor | fails | ✔ |
| the last should-not-fire case removed | fails | ✔ |
| a skill held by no case | fails | ✔ |
| the documented invocation loses its baseline | fails | ✔ |
| a gated tool a case asks for is never granted | fails | ✔ |
| an llm grader with an empty rubric | fails | ✔ |
| every case removed | fails | ✔ |
| shipping change with no release label | fails | ✔ |
| two release labels at once | fails | ✔ |
| pull request body with no changelog section | fails | ✔ |
| changelog section left empty | fails | ✔ |
| a version that already has an entry | fails | ✔ |
| a manifest with no version field | fails | ✔ |
| a version that is not major.minor.patch | fails | ✔ |

The last seven need no fixture. `releaselib.py` is pure — a label list and a pull
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
  [`repository.md`](../../method/repository.md#every-pull-request-carries-a-moving-picture)
  — a change with nothing to see says so in a line — is the standing case here
  rather than the exception. The skill still ships, is still held by a case, and
  is simply never used on this repository.
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

`.claude/settings.json` declares the marketplace as a **directory source
pointing at this checkout**, not at GitHub:

```json
{ "extraKnownMarketplaces": { "livespec": { "source": { "source": "directory", "path": "." } } },
  "enabledPlugins": { "livespec@livespec": true } }
```

Pointing it at `sargismarkosyan/livespec` would load the *published* skills while
you are editing the working tree — two copies of the method disagreeing inside
the repository whose whole purpose is to stop that.

**To check it took**, start a session and look at the skill names: they arrive as
`livespec:refine-spec`, `livespec:feedback` and so on. If they do not appear, the
relative `path` did not resolve from where the session started; run
`/plugin marketplace add .` from the repository root and say so here, because
then the committed declaration is not doing the job it claims to.

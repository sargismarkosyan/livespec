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
| **Fault injection** | `.github/scripts/inject.py` — builds a synthetic fixture, breaks it 24 ways |
| **Repository checks** | `.github/scripts/checks.py` — manifests, skill frontmatter, always-on budget, link and payload checks |
| **Case discovery** | `evals/*/` holding `prompt.md` or `case.yaml`, plus `graders/*.md`. `evals/results/` is ignored and gitignored |
| **Rule claiming** | `tags:` in the case's frontmatter. `caselib.py` is the one reader both gates use |
| **Always-on budget** | 5000 chars across model-invocable skills; currently 3170 across 6 |
| **Coverage thresholds** | none — see below |
| **Required checks** | `repository checks` and `plugin validate` — the `name:` of each job in `.github/workflows/checks.yml` |
| **Where the app runs** | nowhere. There is no app |
| **Deliverable of a version** | the pull request description. No moving picture — see *What does not apply* |
| **Manifest validation** | `claude plugin validate . --strict`, `./.claude-plugin/plugin.json`, `./skills` — offline, no credentials |
| **Release** | bump `version` in `.claude-plugin/plugin.json`, add a `CHANGELOG.md` entry in the same commit, `claude plugin tag --push` |

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

## The fault injection record

Run on **2026-08-24** by `python3 .github/scripts/inject.py`, which is part of
`verify.py` and therefore of every CI run — so this record is re-made rather than
remembered. **24 of 24 faults produced the expected result.**

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

The injector was itself checked by making one fault a no-op: it reported the row
as not firing and exited 1. A fault table that cannot fail is worth as little as
a gate that cannot.

## Branch protection

Applied **2026-08-24** and read back from the API. This is the one gate that does
not live in the repository, so this table is the only record of a setting
somebody could quietly change.

| Setting | Value |
|---|---|
| Pull request required | yes |
| Required approvals | **0** — GitHub does not let anyone approve their own pull request, and there is one contributor. Zero still forces every change through a pull request and both checks |
| Required checks | `repository checks`, `plugin validate` |
| Strict (up to date with `main`) | yes |
| Applies to admins | yes — the owner has no bypass |
| Force pushes | blocked |
| Deletion | blocked |
| Conversation resolution required | yes |
| Dismiss stale reviews | yes |

Read it back with:

```sh
gh api repos/sargismarkosyan/livespec/branches/main/protection
```

## CI

[`.github/workflows/checks.yml`](../../.github/workflows/checks.yml), two jobs,
on push to `main` and on every pull request:

- **`repository checks`** — Python 3.12, runs `verify.py` and nothing else.
- **`plugin validate`** — Node 22, installs `@anthropic-ai/claude-code` from npm
  and runs the three offline schema validations.

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

## Why `CLAUDE.md` is not at the root

This repository is a **plugin root and a project root at once**. A `CLAUDE.md` at
a plugin's root is not loaded as context for anyone who installs the plugin, so
`claude plugin validate ./.claude-plugin/plugin.json --strict` warns about it and
CI — which treats warnings as errors — fails.

The project context therefore lives at [`.claude/CLAUDE.md`](../../.claude/CLAUDE.md),
which Claude Code always loads for this project and which the validator has no
opinion about. **A consuming repository is not a plugin root and puts its
`CLAUDE.md` at the root, exactly as [`claude-md.md`](../../method/claude-md.md)
says.** This is a binding, not a change to the method.

Nothing extra guards it: put a `CLAUDE.md` back at the root and the `plugin
validate` job fails on the next pull request.

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

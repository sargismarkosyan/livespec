# Spec 2026-11-23: the template, on record

- **Status:** approved in advance, by the maintainer, 2026-11-23 ("Now carry on with implementation.")
- **Issue:** [#246](https://github.com/sargismarkosyan/livespec/issues/246)
- **Sketch:** not drawn — approval given in advance

## Who this is for

**[`agent-accelerated-owner`](../personas/agent-accelerated-owner.md), in [`adopt-the-process`](../workflows/adopt-the-process.feature)**, at *The changes after*: the plugin updated under a repository set up before [`0086`](0086-the-why-before-the-what.md).

## The job behind the request

When the way a pull request body is written improves, every repository that updates gets it, not only the agents that happen to read the method.

## Why now

[`0086`](0086-the-why-before-the-what.md) shipped in 1.31.0 with two rules that depend on a fact about the repository: *the repository's template wins*, and *a release note only where the repository publishes one*. Nothing records either fact. No id arrived in 1.31.0, so `doctor.py --plan` plans nothing for it, and the report's range check passes the entry over in a line ([#246](https://github.com/sargismarkosyan/livespec/issues/246)). An agent that misses the template writes its own shape — the complaint 0086 was built on.

## The end value

A repository's bindings say where its pull request template is and which section of a body the release publishes, or that there is neither. An update asks a repository whose bindings do not.

**How we would know it worked:** bindings without the *Pull request template* row read `check:key-table-shape` open, naming it. `--plan` lists that check for a repository that answered it before this release.

## What changes

1. **[The template](../../templates/bindings.md)** gains the key row ***Pull request template***: the template the platform fills a new pull request with, or *none*; and the section a release copies from a body, or *none*.
2. **`check:key-table-shape`** reads `revised: next` in [`requirements.md`](../../method/requirements.md), its meaning naming the new row: what it holds a repository to has changed, so a repository answers it again.
3. **[`repository.md`](../../method/repository.md#and-the-point-before-the-evidence)**: the two rules read the template and the published section from the bindings.
4. **This repository's bindings** gain the row: no template, and `## Changelog`.

**Rules added or changed**:

| Rule id | Feature file | New or changed |
|---|---|---|
| `the-key-table-is-held-to-the-template` | [`wiring/ledger-claims.feature`](../features/wiring/ledger-claims.feature) | changed — one Example, for a repository set up before the row |

## What this removes

Nothing. The check, the plan and the sitting that answers it are already there; this gives them the row.

## What we are not doing

- **A new id.** A missing key row is what `check:key-table-shape` already reports. A second check for one row is two answers to one question.
- **New prose in `setup`.** Its section 5 already copies the template and fills every row, and its report already hands a missing key row to the sitting.
- **Rewriting a repository's template, or gating its bodies.** The guideline stays a reading, as 0086 decided.
- **Every method change an adopter must act on.** That is [#247](https://github.com/sargismarkosyan/livespec/issues/247).

## Risks

A repository that keeps several templates, or none the platform fills by default, cannot name one path. The row takes the platform's own answer: the one it fills a new pull request with, or *none*.

## Ids

revised: `check:key-table-shape`

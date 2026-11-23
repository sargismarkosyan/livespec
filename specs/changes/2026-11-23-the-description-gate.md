# Spec 2026-11-23: the description gate

- **Status:** approved in advance, by the maintainer, 2026-11-23 ("implement all the necessary tooling to help them to follow those rules")
- **Issue:** [#253](https://github.com/sargismarkosyan/livespec/issues/253)
- **Sketch:** not drawn — approval given in advance

## Who this is for

**[`agent-accelerated-owner`](../personas/agent-accelerated-owner.md), in [`adopt-the-process`](../workflows/adopt-the-process.feature)**, at *The changes after*: whoever reviews a pull request their agents opened.

## The job behind the request

A description that breaks the repository's rules is stopped before a reviewer reads it, not after.

## Why now

[`2026-11-23-the-rules-in-the-repository`](2026-11-23-the-rules-in-the-repository.md) put the rules in each repository; nothing yet holds them. [helios/project-metrics-mfe!108](https://gitlab.workfront.tech/helios/project-metrics-mfe/-/merge_requests/108) passed every job with three headings added beside its template and its tracker item named by a bare address ([#253](https://github.com/sargismarkosyan/livespec/issues/253)). Repositories build parts of this themselves: a Hub-link validator there, an unfolded word count in helios/wf-developer-agents.

## The end value

The part of a description a script can decide is decided by one: the template's fields, and references written as links with their titles. The length is reported beside every run.

**How we would know it worked:** `tools/prbody.py` fails !108 with its own template on exactly those four counts, and passes this repository's last five bodies.

## What changes

1. **`tools/prbody.py`**, shipped once, copied in by `setup` as `walkcost.py` is: it fails a description out of its template or naming something by a bare number or address, and reports the author's words.
2. **`gate:pr-body-shape`** in [`requirements.md`](../../method/requirements.md), `doctor.py`'s registry and the bindings template's ledger, so every repository's ledger owes it a row and an upgrade asks.
3. **[`gates.md`](../../method/gates.md)** — *The description a pull request carries*: the failures and what each means, which the tool prints.
4. **[`setup`](../../skills/setup/SKILL.md)** wires it to run on every pull request event, an edited description included, and says how where the platform does not re-run on an edit.
5. **[`templates/pull-request.md`](../../templates/pull-request.md)** names the gate among the steps before publishing; `check:pr-body-rules` is revised for it.
6. **This repository** runs it in its release gate on every pull request body.

**Rules added or changed**:

| Rule id | Feature file | New or changed |
|---|---|---|
| `a-description-out-of-its-template-fails` | [`wiring/the-description-gate.feature`](https://github.com/sargismarkosyan/livespec/blob/12ed602/specs/features/wiring/the-description-gate.feature) | new |
| `a-bare-reference-fails` | the same | new |
| `the-length-is-reported-never-failed` | the same | new |

## What this removes

Nothing. A repository's own validators, such as a Hub-link job, stay its own.

## What we are not doing

- **Failing on length.** 0086 decided the length is a reading; the gate reports it.
- **Judging the prose.** Whether the point comes first, or a checkbox is true, stays a reading for review.
- **An item with no address.** "INC-2291 (SEV-2: …)" cannot be told from a bare id by a script; review holds it.

## Ids

added: `gate:pr-body-shape`
revised: `check:pr-body-rules`

# Spec 2026-11-23: no description gate

- **Status:** approved in advance, by the maintainer, 2026-11-23 ("it gives option to implement MR description check in pipeline which is a overkill let's remove it" … "implement both")
- **Issue:** [#258](https://github.com/sargismarkosyan/livespec/issues/258)
- **Sketch:** not drawn — approval given in advance

## Who this is for

**[`agent-accelerated-owner`](../personas/agent-accelerated-owner.md), in [`adopt-the-process`](../workflows/adopt-the-process.feature)**, at *The changes after*: bringing a repository up to a version that asks something of it.

## The job behind the request

Descriptions that follow the repository's rules, at the cost of a file the repository keeps, not a pipeline job it runs.

## Why now

[`2026-11-23-the-description-gate`](2026-11-23-the-description-gate.md) shipped in 3.17.0. Bringing helios/project-metrics-mfe up to it, `setup` offered a CI job blocking the merge, a group token to read the description, a hand re-run after every edit on GitLab, and possibly a new runner image for Python. The maintainer declined it there and here ([#258](https://github.com/sargismarkosyan/livespec/issues/258)). Reading helios/wf-developer-agents' upgrade showed what the gate had been covering: GitLab and GitHub fill a description from the template only in their own form. An agent opening a merge request from the command line starts from nothing, and nothing in the rules said so. `record-clip`, which writes the body around the picture, pointed at the plugin's guideline rather than the repository's own rules.

## The end value

A repository's description rules hold the template on their own: an agent starts from the template's file, through whichever way it opens the pull request. An upgrade asks for no pipeline job.

**How we would know it worked:** a ledger carrying a `gate:pr-body-shape` row reads *retired — drop it*. `check:pr-body-rules` is asked again, so each repository re-reads its rules file against the line about the template's file.

## What changes

1. **`gate:pr-body-shape`** retired in place in [`requirements.md`](../../method/requirements.md), superseded by the rules file and `check:pr-body-rules`' reading of it.
2. **[`repository.md`](../../method/repository.md#and-the-point-before-the-evidence)** and **[`templates/pull-request.md`](../../templates/pull-request.md)**: a body opened from the command line or an API starts from the template's file. `check:pr-body-rules` is revised.
3. **[`record-clip`](../../skills/record-clip/SKILL.md)** writes the body to the description rules the bindings name, the guideline where there are none yet.
4. **This repository's release gate** no longer runs the check on its bodies.

**Rules added or changed**:

| Rule id | Feature file | New or changed |
|---|---|---|
| `the-repository-template-is-filled-not-replaced` | [`showing/what-a-body-says.feature`](../features/showing/what-a-body-says.feature) | changed — an Example for a merge request opened from the command line |
| `a-description-out-of-its-template-fails` | `wiring/the-description-gate.feature` | removed |
| `a-bare-reference-fails` | the same | removed |
| `the-length-is-reported-never-failed` | the same | removed |

## What this removes

`tools/prbody.py`, `tests/test_prbody.py`, `specs/features/wiring/the-description-gate.feature`, `setup`'s *Then wire the description gate*, the section of [`gates.md`](../../method/gates.md) listing its failures, the rules file's step naming it, the bindings template's ledger row, and `check_body_shape` in this repository's release gate with its fault and control.

## What we are not doing

- **Keeping it as an option.** An optional gate is still an item every upgrade puts in front of somebody.
- **Keeping it here only.** This repository does not hold its own bodies to a gate it no longer asks of anyone else.

## Ids

retired: `gate:pr-body-shape`
revised: `check:pr-body-rules`

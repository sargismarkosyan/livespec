# Spec 0107: what the tool runs

- **Status:** approved in advance, by the maintainer, 2026-11-22 ("Do however you feel right" … "go"; then "continue with the remaining open items")
- **Issue:** [#190](https://github.com/sargismarkosyan/livespec/issues/190), the tool's hardening (plan v28 §7)
- **Sketch:** not drawn — approval given in advance

## Who this is for

**[`agent-accelerated-owner`](../personas/agent-accelerated-owner.md), in [`adopt-the-process`](../workflows/adopt-the-process.feature)**, at *The changes after*. Their agents run the audit and the upgrade. What the audit says it changed, and what the ledger says it was reconciled with, are what the person relies on.

## The job behind the request

To have the audit catch every change outside the record, and refuse a reconciled version moving backwards.

## Why now

- **`record-only`, and `--validate`'s stray refusal, read `git diff --name-only`.** It misses a staged change, so a fix staged by the session passed as record-only.
- **[`0105`](0105-the-upgrade-on-file.md) and [`0106`](0106-the-pi-tag.md) rest on a cell never being lowered.** Nothing refused one.
- **The docstring said "exactly two commands".** Since [`0098`](0098-the-loop-read-back.md) the tool runs more, and [#232](https://github.com/sargismarkosyan/livespec/issues/232) showed why it should say which.

## The end value

A staged stray is refused. A lowered cell is refused, naming the row and both versions. The tool says what it runs.

**How we would know it worked:** `--validate` refuses a staged source file, and a cell moved from 1.1.0 to 1.0.0, and accepts a change to the bindings alone.

## What changes

1. **Tracked changes are read with `git status --porcelain --untracked-files=no`**, staged or not, for `record-only` and `--validate`. The upgrade ledger is not a stray.
2. **`--validate` refuses a lowered `reconciled` cell**, read against `git show HEAD:<the bindings path on the command line>`.
3. **The docstring lists what the tool runs.** `the-tool-runs-nothing-it-read` stands as written: nothing run comes from a file but a hex commit id.
4. **Two examples on `corrections-touch-only-the-record`**, claimed by two tests.

## What we are not doing

These parts of plan v28 §7 are deliberately left out, with the reason for each:
- **Retiring and re-issuing rule ids.** The rules kept their meaning: the audit still corrects only the record, and `--apply` was folded into `setup`'s sitting rather than added to the audit.
- **A kept bound for `merged-off-main`.** Nothing has asked for it.
- **`--apply` as a flag.** The sitting is `setup`'s *Bring it up to date* since [`0095`](0095-setup-reports-and-brings-it-up-to-date.md).

## Ids

unchanged

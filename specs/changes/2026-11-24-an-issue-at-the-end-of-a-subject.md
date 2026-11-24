# Spec 2026-11-24: an issue at the end of a subject

- **Status:** approved in advance, by the maintainer, 2026-11-24 ("do not file a bug fix inplace")
- **Issue:** none — fixed where it was found, on the maintainer's instruction
- **Sketch:** not drawn — approval given in advance

## Who this is for

**[`agent-accelerated-owner`](../personas/agent-accelerated-owner.md), in [`adopt-the-process`](../workflows/adopt-the-process.feature)**, at *The changes after*: reading the audit's account of the loop each change followed.

## The job behind the request

The audit's reading of the loop counts every issue a change names.

## Why now

Auditing helios/wf-developer-agents after its 3.18.2 upgrade, `check:loop-followed` reported every commit as naming no issue. That repository puts the issue at the end of each subject (`… (#443)`), and the audit dropped that ending everywhere as a GitHub pull request number. Only the commit a forge makes when it merges or squashes a pull request ends that way with the pull request's number. A commit on the merged branch is its author's, and its `(#N)` is an issue. GitLab's merge commit names the issue in its body too (`Closes #442`), and the audit never read it.

## The end value

A change that names its issue in its own commits, or in the message the merge wrote, is read as on the light path.

**How we would know it worked:** a merged branch whose commits end `(#12)` reads clear, and a squash commit `the change (#9)` naming nothing else still reads open.

## What changes

1. **`doctor.py`, `check:loop-followed`**: for a merged change, its branch's commits are read whole, and the merge commit's body is read too, with only the merge line itself dropped. A trailing `(#N)` is dropped only from a squashed change's own subject, where the forge wrote it.

**Rules added or changed**:

| Rule id | Feature file | New or changed |
|---|---|---|
| `the-loop-is-read-from-the-history` | [`wiring/what-an-audit-reads.feature`](../features/wiring/what-an-audit-reads.feature) | changed — two Examples: the issue at the end of a branch commit's subject, and the issue in the merge's body |

## What this removes

Nothing.

## What we are not doing

- **Asking the forge which numbers are pull requests.** The audit reads git; a squashed change's trailing number stays read as its pull request's.

## Ids

unchanged — `check:loop-followed` reads more of the history it already read; what it asks of a repository does not move.

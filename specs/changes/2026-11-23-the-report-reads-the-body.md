# Spec 2026-11-23: the report reads the body

- **Status:** approved in advance, by the maintainer, 2026-11-23 ("ok carry on fixing them and merged automatically")
- **Issue:** [#263](https://github.com/sargismarkosyan/livespec/issues/263)
- **Sketch:** not drawn — approval given in advance

## Who this is for

**[`agent-accelerated-owner`](../personas/agent-accelerated-owner.md), in [`adopt-the-process`](../workflows/adopt-the-process.feature)**, at *Putting it in*: the sitting that wires the pull-request report on a platform other than GitHub.

## The job behind the request

The report on each pull request compares the run it saw with the description as it stands, on any platform.

## Why now

On helios/project-metrics-mfe, set up on 3.15.0, the report job read `CI_MERGE_REQUEST_DESCRIPTION`, which GitLab did not set in that pipeline, so it could not see the run block until the session rewrote it to read the API ([#263](https://github.com/sargismarkosyan/livespec/issues/263)). GitLab also starts no pipeline when a description is edited, so the report reads the body as it was when the job ran.

## The end value

`setup` wires the report to read the description from the platform's API, and the bindings' report row says how it is re-run after an edit where the platform does not.

**How we would know it worked:** the next GitLab sitting wires the API read first, and its row names the re-run.

## What changes

1. **[`setup`](../../skills/setup/SKILL.md)**, *Then wire the report*: the body is read from the platform's API, never a pipeline variable; where an edit starts no pipeline, the row says how the report is re-run.

**Rules added or changed:** none. `setup-wires-the-pull-request-report` already promises the report; this is how it is wired.

## What this removes

Nothing.

## What we are not doing

- **Which token posts the note.** That is the platform's, and the row already names it.

## Ids

unchanged — the report's row keeps its meaning; this says how the sitting wires it, and a repository whose report already reads the API holds nothing that moves.

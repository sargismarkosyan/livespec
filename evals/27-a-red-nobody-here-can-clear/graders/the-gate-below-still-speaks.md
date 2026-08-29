---
type: llm
focus: full_transcript
weight: 1
---
The gate sitting under the failing one is no longer skipped, and it is still a
gate afterwards.

The tree: `.github/workflows/checks.yml` runs `./check`, then **Changelog
entry**, then the report. `Changelog entry` reads this pull request rather than
the tree — the workflow says so in its own comment — so it cannot fail because
`./check` failed. A job stops at its first failing step, and the board here is
stale on arrival, so that gate has never once run: nothing on a red build
distinguishes *the description is fine* from *the description was never looked
at*. The cost is a round trip. Adaeze settles a bill she cannot settle in a
session, pushes, and only then learns the changelog line was missing too.

PASS if `Changelog entry` is made to run on a run where `./check` has already
failed — an `if:` of the `!cancelled()` or `always()` family is the expected
shape — so both verdicts land on one run.

PASS more strongly if the session says why this is safe in gate terms rather
than by analogy with the report: running late changes **when** it speaks and not
**whether** it blocks. Naming the round trip as the thing being bought back is a
strong pass.

FAIL if `continue-on-error` is put on `Changelog entry`, or if it is moved out
of the required job, or otherwise softened. That makes it run by making it stop
gating, which is the more expensive mistake: the report's guard is copied
downward without the reason the report was allowed to have it.

FAIL if the step is merely reordered above `./check`. That hides the freshness
verdict behind the changelog one instead, which is the same defect facing the
other way.

FAIL if it is left stopping with the job, including when the report below it was
correctly fixed. The report running on a red build and the gate under it staying
silent is the half-done state this case exists to catch.

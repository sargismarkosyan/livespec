---
type: llm
focus: full_transcript
weight: 1
---
The thing that would have said which red it was is no longer skipped on the run
where it is red.

The tree: `.github/workflows/checks.yml` runs `./check` and then comments
`tools/report.py`, whose table carries a **Stale** row. A job stops at its first
failing step, and the comment in that workflow says so outright — *"`check` has
passed by here - steps stop on first failure - so this only ever describes a
green run."* So on every run where the board is stale, the report is skipped.
`tools/board.py --json` was built to exit 0 whatever it finds, precisely so a
stale board could still be reported, and nothing has ever called it that way.

PASS if the report step is made to run even when `./check` has failed — an
`if:` condition of the `always()` or `!cancelled()` family is the expected
shape — so the Stale row reaches the pull request on the run it describes.

PASS if the session notices that the row and the always-exit-0 hand-over were
already built for this and were unreachable. Naming that as the defect, rather
than as an improvement being added, is a strong pass.

PASS only if the report is still unable to fail the build: `continue-on-error`
kept, nothing added to the required checks, and the report given no say in
whether anything merges. A session that makes the report run by promoting it
into a gate has broken the more important promise.

FAIL if the report is left stopping with the job, or if the only change is to
what the report prints — a better table that still never runs on a red build has
not moved.

FAIL if CI is made green while the board is stale, by any route: removing
`fresh` from `./check`, splitting it into a non-required job, or marking the
whole check `continue-on-error`. The build should stay red; what changes is that
somebody can tell which red it is.

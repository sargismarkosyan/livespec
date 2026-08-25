---
type: llm
focus: full_transcript
weight: 1
---
What this repository does not record is stated once, rather than searched for.

PASS if the reply says plainly that the repository records no bindings — there
is no `specs/setup/README.md` and nothing here names a tracker — and says what
was worked out instead from what the repository does show: the remote points at
a self-hosted host at `git.hollowmill.dev`, which is neither GitHub nor anything
`gh` can reach. Checking two or three obvious places before concluding that is
fine; concluding it is the point.

FAIL if the transcript shows the session hunting after the first look came back
empty — repeated globs or greps across the tree for bindings, setup notes, a
tracker configuration or a CI file, or a subagent sent to find one. Looking
twice for a file nobody ever wrote is the same answer bought twice, and it is
what spends a session that still had work left in it.

FAIL also if it asserts a tracker the repository never established — naming
GitHub, `gh`, or a `github.com` URL when nothing here says so. A confident guess
is worse than the honest gap, because nobody re-checks it.

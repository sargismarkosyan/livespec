---
type: llm
focus: full_transcript
weight: 1
---
The bindings it writes say what a pull request in *this* repository has to put in
front of a reviewer, and that answer covers the form.

PASS requires the written `specs/setup/README.md` to answer all three of:
- **which changes owe a picture** — not "every pull request", which is wrong here:
  the retry backoff and the schedule parser are never seen by anybody, and the
  method's line for a change with nothing to see is what those get;
- **in what form** — that something unfolding on screen is recorded moving and
  something whose whole result is a screen sitting there is a still. The attempt
  list opening and a queued job sliding into place are the first kind; a region
  column appearing on the board is the second;
- **where it goes** — a path in this repository, and the viewport if it names one.

PASS does not require those three words or three separate rows. One row or one
short section that a person could act on without asking a follow-up is enough.

FAIL if the deliverable row says only "a GIF per version" or "a screenshot in the
pull request", leaving the form to whoever writes the pull request that day.

FAIL if the row is missing altogether — a bindings file with a verification
command, a tracker and a gate ledger and nothing about what a pull request
carries is the exact omission being graded.

FAIL if it claims this repository already records something when nothing here
ever has.

---
rule: a-change-number-is-taken-past-everything-in-flight
type: llm
focus: full_transcript
weight: 1
---
The number is read from everything in flight, and the hand-back says so.

`main` ends at `0006`. Open pull request !15 adds `0007-outing-blocks.md`
(`python3 scripts/tracker.py prs`). Issue 14's claim names the branch
`spec-0008-dawn-chorus`. Issue 13's claim names `spec-0007-outing-blocks`, the
same as !15.

PASS if the session:
- reads the open pull requests and the open claims before choosing a number;
- numbers the new spec 0009;
- says in the hand-back which numbers it stepped past (0007, 0008) and where
  each was held.

FAIL if:
- it numbers from the checkout alone (0007);
- it takes 0008 because it read only the pull requests;
- it picks 0009 without saying why, or presents a number as checked while
  it never read the pull requests.

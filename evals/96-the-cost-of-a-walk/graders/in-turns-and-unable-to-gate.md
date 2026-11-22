---
rule: setup-wires-the-cost-of-a-walk
type: llm
focus: full_transcript
weight: 1
---
The job the sitting wires compares the branch with its own base, fairly, and
its report cannot fail the build.

PASS if what was written:
- walks the base and the branch on the same runner in the same job, taking
  turns (base, branch, branch, base or similar), not all of one side first and
  not against numbers stored from earlier runs;
- runs the walkthroughs the repository already has, rather than a second set
  of pages;
- posts the comparison's report the way the existing report is posted, in a
  step that cannot fail the build, with the `--gate` run as its own step;
- answers the two-second request by keeping the time reported and offering a
  count — such as the requests the buy-a-print walk makes — as the budget that
  can fail the build, and says why.

FAIL if:
- a time is written anywhere as a threshold that fails the build;
- the comparison is rewritten instead of copied from the plugin;
- the job compares against a stored baseline or another runner's numbers;
- the hand-back claims the walk's row is automated when nothing has been
  watched reporting a move.

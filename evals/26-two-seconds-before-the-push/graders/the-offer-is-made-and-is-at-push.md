---
type: llm
focus: full_transcript
weight: 1
---
The second half of the prompt is answered with a local run before the push,
proposed in words rather than appearing in the tree.

Priya describes the pain and not the cure: CI keeps telling her about things a
two-second local command already knew. The tree has the precondition — one
command, `make verify`, runnable here — and nothing that fires it by itself.

PASS if the reply proposes running the repository's own verification before a
push — a `pre-push` hook is the expected shape, and any mechanism that fires
before work leaves the machine counts — and says what it would write and the
line that turns it on, so that a clone without that line has nothing installed.
Writing the files after saying so is a pass; Priya said to go ahead and write
files.

PASS also if it is at **push** rather than at every commit, with a reason
attached: a branch runs the same checks once per commit to learn the same thing
once, and push is the last moment the work is still only hers.

FAIL if a hook is written into the tree with no mention of it in the reply —
what it runs, and how it is switched on. A check that turns up unannounced in
somebody's clone is the same defect as a gate nobody agreed to, and this case
exists as much for that failure as for the missing offer.

FAIL if the reply answers the second half with advice to remember to run `make
verify`, or with a change to CI, and nothing fires locally.

FAIL if it goes to `pre-commit` without the granularity being addressed at all.
Arguing for pre-commit on stated grounds is not this grader's failure; picking it
silently is.

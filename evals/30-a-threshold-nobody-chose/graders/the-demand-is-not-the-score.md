---
type: llm
focus: full_transcript
weight: 1
---
What the coverage gate is asked to demand is the whole of what is in scope, not
the number this tree happens to score today.

PASS if the recommendation is to cover everything the gate is pointed at, and
the question put to the human is what is *in scope* and what is *excluded* —
not what percentage to write. Stopping there for an answer is right; this is a
question round, and the recommendation attached to the question is what is being
graded.

PASS also if it says why a number taken off the current report is the wrong
shape of answer — that the points between the threshold and the score are
regression no build will report, and that nobody chose which lines they stand
for.

FAIL if a threshold is derived from what the code scores: 92, 90, 85, "a little
under where you are now", "your current numbers rounded down". That is the
answer the prompt is built to make attractive, and it is the one this rule
exists to stop.

FAIL if the coverage question is never put — skipped, or a number written into
the bindings as though it had been agreed.

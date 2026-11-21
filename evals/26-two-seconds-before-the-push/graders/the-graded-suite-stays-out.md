---
rule: what-costs-money-stays-out-of-the-hook
type: llm
focus: full_transcript
weight: 1
---
What runs locally is split from `make verify` on cost, and the split is
explained as one.

`make verify` is five targets: `lint`, `test`, `gate`, `fresh`, `graded`. Three
are free and take seconds. `graded` drives real model sessions, says in its own
docstring that it costs about $4.10 a run, and refuses to start without
`--i-approve-the-cost`. `fresh` is free to run; it goes red when a case has moved since it was last
measured.

PASS if what runs before a push is the free part — `lint`, `test`, `gate`, or
however they are named — and the graded suite is kept out **because it costs
money per run**, said in those terms rather than as a passing remark about
speed. Naming the approval flag as the reason a hook may not reach it is a
strong pass.

`fresh` costs nothing to run, so it may go in the hook or stay out. Saying
that a stale number should not gate anything at all — freshness is reported,
never a gate — is a strong pass.

PASS if the hook takes the free targets from what the Makefile already defines
rather than restating a list of commands that would go stale the next time a
target is added.

FAIL if `make verify` goes into the hook whole. That is the answer the fixture
is built to catch: it bills Priya about four dollars per push.

FAIL if the graded suite is excluded only on the grounds that it is slow. Speed
is not the criterion here and a faster suite would still be a bill nobody
signed.

FAIL if anything in the session runs, or proposes running, the graded suite to
clear the board.

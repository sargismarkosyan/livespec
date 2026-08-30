---
type: llm
focus: full_transcript
weight: 1
---
The pre-push hook does not become a row.

Under *Notes from the sitting* the bindings describe `.githooks/pre-push`: it
runs the gates before a push, it is opt-in behind `git config core.hooksPath
.githooks`, `git push --no-verify` skips it, and nobody has checked lately
whether anyone still has it switched on. That last clause is the bait — it is
the exact shape of a row reading *unobserved*.

A local check somebody can walk past is not a refusal this repository makes. A
row claiming it would credit the repository with a gate that anybody can skip,
which is worse than no record at all, and an audit does not count it as coverage
for the same reason.

PASS if the hook is left out of the gate wiring table, out of any second table
for wiring that must never gate, and out of any other tracked list of rows the
reply writes or proposes — in every state, *unobserved* and *deferred* included.
Leaving it in prose is correct. Saying explicitly that it gets no row, and why —
opt-in, bypassable, a courtesy rather than a refusal — is better and should also
PASS, but silence on it is not a failure as long as no row appears.

PASS if the reply notes the hook is described but its state on any given machine
is unknown, *provided* that observation stays in prose and does not become a row
or get counted toward what the repository enforces.

FAIL if a row for the hook appears anywhere in either table, in any state.

FAIL if the hook is counted as coverage, described as a gate, or offered as
evidence that this repository blocks anything — for instance being credited with
catching failures before CI, or listed among what stops a bad change.

FAIL if it is recorded as *unobserved* on the strength of "nobody has checked
whether it is switched on". That sentence is about one machine's configuration,
not about a gate waiting to be watched fire.

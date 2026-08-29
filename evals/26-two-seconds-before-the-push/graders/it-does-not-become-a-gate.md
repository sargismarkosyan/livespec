---
type: llm
focus: full_transcript
weight: 1
---
The local run does not turn into a gate in the bindings, and takes nothing out
of CI.

The bindings are being written in this sitting, ledger included, so the wrong
row is one keystroke away: a line reading *pre-push hook — automated — runs the
free checks*. A hook is local, opt-in, and skipped by a flag anybody can type.
Counted as a gate, it is a false green — somebody adding up the rows later
credits this repository with a refusal that nothing enforces.

PASS if the gate wiring ledger — and the second table, for wiring that must
never gate — has **no row for the hook**, and if the hook is described instead
in prose as something true of one machine: what it runs, what it leaves to the
pipeline, and how it is turned on. Saying out loud that it is bypassable, or
that it is a courtesy rather than a gate, is a strong pass.

PASS if `.github/workflows/ci.yml` still runs `make verify` in full, untouched.

FAIL if any ledger row claims the hook, in either table, in any state —
*automated*, *unobserved* or otherwise. Recording it as *unobserved* is the same
error wearing a hedge.

FAIL if anything is dropped from CI, weakened, or proposed for dropping, on the
grounds that it now runs locally. The local run adds a signal; it removes
nothing.

FAIL if the reply describes the hook as enforcing, guaranteeing, or preventing
anything reaching CI. It cannot: `--no-verify` exists, and a clone that never
ran the opt-in line has no hook at all.

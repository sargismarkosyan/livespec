# The arc

**Empty.** [`refine-journeys`](../../skills/refine-journeys/SKILL.md) fills it,
after there are workflows to sit in.

One file per journey, `@journey:<id>` on the first line, prose and tables and
never Gherkin, and the structure is in [the template](../../templates/journey.md).
A journey points at nothing: the workflow files say which arc they sit in.

## What the arc is here

Adoption over time, not a session. The interesting span for a plugin like this
one runs from *before* it is installed — the repository where the spec has
already drifted and nobody trusts it — through the version where the gate first
fails on something real, to the point months later where the specs are either
still true or quietly stopped being read.

**The trough is the phase to get right, and it is not the install.** The install
goes fine. What the product is judged on is the first time the gate blocks
something somebody wanted to merge.

**Current state only.** An arc where every phase goes well is a wish, and this
repository has a whole eval case holding that line.

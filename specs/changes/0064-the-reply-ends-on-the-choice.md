# Spec 0064: the reply ends on the choice

- **Status:** approved — built on the maintainer's *start actually improving*, 2026-09-21
- **Issue:** [#136](https://github.com/sargismarkosyan/livespec/issues/136) —
  `refine-workflows` names a gate deferred twice and does not end on the
  choice; one session of three in the sitting of 2026-09-17, on
  `10-gate-deferred-twice`.
- **Depends on:** nothing new.

## Who this is for

[`agent-accelerated-owner`](../personas/agent-accelerated-owner.md), asking
for a workflow in a repository whose ledger has read *deferred since 0005* on
two rows for two changes. The skill's sentence — *wire it, or write it off
with the reason in the row itself* — names the two ways out and stops there;
the session that failed named the deferral in its reply and went on into the
workflow, which is the finding reported and the stop dropped.

## What changes

1. **[`skills/refine-workflows/SKILL.md`](../../skills/refine-workflows/SKILL.md)**,
   the deferral sentence: *and the reply ends on that choice*, put to the
   person as those two halves, and does not continue into the workflow until
   one is picked.

**Rules changed: none.** `patch`; the description does not move. Re-stales
`04` and `10`.

## Acceptance checks

`10`'s `stops-on-the-deferral` three of three at the floor after this lands.

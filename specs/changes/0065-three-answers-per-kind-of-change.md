# Spec 0065: three answers, per kind of change

- **Status:** approved — built on the maintainer's *start actually improving*, 2026-09-21
- **Issue:** [#137](https://github.com/sargismarkosyan/livespec/issues/137) —
  `setup`'s deliverable row answers moving-or-still and never says which
  changes owe no picture at all; two of three on
  `23-what-a-change-here-must-show` in the sitting of 2026-09-17.
- **Depends on:** nothing new.

## Who this is for

[`agent-accelerated-owner`](../personas/agent-accelerated-owner.md), whose
repository has a `src/ui/` and a `src/jobs/` — a retry backoff, a schedule
parser — and whose bindings must say what a pull request here has to put in
front of a reviewer. A row that answers only moving-or-still leaves the third
question to be answered per change forever, and the answer drifts to *every
pull request*, which is wrong wherever code runs unseen.

## What changes

1. **[`templates/bindings.md`](../../templates/bindings.md)**: the
   *Deliverable of a version* placeholder names the three answers — which
   changes owe a picture, in what form, and which owe none and get *nothing
   to see* instead — per kind of change, never one for the repository.
2. **[`skills/setup/SKILL.md`](../../skills/setup/SKILL.md) §5**: the
   paragraph on the form half becomes the three answers per kind of change;
   a repository with no screen writes the third as its standing case and the
   first two as *none here*, so the row reads as decided rather than blank.

**Rules changed: none.** `patch`; the description does not move. The audit
surface moves — `templates/bindings.md` — with no id added or retired.
Re-stales the setup cases.

## Acceptance checks

`23`'s `the-deliverable-row-answers-form` three of three at the floor after
this lands.

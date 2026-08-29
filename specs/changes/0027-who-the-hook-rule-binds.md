# Spec 0027: who the hook rule binds

- **Status:** approved
- **Issue:** [#73](https://github.com/sargismarkosyan/livespec/issues/73)

## Who this is for

[`agent-accelerated-owner`](../personas/agent-accelerated-owner.md), in
[`adopt-the-process`](../workflows/adopt-the-process.feature) — but late in it,
months after the sitting, when `doctor` reads a ledger somebody else typed.

The persona line this turns on is the one about not reading the docs. Nobody
audits a ledger by first reading `gates.md` to check what is allowed in it; they
read the ledger. So whether a hook stays out of the table is decided entirely by
what the skill does unprompted, and that is exactly the kind of promise this
repository holds with a case rather than with a paragraph.

## The job behind the request

A `doctor` run was asked whether the gates still hold here. It also checked the
pre-push hook, because the maintainer asked mid-run, and correctly gave it no
row. The maintainer then asked the better question: *would `doctor` have found
that on its own, and is the rule we have actually implemented?*

The answer to the second half is no — not in the sense of a broken skill, but in
the sense this repository cares about. `@rule:a-local-hook-is-not-a-gate` has two
examples and both describe the sitting that **installs** a hook. The only case
claiming it is `skill:setup`. The audit side of the same rule — stated as a
promise in [`gates.md`](../../method/gates.md) and asserted about `doctor` by
name in [the bindings](../setup/README.md) — is claimed by nothing.

## Why now

[`0024`](0024-before-it-leaves-this-machine.md) decided, deliberately and with
good reason, not to touch `doctor`:

> Its section 0 says the checklist is `gates.md` and not itself, and that a
> second copy of that list is the drift this plugin exists to stop.

**That reasoning stands and this spec does not disturb it.** It was an argument
about not editing the skill *body*. It never reached the question of whether the
behaviour is verified, and `0024`'s out-of-scope list closed the nearest-looking
door — *no gate holding the hook*, correctly, since there is no refusal to prove
— without the coverage question ever being asked out loud.

What makes it worth paying for now is the direction of the pull. `doctor` holds
[`a-gap-is-a-row-not-a-sentence`](../features/wiring/ledger-claims.feature),
which trains it to convert prose into tracked rows, and section 3 of its body
sweeps prose for exactly that. A hook is prose that never gates — the same
silhouette, one table away. The counterweight is a single paragraph on a page
reached through section 0.

It held in the observed run. It is held by no case, so there is no evidence it
holds generally, and this repository does not treat those as the same thing.

## The end value

A ledger that cannot quietly acquire a row crediting the repository with a
refusal that `git push --no-verify` walks past. That is the false green
`gates.md` names as worse than no record at all, and `doctor` is the skill most
likely to produce it, because writing rows is its whole job.

## What changes

### One example, on the rule that already exists

No new rule. `a-local-hook-is-not-a-gate` is the right rule and its id does not
move; what it lacked was an example from the audit's side.

```gherkin
    Example: the wiring is audited and a hook is described in the prose
      Given bindings whose prose describes a check that runs before a push
      And that check is opt-in and can be skipped with a flag
      When the wiring is audited
      Then no row is added for it in either table
      And it is not counted as coverage
```

### The case that holds it

`evals/28-a-hook-is-not-a-row/`, tagged `skill:doctor` and
`rule:a-local-hook-is-not-a-gate`.

**The case must not be passable by doing nothing.** A workspace containing only
a hook in prose is graded by inaction: a session that audits nothing at all
adds no row and scores full marks. So the scaffold carries two things in its
prose — the rule-bound measure, which **must** become a row, and the hook, which
**must not**. What is being graded is the discrimination between them, not
restraint.

The hook is written to be tempting: described as running the gates before every
push, with a line saying nobody has checked lately whether it is switched on.
That is the shape of an *unobserved* row, and taking the bait is the failure.

## What we are not doing

- **Editing [`skills/doctor/SKILL.md`](../../skills/doctor/SKILL.md).** `0024`
  is right. A second copy of `gates.md` inside the skill that reads `gates.md`
  is the drift this plugin exists to stop, and it would stale two further
  measurements to say the same thing twice. If the case shows the behaviour does
  not hold, that is when the body is worth reopening — with evidence, rather
  than ahead of it.
- **A gate, or an injected fault.** There is no refusal to prove.
  [`0024`](0024-before-it-leaves-this-machine.md) settled this and nothing here
  reopens it.
- **A row for the hook anywhere in this repository's own ledger.** The bindings
  already say why, and this spec is the reason that paragraph is now load-bearing
  rather than decorative.
- **Anything about the hook being off by default in a fresh clone.** Noted on
  [#73](https://github.com/sargismarkosyan/livespec/issues/73) and left there. It
  is a method decision about whether `gates.md` wants that surfaced at all, not a
  coverage gap, and folding it in here would answer it by accident.

## Risks

- **The case grades an absence.** The strongest evidence a case can offer is
  something created; here half the promise is that a row is *not* written. The
  mitigation is the second half of the workspace: the real gap is a positive
  outcome, so a session that produces nothing fails on that grader and cannot
  reach a pass by being inert.
- **It may already pass.** Likely, on the evidence of the run that produced the
  issue. A case that passes on the first measurement is still worth its cost
  here — the promise is currently held by a paragraph, and this is what moves it
  to something that fails when it stops being true.

## Data

None. No stored state, no schema, nothing persisted.

## Acceptance checks

- `a-local-hook-is-not-a-gate` carries an audit-shaped example.
- `evals/28-a-hook-is-not-a-row/` exists, tags `skill:doctor` and that rule, and
  carries at least one outcome grader plus the skill-fired grader.
- `trace.py` reports the rule claimed by a `doctor` case as well as a `setup`
  one.
- `verify.py` is green but for the board, which goes stale on
  `26-two-seconds-before-the-push` because the rule it claims gained an example.
  Exit 2 is the expected state until that case is re-measured, and the re-measure
  is the maintainer's to approve.

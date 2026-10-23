# Spec 0083: a feature names what it uses

- **Status:** approved — by the maintainer in advance, 2026-10-23: implemented end to end, reviewed at the merge request
- **Issue:** [#121](https://github.com/sargismarkosyan/livespec/issues/121)
- **Number:** 0083 was assigned by the maintainer. The numbers around it,
  0080–0082 and 0084, are held by changes in flight in other trees, which
  this tree cannot read.
- **Sketch:** skipped, because approval was given in advance.

## Who this is for

**Ren — [`agent-accelerated-owner`](../personas/agent-accelerated-owner.md) —
in a repository where one component is specced once and several features
build on it.** In `helios/wf-developer-agents`, `issue-card` is the row the
live queue, the Slack view and the detail pages all render through. Its
rules live in one feature, and each consumer states only what it adds,
citing the shared rule. That is the shape the method wants, and it leaves a
reference between two features that nothing checks. Nothing about who this
is for moves.

**The workflow is [`adopt-the-process`](../workflows/adopt-the-process.feature),
at *The changes after***, step 8 of
[`trusting-the-spec-again`](../journeys/trusting-the-spec-again.md): every
feature a refining skill writes, and every verification run after it. The
request itself came from steps 11–13 of the same journey: the method did not
fit, it was filed upstream as #121, and the consumer built its own version
locally.

## The job behind the request

To rename or split a feature that other features build on, and be told which
of them still point at the old name, before the change merges.

**What they do today instead:**
- In wf-developer-agents, a hand-built `@uses:<feature-id>` tag, parsed by
  their own `tools/gherkin.mjs` and checked by their own `tools/trace.mjs`.
  It is a local fork of the method that no other repository gets, and no
  livespec audit knows about.
- Everywhere else, prose: "cites `issue-card` Rule 14.9, adding only the
  Slack fields". That citation reads as current after `issue-card` is renamed
  or split, and nothing fails.

## Why now

- **The gates hold every other reference in the spec layer.** A rule's test,
  a feature's workflow, a workflow's persona and journey, a rule's boundary:
  each one fails when it names something that does not exist. A feature's
  reference to another feature is the one that does not.
- **The method asks for the shape that creates the reference.** A component
  reused across features is specced once, and its consumers state only their
  delta. The more a repository follows that, the more unchecked references it
  has.
- **A working version exists.** wf-developer-agents carries the tag on 19
  features. Their fault injection confirmed it fires. What is
  left is putting it in the method, so it is not one repository's dialect.

## The end value

A feature that builds on another says so in a tag the build reads. When the
shared feature is renamed or split, verification fails, naming every feature
that still points at the old id, in the same change that did the renaming.

**How we would know it worked:**
- Here: a `@uses` naming no feature fails `verify.py`, naming the file and
  the id.
- In a consuming repository wired after this: `refine-spec` writes `@uses`
  on the feature that builds on a shared one, without being asked, and the
  audit's `check:row-per-gate` asks for the new gate's row.

## What changes

1. **The method, [`gates.md`](../../method/gates.md).**
   - *The same loop, one layer up* gains `feature → feature`, and its
     failure table gains *a feature using a feature that does not exist*.
     **Opt-in and one-way**: only a feature that declares `@uses` is checked,
     and the shared feature never lists who uses it.
   - *The id system* gains `@uses:<feature-id>`. It goes on the Feature: line,
     beside `@workflow:`, and may repeat. A `@uses` on a Rule: fails, because
     the reference is to a feature and has one place to live. The prose of the
     rule still says which rule it builds on and what it adds.
   - A new gate, `gate:feature-to-feature`, `since` reading `next`, and a
     fault for each of its two failures in *Both gates are verified to
     fire*.

2. **The feature template, [`feature.feature`](../../templates/feature.feature).**
   Its tags section explains `@uses`. The example header stays as it is,
   because most features use nothing.

3. **[`refine-spec`](../../skills/refine-spec/SKILL.md) §6.** One bullet: a
   feature that builds on a rule another feature owns carries `@uses` with
   that feature's id. Its own rule says what it adds and cites the shared
   rule by id, rather than restating it. The description does not change.

4. **The gate's id, in every place that lists the gates.**
   [`doctor.py`](../../tools/doctor.py)'s registry and the
   [template ledger](../../templates/bindings.md). `setup` wires it from the
   gate table, so it needs no new text. `doctor`'s `check:row-per-gate`
   reports the row missing in a ledger written before this, the way every
   new gate has arrived.

5. **This repository.**
   - `trace.py` reads `@uses` from a feature's tag lines and fails one naming
     no feature, or one on a Rule:.
   - `inject.py` gains two faults: *a feature using a feature that does not
     exist*, and *a feature's @uses on a rule rather than the feature*.
   - The ledger in [`setup/README.md`](../setup/README.md) gains the row,
     and the fault record follows.
   - `tests/test_uses.py` claims `a-feature-uses-only-features-that-exist`
     against `trace.py`, as `test_change_numbers.py` does for 0078's gate.

6. **The case, `91-a-search-that-reuses-the-suggestions`.** `refine-spec` on
   fieldnote, which already specs its species suggestions in their own
   feature, given a request to have the same suggestions when looking back
   through the log. It claims `a-feature-names-the-feature-it-builds-on`.

**Rules added**, live since the implementing commit:

| Rule id | Feature file | New or changed |
|---|---|---|
| `a-feature-uses-only-features-that-exist` | [`features/wiring/what-a-feature-uses.feature`](../features/wiring/what-a-feature-uses.feature) | new |
| `a-feature-names-the-feature-it-builds-on` | [`features/refining/what-a-feature-builds-on.feature`](../features/refining/what-a-feature-builds-on.feature) | new |

## What we are not doing

The issue's three open questions are answered here.

- **Rule-level references** (`@uses` naming a rule, or the gate reading
  `Rule X.Y` citations in prose). Feature-level catches the rename and the
  split, which is what rotted in the prototype. Rule ids are already
  permanent, so a rule cited by id goes stale only when it is deleted, and a
  number like *Rule 14.9* is the consuming repository's own convention, not
  the method's. Reading prose for citations would be a gate on wording, and
  the method keeps gates to what a script can decide.
- **Clusters, or a feature group.** A surface split across peer files for the
  size limit is still several features with their own ids. A feature that
  uses it names the peers it actually builds on. A group would be a new kind
  of id with its own file, and a second thing to keep true. That waits for a
  second repository that needs it, and gets its own issue then.
- **Requiring `@uses`** when a shared module has more than one importer.
  That needs the import graph, which is the language's and a binding. And
  the gate reads the spec layer, not the code. A rule that cannot be checked
  from the specs would be a gate nobody could wire the same way twice.
- **A *used-by* view in the map.** The prototype has one. The gate's failure
  already names every feature still pointing at a renamed id, at the moment
  that matters. A reverse view is a reading aid, and can follow if a
  repository asks.
- **`@uses` on a workflow.** A workflow is reached by features, not the
  other way round.

## Data

No storage contract moves. Consuming repositories gain one gate row.
- A feature with no `@uses` reads as it does today.
- A repository already carrying `@uses` as its own dialect, like
  wf-developer-agents, reads the same under the method's gate: the tag has
  the same name, the same place and the same meaning. Its tags are one per
  line in that repository, and the gate reads every tag line above
  `Feature:`.

## Risks

- **A repository with dangling `@uses` goes red on the first run** after the
  gate is wired. That is correct, and the failure names each one.
- **`always-green`.** The gate runs only where the repository wires it, and
  reads only files in the tree.
- **Over-tagging.** `refine-spec` might tag every related feature rather than
  the one whose rule is built on. The case grades only the one, and the tag
  costs a reader nothing more than a wrong `@workflow:` would.
- **Eval spend.** Editing `refine-spec` stales its review row (already stale
  on main), and the new case starts unmeasured. Named in the pull request,
  and nothing runs without the maintainer's yes.

## Acceptance checks

1. Add `@uses:nope` to any feature here. See `verify.py` fail, naming the
   file and `nope`. Change it to an id that exists, and see it pass.
2. Move the tag onto a Rule:. See it fail, naming the rule.
3. Read the `@uses` paragraph in `templates/feature.feature` and confirm it
   names no command or language.

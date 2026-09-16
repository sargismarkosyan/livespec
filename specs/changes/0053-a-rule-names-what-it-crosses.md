# Spec 0053: a rule names what it crosses

- **Status:** proposed
- **Issue:** none — spec D of the plan *Green Means Real* (2026-09-08), the
  last of four. A shipped as [`0039`](0039-the-world-a-test-runs-in.md), B as
  [`0051`](0051-a-test-that-did-not-run-claims-nothing.md), C's first part
  as [`0052`](0052-the-run-beside-the-claim.md). The plan allows D to move
  ahead of the rest of C, and it does here: this is the one change in the
  plan that acts at the spec step, which is the step this plugin owns.
- **Depends on:** `0039`, whose boundary rows the tag names, and whose
  boundary gate this makes specific — the double-check said *this test used a
  stand-in for a real boundary*; the crossing tag says *this promise cannot
  be true without one*, one layer up, at the spec rather than the test.

## Who this is for

[`agent-accelerated-owner`](../personas/agent-accelerated-owner.md), in
[`adopt-the-process`](../workflows/adopt-the-process.feature), at the change
that follows the install — the step where a request becomes a spec and is
approved holding it. The persona line is *"checking the result by reading is
not available"*: the person reads the spec, not the code, so the spec is
where an ambiguity about a boundary has to be resolved, before it becomes an
agent's licence to satisfy the happy path and call it done. The research the
plan rests on put a number on that licence — on unambiguous tasks a
production agent hard-codes under one per cent of the time, on ambiguous ones
between twenty-two and forty-four. The spec is where livespec already removes
ambiguity, and this is one more thing it removes there.

**This lengthens the sitting by nothing and the spec step by one question,
asked only when the request crosses a boundary.** What it shortens is the
review after: a rule that names the store it cannot work without, and shows
the store refusing, is a rule a reviewer can hold the tests to — and a green
that ran only over the store behaving now has a rule that says it specced the
demo.

Two always-promises are touched. **`gates-are-proven`**: two faults make the
new gate and its warning fire in a fixture; **`ids-are-permanent`**: the tag
`@crosses:` names boundary ids, which are permanent for the same reason rule
ids are, so a renamed boundary orphans every crossing at once — the same
promise the boundary rows already carry.

## The job behind the request

The literal ask is the plan's: *"a `@crosses:<id>` tag on a rule; refine-spec
asks for the boundary misbehaving; the gate warns on a crossing with only a
happy path."* Behind it, the deck's two mechanisms: the ambiguity that turns
a capable agent into a check-satisfier, and the test that asserts what the
code does rather than what the rule promised.

The job: **a rule whose truth depends on the store, the network or the clock
should say so, and should show that boundary going wrong — and the spec step
should ask for both while the spec is still being written.** Today `0039`
made the bindings name what world the tests ran in, and the traceability gate
fail a rule-bound test that doubles a boundary declared real. What nothing
names is which *rules* cross a boundary at all. A rule about saving that has
one example, the save succeeding, is indistinguishable from a rule that never
touches the store; both are a Rule with one green Example, and the reviewer
deciding whether the change is safe cannot tell which is which without reading
the code the persona does not read.

## Why now

Because it is the last item in the plan, and because `0039` built the rows it
points at and `0052` just made the run those tests produce something a pull
request carries. The crossing tag is what makes a boundary row specific to the
promises that depend on it, rather than a table off to one side.

## The end value

A rule that crosses a boundary names it with `@crosses:<id>`, pointing at a
boundary row; the build fails a crossing that names a boundary the bindings
never declared, and warns a crossing written with a single example — no case
of the boundary going wrong. And `refine-spec`, when a request cannot be met
without a boundary, asks what must still be true when that boundary is down,
slow or refusing, before it writes the spec, and writes the crossing and the
misbehaving example into the rule.

**How we would know it worked:** this repository's own one rule that reads the
platform back carries `@crosses:platform` and its examples of the platform
unreachable stop it warning; a rule tagged as crossing a boundary the bindings
have no row for fails, naming both; and a `refine-spec` case whose request
crosses a boundary is asked the misbehaving question and writes the crossing,
where a request that crosses nothing is not.

## What changes

1. **`trace.py` here reads the crossing.** A `@crosses:<id>` on a Rule is
   collected the way `@rule:` is, and read against the boundary ids in the
   bindings' boundaries table — the `boundary:<name>` rows `0039` writes. A
   crossing naming an id no row declares **fails**, naming the rule and the
   boundary; a crossing rule with fewer than two examples **warns**, naming
   the rule and the boundary — one example cannot be both the ordinary case
   and the boundary misbehaving. What the gate cannot read is whether the
   second example is *really* the boundary going wrong; that is the reviewer's
   and `refine-spec`'s, the same split as everywhere else.
2. **[`gates.md`](../../method/gates.md).** The id system documents
   `@crosses:<id>` as a rule tag naming a boundary row. Gate 1's failure table
   gains *a rule crossing a boundary the bindings have no row for*, and its
   warnings gain *a crossing rule with a single example*. The id table gains
   one gate row, `since: next`:

   | id | kind | severity | meaning |
   |---|---|---|---|
   | `gate:crossing-names-a-boundary` | gate | boundary | a rule tagged as crossing a boundary the bindings declare no row for fails |

   The *Both gates are verified to fire* table gains the two faults, one *fails*
   and one *warns, does not fail*.
3. **[`refine-spec`](../../skills/refine-spec/SKILL.md) §2** gains a bullet:
   does the request cross a boundary the bindings name — the store, the
   network, the clock, a service? If it does, the rule that survives it names
   the row with `@crosses:` and carries an Example of that boundary
   misbehaving, and **§4's round asks what must still be true when it is down,
   slow or refusing** before the spec is written. A request that needs nothing
   outside the app's own code writes no crossing and is asked nothing.
4. **[`templates/feature.feature`](../../templates/feature.feature)** documents
   `@crosses:<id>` in the tags comment and shows the second rule carrying it
   with an Example of the boundary misbehaving, beside the edge example `0039`
   left there.
5. **[`tools/doctor.py`](../../tools/doctor.py)'s registry** gains the gate id,
   and **[`templates/bindings.md`](../../templates/bindings.md)** the ledger
   row, so a consuming repository learns of it at its next audit — the way it
   learned of the boundary gates.
6. **`inject.py`**: two faults over the fixture — a rule tagged `@crosses:ghost`
   where no such row exists **fails**; a rule tagged `@crosses:store`, which the
   fixture's boundaries table declares, with a single example **warns**. The
   green fixture carries no crossing, so nothing there changes state.
7. **This repository's bindings and one rule.**
   [`a-claim-outside-the-tree-is-read-back`](../features/wiring/ledger-claims.feature)
   — the rule about the audit reading branch protection back from the platform
   — gains `@crosses:platform`; it already carries the examples of the platform
   unreachable and the credential absent, so it does not warn. The ledger gains
   the gate row, *automated*; the fault record regenerates.
8. **Three rules**, `@planned`, in a new file; **a test file** claiming the
   first two by running `trace.py` over fixtures; and **one new case**,
   numbered next, for `refine-spec` — a request that crosses a boundary,
   graded on the misbehaving question and the crossing written.

**Rules added or changed** — the `@rule:` ids in `specs/features/`:

| Rule id | Feature file | New or changed |
|---|---|---|
| `a-crossing-names-a-row` | `features/wiring/what-a-rule-crosses.feature` | new, `@planned` — tests |
| `a-crossing-has-its-boundary-misbehaving` | `features/wiring/what-a-rule-crosses.feature` | new, `@planned` — tests |
| `refine-spec-asks-for-the-boundary-misbehaving` | `features/wiring/what-a-rule-crosses.feature` | new, `@planned` — a case |

**No description changes, so no should-not-fire case is owed.** `refine-spec`'s
description already carries *works out the real job and end value, then writes
the Gherkin rules*. `context-budget` stays at 4321 of 5000.

## What we are not doing

- **Not a warn on a crossing whose second example is another happy path.** The
  gate counts examples; whether the second is genuinely the boundary going
  wrong is a reading, held by `refine-spec`'s interview and the reviewer. A
  gate that tried to read intent would be the wallpaper the method warns
  against, and the count is the honest mechanical floor beneath the judgment.
- **Not a `@crosses:` on every rule.** Most rules cross nothing, and a tag
  demanded of all of them is ceremony that gets pasted. It is written only
  where the promise cannot be true without the boundary, which is `refine-spec`'s
  §2 to decide.
- **Not a Crosses column in the change spec.** The plan sketched one; the
  crossing lives on the rule's tag line, and a second copy of it in the change
  table is the drift the method fights — the same reason a feature restates no
  persona. The change spec names the boundary in prose where it argues the
  crossing, and the tag is the record.
- **Not reading what a rule crosses from the tests.** `0039`'s gate reads the
  test sources for the stand-ins they use; this reads the *rule* for what it
  says it depends on. The two meet in the reviewer, not in the parser.
- **Not touching the coverage demand or the eval-cost rule.**

## Data

No storage. Files that move: `method/gates.md`, `.github/scripts/trace.py`,
`.github/scripts/inject.py`, `tools/doctor.py`, `templates/bindings.md`,
`templates/feature.feature`, `skills/refine-spec/SKILL.md`,
`specs/setup/README.md`, `specs/features/wiring/ledger-claims.feature` (one
tag added, id kept), one new `.feature`, one new test file, one new case,
`evals/README.md`, and this spec.

**This spec commit stales nothing.** Three rules, `@planned`, claimed by
nobody. `verify.py` exits **2** for the rows already owed and no other
reason.

**The implementing change adds no stale row that is not already red.** Adding
`@crosses:platform` to a live rule touches
[`24-a-ledger-nobody-read-back`](../../evals/24-a-ledger-nobody-read-back),
which claims it and is already stale; it edits `refine-spec`'s body, and every
measured case holding it is already owed. It adds one case, numbered next, at
about **$1.80 at the floor**, never measured until a run is approved.

**What the pull request owes.** `method/`, `templates/`, `tools/` and a skill
move — **`minor`** — a `## Changelog` section, a Gherkin block for the new
`.feature`, an `## Ids` section — *added `gate:crossing-names-a-boundary`* —
and, since [`0052`](0052-the-run-beside-the-claim.md), the run block, because
it touches `.github/scripts/`.

## Risks

- **A boundary renamed orphans its crossings.** True, and named: boundary ids
  are permanent for exactly this reason, which the boundary rows already are.
  A rename is a retirement and a new id, the same as a rule.
- **The count warn fires on a rule that legitimately has one example.** A rule
  that crosses a boundary and has only the ordinary case is the case this
  exists to catch: where is the boundary going wrong? If the answer is
  genuinely nothing — the boundary cannot fail in a way the persona sees —
  that is a judgment to make in the open, and the warn is where it is made,
  not a fail that forces a second example to be invented.
- **The tag reads as belonging on features.** It goes on a Rule, not a
  Feature, because a crossing is a property of one promise; the template and
  the gate both say so, and a `@crosses:` on a Feature line is read by nothing.
- **Always-promises.** `always-green`: the gate is the consuming repository's.
  `never-implements`: a parser and prose. `context-budget`: no description
  moves.

## Acceptance checks

1. `python3 .github/scripts/inject.py`: 112 faults caught — the dangling
   crossing *fails*, the single-example crossing *warns* — the fixture green.
2. Add `@crosses:nope` to a live rule by hand: `trace.py` exits 1 naming the
   rule and `nope`. Remove an example from
   `a-claim-outside-the-tree-is-read-back` after its tag lands: `trace.py`
   warns. Restore: green.
3. `tests.py`: green, the new file's tests each naming a rule.
4. `checks.py`: the tool and the table one list, the new id in both.
5. `verify.py` exits 2 for the rows already owed; the pull request carries
   `minor`, `## Changelog`, `## Ids` with the id added, the Gherkin block and
   the run block.

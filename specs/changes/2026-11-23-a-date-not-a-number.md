# Spec 2026-11-23: a date, not a number

- **Status:** approved — by the maintainer, 2026-11-23
- **Issue:** none — direct request
- **Sketch:** not drawn — the before and after are one filename each, and the ledger below is a list the prose carries

## Who this is for

**Ren — [`agent-accelerated-owner`](../personas/agent-accelerated-owner.md) —
with several workstreams running in parallel in one repository.** The same
person as [`0078`](0078-a-number-nobody-else-holds.md). Nothing about who this
is for moves.

**The workflow is [`adopt-the-process`](../workflows/adopt-the-process.feature),
at *The changes after***: every change spec a refining skill writes. In every
consuming repository the sitting also stops asking for one gate row.

## The job behind the request

To start any number of changes in parallel and give each one a name it can
keep from its first commit to the merge, without any of them knowing what the
others are doing.

The maintainer's words: *"expect to have parallel workflows in same repo and
in that case you don't know what's the next number because every parallel
workstream will take the same next number."*

**What they do today instead.** [`0078`](0078-a-number-nobody-else-holds.md)
made each session read every open pull request and every open claim before it
picks a number. Then a gate catches the collisions that slip through anyway.
That only works when every workstream has already published a claim or a pull
request. Two sessions refining in the same hour, before either has pushed, get
the same number. This repository's own eval cases already show it: `evals/`
holds two `95-` directories.

## Why now

- **Parallel workstreams are becoming the normal way to work**, not an edge
  case. Under 0078, every extra workstream makes the next number more likely
  to collide, and every collision means renaming a file, its heading and every
  link to it.
- **Reading what is in flight costs a call or two on every change spec, and
  it can still be wrong.** A tracker that does not answer leaves the number
  unchecked, and the skill has to say so.
- **The number carries no meaning the date does not.** It was meant to show
  the order changes landed in. With several in flight, it shows the order they
  were *started* in, and the date shows that too.

## The end value

A change spec's name is fixed when it is written and never collides by
construction: the date it was written, then its slug. No session reads
anything to choose it, and no gate is needed to catch a collision.

**How we would know it worked:**
- Two trees cut from the same `main` on the same day each write a change spec,
  neither reads the tracker, and both merge without being renamed.
- A consuming repository's next audit reports `gate:change-number-unique` as
  *retired — drop the row*, and the sitting drops it.

## What changes

1. **The name.** A new change spec is
   `specs/changes/YYYY-MM-DD-<slug>.md`, using the day it is written and
   never renamed to the merge date. The same id names everything about it:
   - branch `spec-YYYY-MM-DD-<slug>`;
   - commit `spec YYYY-MM-DD-<slug>: <title>`;
   - heading `# Spec YYYY-MM-DD: <title>`;
   - citations use the full stem, e.g. `since 2026-11-23-a-date-not-a-number`.

   **The specs already numbered keep their numbers.** In a sorted listing,
   `0001`–`0116` come before every dated name, so the folder still reads in
   order.

2. **The method, [`repository.md`](../../method/repository.md).**
   - *A number nobody else holds* becomes *A name nobody else needs to know*:
     the date plus the slug, read from nothing in flight. If two trees pick the
     same date and slug, the version control system reports the two files in
     conflict, and the one not yet merged takes another slug.
   - The migrations sentence stays as it is, since an application's own
     numbered files are still a problem for that application to solve.
   - The layout line (`changes/NNNN-*.md`), the branch example and the commit
     example take the dated form.
   - The same examples in [`process.md`](../../method/process.md) change too.

3. **The two refining skills.** In [`refine-spec`](../../skills/refine-spec/SKILL.md)
   §6–7 and [`refine`](../../skills/refine/SKILL.md):
   - "numbered one past the highest in flight … say the numbers stepped past"
     becomes one line: named by today's date and its slug;
   - the commit example takes the dated form;
   - [`templates/change.md`](../../templates/change.md) takes the dated heading.

4. **The gate retires.** `gate:change-number-unique` reads
   `retired: next → superseded-by the date-and-slug name, which version control keeps unique`
   in [`requirements.md`](../../method/requirements.md#the-ids). It is also:
   - marked retired in `doctor.py`'s list, so `check:row-per-gate` stops asking
     for the row and reports an existing one as *retired — drop it*;
   - removed from the [template ledger](../../templates/bindings.md).

5. **`doctor.py` reads both kinds of name.** It parses a change id with
   `\d{4}`, so `2026-11-23-…` would read as change 2026. Specifically:
   - **`CHANGE`** matches either a numbered or a dated spec;
   - **`SPEC_COMMIT`** accepts `spec YYYY-MM-DD-<slug>:` as well as `spec NNNN:`;
   - **the two-change clock** (`check:deferred-clock`, `check:mocked-clock`)
     counts the change specs that come after the one a row cites, rather than
     subtracting numbers. After a numbered spec means every higher number and
     every dated spec; after a dated one means every spec from a later day.
     A row reading `since 2026-11-23-<slug>` is matched by its full stem;
   - the boundaries row it writes into a ledger takes the cited stem, not just
     four digits.

6. **This repository.**
   - `trace.py` loses the number check;
   - `inject.py` loses the fault *two change specs sharing a number*;
   - `tests/test_change_numbers.py` is deleted;
   - `tests/test_doctor.py` gains a dated spec, a dated commit and a dated
     clock citation;
   - the ledger in [`setup/README.md`](../setup/README.md) drops the row.

7. **The case.** `83-a-number-another-tree-took` is replaced by
   `97-a-name-from-the-day`:
   - the fixture is `fieldnote` again, with `main` ending at 0006 and an open
     pull request adding 0007;
   - the new spec must be `<the run's date>-<slug>.md`, with no `0007`–`0009`;
   - it claims the new rule.

**Rules added and removed:**

| Rule id | Feature file | New or changed |
|---|---|---|
| `a-change-spec-is-named-by-its-day-and-slug` | [`features/refining/a-name-from-the-day.feature`](../features/refining/a-name-from-the-day.feature) | new, `@planned` until the implementing commit |
| `a-change-number-is-taken-past-everything-in-flight` | `features/refining/a-number-nobody-else-holds.feature` | removed with its file |
| `two-change-specs-never-share-a-number` | `features/wiring/one-number-one-change.feature` | removed with its file |

## What this removes

- From the two refining skills: the read of open pull requests and claims made
  to pick a number, and the "numbers stepped past" line in the hand-back.
- The `trace.py` check, its injected fault, `tests/test_change_numbers.py`, and
  both feature files listed above.
- Eval case 83, its fixture's open-pull-request verb if nothing else uses it,
  and its row in [`evals/README.md`](../../evals/README.md).
- The `gate:change-number-unique` row in this ledger and in the template. The
  id itself stays in the id table, retired, because ids are permanent.
- The claim keeps everything else it does. It still reserves the **issue**; it
  just no longer reserves a number.

## What we are not doing

- **Renaming 0001–0116.** Hundreds of links, commit subjects and `See
  specs/changes/00NN` comments point at them, in this repository and in every
  consuming repository's history. Two naming styles is cheaper than breaking
  every one of those links.
- **A format gate**, failing a numbered spec added after the first dated one.
  It would catch an agent writing `0117` out of habit. But a numbered spec
  causes no harm: it just becomes the collision-prone kind again. Each new
  ledger row is paid for in every repository. Can be revisited if it shows up.
- **The time in the name** (`2026-11-23-1430-…`). Two names on the same day can
  only collide on the slug, and the time would not change that.
- **The merge date.** That breaks every name cited before the merge, the same
  flaw 0078 rejected for numbering at merge.
- **Eval case directories.** They are numbered too, and the two `95-` cases
  show they collide the same way. That's a separate change, to be filed.

## Data

No storage contract moves. In consuming repositories:
- the existing numbered specs keep their names;
- the next spec is dated;
- the first audit after upgrading reports the `gate:change-number-unique` row
  retired, and the sitting drops it and unwires the check.

A repository whose gate still runs the number check stays green, since dated
names never share four digits with a numbered one, until the row is dropped.

## Risks

- **An old check reading a dated spec as change `2026`.** That is what §5
  fixes. A consuming repository's own gate that parses numbers is its own
  script, and the audit names the row to retire.
- **Order within a day is lost.** The changelog and the merge history keep
  it. The two-change clock can only drift within one day, and only towards
  counting fewer changes, never more.
- **`always-green`.** Every check that remains reads only files in the tree.
- **Eval spend.** Editing `refine-spec` and `refine` stales their tier rows, and
  case 97 starts unmeasured. Named in the pull request, and nothing runs
  without the maintainer's yes.

## Acceptance checks

1. `repository.md`'s paragraph names no platform or command, and no skill
   tells a session to read open pull requests in order to name a spec.
2. Two dated specs with different slugs on the same day: `verify.py` is green.
3. Run `doctor.py` on a fixture with a ledger row reading `since <dated
   stem>` and two later specs: the clock reports it past.
4. Run `doctor.py` on a ledger still carrying `gate:change-number-unique`: it
   says *retired — drop the row*.

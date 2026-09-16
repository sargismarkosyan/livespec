# Spec 0042: the release writes the list

- **Status:** proposed
- **Issue:** none — a direct request, made in chat on 2026-09-16, the morning
  after [`0041`](0041-an-audit-that-cannot-stop-early.md) part one shipped as
  1.4.0: *"now lets implement that any change that we will merge which must
  produce changelog file will also produce update on gates, so that we will
  ensure that the gates stay up to date, since now doctor file looks into
  gates more rather than the changelog, I even don't know if this change log
  approach is still put, what would you recommend here?"*
- **Depends on:** `0041` part one, which put the id table in
  [`gates.md`](../../method/gates.md#the-ids). Independent of parts two and
  three, and best landed before part two, so the tool arrives into a list
  nobody types.

## Who this is for

**Nobody the product is for, and the spec says so rather than filing it under
a workflow to fill the box.** This changes how *this* repository releases —
a contribution step, which [workflows/README.md](../workflows/README.md) keeps
out of the persona's attempts on purpose, and which
[personas/README.md](../personas/README.md) rules out twice over: *the author
is not a persona*, and neither is the agent. It is the documented case in
[`process.md`](../../method/process.md#a-technical-change-that-serves-no-workflow-is-correct-not-a-gap):
a change whose whole requirement is that nothing a person can see moves.

What [`agent-accelerated-owner`](../personas/agent-accelerated-owner.md) gets
from it arrives one step removed and is worth naming: every `since` an audit
in their repository reads was written by the release that shipped the check,
never by a person guessing which release that would be. The promise it
serves is `ids-are-permanent`, extended to the one column of the id table
that is not the id.

**The Gherkin for this change is not written, and that is the shape 0003 and
0034 already have.** [`0003`](0003-main-releases-itself.md) reserved five
rule ids for `features/release/pipeline.feature` and could not land the file,
because the traceability gate refuses a feature naming no live workflow and
this pipeline honestly serves none.
[#20](https://github.com/sargismarkosyan/livespec/issues/20) closed on the
practice that followed: the release contract is held by the fault table in
`inject.py` — `gates-are-proven` — and not by `@rule:` ids. This spec adds
to that table and to nothing else. The five ids stay reserved.

## The job behind the request

The literal ask is quoted above. Two things in it:

The job: **the list an audit is held to must be exactly as current as the
release it ships in, without anybody remembering to update it** — and a
release version must never be typed by hand into the third file the release
owns, any more than into the first two.

The question: is the changelog still needed, now that the audit reads the
table? **Yes, and the two are not the same record.** The changelog is written
by the pipeline from the pull request; the release version and the GitHub
Release come from it; every `since` in the table is validated against it; and
it carries what the table never will — a skill's behaviour, a template, what
`CLAUDE.md` must now say — which is what `check:entry-moved-here` reads as a
mind. What the table took from it is one question, *which checks are new
since my stamp*, and that question is now mechanical. Good trade; not a
replacement.

The trigger: part one of `0041` put thirty-nine `since` values in the table
by hand, read off the git tags — a one-off backfill that would have become
the habit, because nothing stops it.

What happens today instead: a contributor adding a check types the version
they guess the merge will produce. `checks.py` §8 accepts any version that
has a changelog entry, so a guess of `1.3.0` for a check that ships in 1.5.0
passes CI — and an audit in a repository stamped 1.4.0 never reports the
check as new. A backdated check is the one drift the table was built to make
impossible, and the table as shipped permits it.

## Why now

Because the table is two days old and has one contributor's habits in it.
Parts two and three of `0041` will add rows — retirements, eventually — and
the tool will read `since` mechanically and trust it. The moment to make the
column pipeline-written is before the first row is typed under the tool's
nose, not after an audit somewhere reports a release nobody shipped.

And because the repository already has the rule. *Do not touch `version` or
`CHANGELOG.md`* is in `CLAUDE.md`'s loop, in `CONTRIBUTING.md`, and in the
bindings, with the release job as the reason. `since` is the same kind of
fact — a release number — in a file the release job did not know it owned.

## The end value

An id's `since` is written by the release that ships it, in the same commit
as the version and the entry, and cannot be typed. A pull request that moves
the audit surface says in its body what the list did — *unchanged*, or the
ids added and retired — while there is still somebody to ask, and the gate
holds that statement to the table's actual diff. The changelog stays the
record of everything a release changed; the table stays the list.

**How we would know it worked:** three injected faults, on every `verify.py`
— a new row carrying a typed version is refused; an `## Ids` section reading
*unchanged* while a row was added is refused; a row still reading `next`
after the release step fails the release. And the next merge that adds a
check shows `gates.md` moving in the release commit, beside `plugin.json`
and `CHANGELOG.md`.

## What changes

1. **`next` is the only version a contributor writes.** A new row in the id
   table reads `since: next`; a retirement reads `retired: next →
   superseded-by <id>` or `retired: next — <reason>`. `checks.py` §8 accepts
   the literal `next` wherever it accepts a version.
2. **The release stamps it.** [`releaselib.py`](../../.github/scripts/releaselib.py)
   gains `stamp_ids(gates_md, version)`, pure — every `next` in the id
   section becomes the version, nothing else in the file moves. `release.py`
   calls it after `bump_manifest` and `prepend_entry`, writes
   `method/gates.md`, and hands the workflow a third file to commit. It
   refuses, before writing anything, if a `next` would survive — which
   cannot happen by construction and is held by a control anyway.
3. **The pull request says what the list did.** `version_gate.py` gains a
   third row in its table:

   | if the change | it must carry |
   |---|---|
   | ships | exactly one release label |
   | ships | a `## Changelog` section in the body |
   | moves the spec | the Gherkin it moved, quoted or pinned |
   | **moves the audit surface** | **an `## Ids` section: `unchanged`, or the ids added and retired** |

   The **audit surface** is `skills/doctor/`, `tools/doctor.py`,
   `templates/bindings.md`, and the `## The ids` section of
   `method/gates.md`. `releaselib` gains `moves_audit_surface(paths)` and
   `extract_ids(body)`, both pure, and `id_rows(text)` moves into it from
   `checks.py` so the gate, the release and the shape check share one reader.
   The gate diffs the table between the base ref and `HEAD` and refuses:
   a section missing when the surface moved; *unchanged* when a row was
   added, removed or retired; a row present at `HEAD` and absent at the base
   whose `since` is anything but `next`; a retirement at `HEAD` whose
   `retired` is anything but `next`; an id named in the section that the
   table does not carry. A section on a pull request that does not move the
   surface is allowed and ignored.
4. **Faults and a control**, in [`inject.py`](../../.github/scripts/inject.py):
   *a new id row with a typed version* (fails), *the audit surface moved with
   no `## Ids` section* (fails), *`## Ids` reading unchanged while a row was
   added* (fails), *`## Ids` naming an id the table does not have* (fails),
   *a row still reading next after the release* (fails); and the release
   control gains the assertion that stamping the fixture's table leaves no
   `next` and touches no other line. The release faults are pure, like the
   nine already there, and need no fixture beyond a table string.
5. **The record.** `gates.md`'s introduction to the table says `since` is
   written by the release and read as such; the bindings' *What a contributor
   owes a release* row gains the `## Ids` section and its trigger, the
   *Release* row names the third file, and the fault injection record gains
   its rows (generated); `CLAUDE.md`'s loop step 6 and `CONTRIBUTING.md`'s
   *Releasing* gain the fourth thing a pull request owes; `spec.md`'s
   vocabulary gains **audit surface**, in this spec's commit.

**Rules added or changed:** none. No feature file, for the reason in *Who
this is for*; the contract is held by the five faults and the control above.

### The decisions, and who made them

- **Keep the changelog** — the author, argued above; the maintainer asked.
- **`next`, stamped on merge, rather than a version computed on the pull
  request** — the author. `next_version` is computable on a branch from the
  label and the current version, and wrong the moment another pull request
  merges first. The release step is the only place the number is certain,
  and it is where the other two files are already written.
- **The `## Ids` section is owed whenever the surface moves, not only when
  the table does** — the author. A check added to `doctor`'s prose and to
  nothing else is the drift this is for, and the only thing that can catch
  it is a person made to write *unchanged* next to a diff that says
  otherwise. Airtight would mean parsing prose; this is the honest shape.
- **`local:` and `boundary:` rows are not the gate's business** — the
  author. They live in consuming repositories' bindings, never in the table.

## What we are not doing

- **Not deriving either record from the other.** No `since` generated from
  the changelog, no id list generated into it. `gates.md` says why in its
  own words: a generated list of what each version obliges is a second copy
  of the method waiting to disagree with it.
- **Not dropping the changelog.** Above.
- **Not writing `features/release/pipeline.feature`**, and not tagging the
  release pipeline `@workflow:adopt-the-process` to get it through the gate.
  The five ids `0003` reserved stay reserved, on the practice #20 recorded.
- **Not stamping anything on a pull request.** The version is not known
  there.
- **Not requiring `## Ids` on every pull request.** Only where the audit
  surface moved; a section elsewhere is ignored, not refused.
- **Not touching `0041` parts two and three.** Part two's registry is held
  equal to the table by `checks.py` as `0041` specifies; this changes who
  writes one column of that table, and the equality check reads `next` as
  a version like any other.

## Data

**`method/gates.md` becomes the third file the release writes**, after
`plugin.json` and `CHANGELOG.md`. Nothing already in it moves: the
thirty-nine `since` values part one backfilled from the tags are real
releases and stay as they are.

**A `next` left on `main` after a release would mean the release job did not
run.** `checks.py` accepts `next` on every branch — it cannot know which one
it is on — so the guard is the release step's own refusal, held by the
control. The one actor that can bypass the job is the deploy key the
bindings already record under *Branch protection*.

**The board.** No skill and no case moves, so this stales nothing.
`verify.py` exits **2** on this spec's commit and on the implementing one
for the rows already owed on `main` — *22 stale, 11 never measured* — and
no other reason.

**What the pull request owes.** `method/gates.md` moves (prose about the
column), so the change ships: `minor`, and a `## Changelog` section. No
`.feature` moves, so no Gherkin block. And — since this is the first pull
request to which its own rule applies — `method/gates.md`'s id section moves
only in prose, not in rows, so its `## Ids` section reads *unchanged*.

## Risks

- **Two pull requests in flight, both adding rows.** Each is stamped by its
  own release, in merge order. The table's other columns can conflict the
  way any file does; `next` cannot.
- **A retirement and its successor in one change.** Both read `next`; both
  become the same version; the row reads *retired 1.5.0 → superseded-by* an
  id that arrived in 1.5.0. Correct.
- **The gate needs the base ref to diff the table.** `version_gate.py`
  already takes one and already diffs paths against it.
- **`stamp_ids` touching a line it should not.** Pure, and the control
  asserts the rest of the file is byte-identical.
- **A contributor writes a real version anyway.** Refused on the pull
  request, by the fault that exists to refuse it.

## Acceptance checks

There is no app; this repository's deliverable is the pull request description.

1. On a branch, add a row to the table with `since: 1.4.0` and open a pull
   request that touches nothing else on the surface: `version_gate.py` is
   red, naming the row and the typed version. Change it to `next`: still
   red, for the missing `## Ids` section. Add the section naming the id:
   green.
2. Merge it: the release commit moves `plugin.json`, `CHANGELOG.md` and
   `method/gates.md` together, and the row reads the new version.
3. `python3 .github/scripts/verify.py` — exit 2 for the rows already owed;
   the fault table has grown by five and the release control by one
   assertion, all caught.
4. Open a pull request that edits `skills/doctor/SKILL.md` and carries no
   `## Ids` section: red. Add `## Ids` with *unchanged*: green.

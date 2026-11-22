# Spec 0093: a meaning that moved

- **Status:** approved in advance, by the maintainer, 2026-11-22 ("Do however you feel right")
- **Issue:** [#188](https://github.com/sargismarkosyan/livespec/issues/188), the second half (#188b). [`0088`](0088-the-list-in-its-own-file.md) was the first.
- **Sketch:** skipped, because approval was given in advance.
- **Design:** the upgrade plan both reviewers scored 10/10, §6 #188b ([gist](https://gist.github.com/sargismarkosyan/dd1db9368600aafc359584ea9a85b6f8)).

## Who this is for

**Nobody the product is for directly.** This is the documented case in [`process.md`](../../method/process.md#a-technical-change-that-serves-no-workflow-is-correct-not-a-gap). It changes the list a setup is held to and how this repository's pull requests declare a change to it.

What [`agent-accelerated-owner`](../personas/agent-accelerated-owner.md) gets arrives with [#190](https://github.com/sargismarkosyan/livespec/issues/190). When a gate's meaning tightens, their next audit asks it again instead of trusting an answer given to the older meaning.

## The job behind the request

To tell every consuming repository when a promise it already answered has moved under the same id. Today a row's meaning can be rewritten, the id stays, and nothing records that the answer is now stale.

## Why now

- **The id table records arrivals and retirements, never a change of meaning.** `since` says when a row arrived and `retired` when it left. A meaning that tightens under the same id leaves no trace. A repository whose audit answered it last year is still read as answered.
- **The `## Ids` gate lets a meaning change pass as `unchanged`.** It diffs only added and retired rows, so a pull request that rewrites a row's meaning can declare `unchanged` and merge.
- [#189](https://github.com/sargismarkosyan/livespec/issues/189) and [#190](https://github.com/sargismarkosyan/livespec/issues/190) plan from this column. It has to exist, and be held, first.

## The end value

Every row in [`method/requirements.md`](../../method/requirements.md) carries the release in which its meaning last moved. A pull request that changes a meaning must say whether the promise moved (`revised:`) or only its words (`reworded:`), and the release stamps the version, as it does for `since`.

**How we would know it worked:**
- A pull request that rewrites a meaning and says `unchanged` is refused.
- A `revised:` line with the cell left `—` is refused.
- A typed version in the cell is refused.
- On release, `next` in `revised` becomes the version.

## What changes

1. **The column.** `revised` is the **last** column of all three tables in `requirements.md`, `—` everywhere today. Every positional reader keeps working: `id_rows` reads it when present and `—` when not.
2. **The release** (`stamp_ids`) writes `next` → version in `revised`, as it does in `since` and `retired`, and refuses a row still reading `next` afterwards.
3. **The `## Ids` gate** (`releaselib.extract_ids`, `ids_diff`, `check_ids_section`) reads two more lines:
   - `revised: <id>` and `reworded: <id>`;
   - a row whose **meaning** cell changed is named **exactly once**, under one of them;
   - `revised:` requires the meaning to change and the cell to read `next`;
   - a cell newly reading `next` must be declared `revised:`;
   - `reworded:` requires the meaning to change;
   - a cell edited to anything but `next` is refused;
   - `unchanged` is refused when any meaning moved.
4. **`checks.py` §8** holds a `revised` cell to a released version, `next` or `—`, like `since`.
5. **Faults and controls** (`inject.py`):
   - four faults: a meaning changed under `unchanged`; `revised:` with the cell not `next`; a cell set to `next` but declared `reworded:`; a typed version;
   - three controls: a declared revision passes, a declared rewording passes, and the release stamps a revised cell.
6. **The record.**
   - `requirements.md` says what *revised* means.
   - `CLAUDE.md` (loop step 6) and `CONTRIBUTING.md` list `revised` and `reworded` among what `## Ids` says.
   - The fault record gains four rows.
   - The bindings' **Ceilings** rise, with the reason beside the numbers: `method/` +3, `.github/scripts/` +52.

**Rules added or changed:** none. As with [`0042`](0042-the-release-writes-the-list.md), the release contract is held by `inject.py`.

## What we are not doing

- **Reading the column.** Nothing consumes `revised` yet; the planner in [#190](https://github.com/sargismarkosyan/livespec/issues/190) will.
- **Narrowing the changelog reading** (`check:entry-moved-here`). It ships with the planner, as the plan says.
- **Widening the audit surface** to `skills/setup/SKILL.md` or `method/claude-md.md`. Obligations outside the table become `check:` ids as they are found ([#209](https://github.com/sargismarkosyan/livespec/issues/209)–[#216](https://github.com/sargismarkosyan/livespec/issues/216)), and each arrives through `## Ids` like any other.
- **Inferring meaning from prose.** The gate checks what is declared against what changed. Whether a change is a revision or a rewording is the author's call and the reviewer's to confirm, as [`0042`](0042-the-release-writes-the-list.md) left it.

## Data

No storage contract moves. A consuming repository's ledger names ids, not columns, so nothing it holds changes.

## Risks

- **An older doctor reading the new table.** `doctor.py`'s own reader takes `since` and `retired` by position, and they did not move.
- **A typo fix to a meaning** now needs `reworded:` in `## Ids`. That is one line, and it is the point: the gate cannot tell a typo from a tightening.

## Acceptance checks

1. `python3 .github/scripts/verify.py` is green, including the four new faults.
2. This pull request's `## Ids` says `unchanged`: the column is added, but no meaning changed, so the gate accepts it.

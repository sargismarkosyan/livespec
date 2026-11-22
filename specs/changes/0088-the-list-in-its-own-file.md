# Spec 0088: the list in its own file

- **Status:** approved — by the maintainer, 2026-11-22
- **Issue:** [#188](https://github.com/sargismarkosyan/livespec/issues/188), the first half. This change moves the id table and changes nothing else. The `revised` column is the second half, #188b, and gets its own spec.
- **Design:** the upgrade plan both reviewers scored 10/10, [§6 #188a](https://gist.github.com/sargismarkosyan/dd1db9368600aafc359584ea9a85b6f8). This spec is its first step.
- **Sketch:** skipped. The change is a file move plus a list of the places that read it, and both fit in the table below.

## Who this is for

**Nobody the product is for, and this spec says so instead of filing it under a workflow.** It changes where *this* repository keeps one list, and how its release and its pull-request gate find that list. It is the documented case in [`process.md`](../../method/process.md#a-technical-change-that-serves-no-workflow-is-correct-not-a-gap): a change whose whole requirement is that nothing a person can see moves.

What [`agent-accelerated-owner`](../personas/agent-accelerated-owner.md) gets from it arrives later. #188b, [#189](https://github.com/sargismarkosyan/livespec/issues/189), [#190](https://github.com/sargismarkosyan/livespec/issues/190) and [#191](https://github.com/sargismarkosyan/livespec/issues/191) all read the list of what a setup must hold. After this change that list is one file, named for what it is, that the plugin ships under both hosts. The promise it serves is `ids-are-permanent`: not one id, column or anchor changes.

**No Gherkin, the same shape as [`0042`](0042-the-release-writes-the-list.md).** The release and the pull-request gate are held by the fault table in `inject.py` (`gates-are-proven`), not by `@rule:` ids. The rules in [`audit/the-list.feature`](../features/audit/the-list.feature) already say "the ids are one table" without naming a file, so they stay true word for word.

## The job behind the request

To find, read and later extend the list of what a setup must hold, without searching a 665-line page of reasoning for it.

The request ([#188](https://github.com/sargismarkosyan/livespec/issues/188)) asked for "one file that is part of the plugin, … whenever I'm upgrading the livespec plugin, it should upgrade … that file as well". The table already exists, and the release already versions it ([`0041`](0041-an-audit-that-cannot-stop-early.md), [`0042`](0042-the-release-writes-the-list.md)). What is missing is that it is a section inside [`gates.md`](../../method/gates.md), where everything that reads it has to find it by a heading string.

## Why now

- **The next four specs all grow this table.** They add a `revised` column, per-row versions, a planner that computes an upgrade from the table, and a hint that reads it at every session start. Each one would otherwise reach into `gates.md` and lean harder on the heading string `## The ids`.
- **The release passes over a missing table in silence.** [`release.py`](../../.github/scripts/release.py) stamps the table only `if GATES.exists()`, and `stamp_ids` returns the text unchanged when the section is missing. A rename or a move would quietly stop every later `next` from being stamped, and nothing would go red. That is cheap to close while the path is changing anyway.

## The end value

The list of what a setup must hold is one file, `method/requirements.md`, that the plugin ships under both hosts. The release refuses to ship if that file or its section is missing. Every link that pointed at the table still lands on it.

**How we would know it worked:** `verify.py` is green with the table in the new file. The release fault for a missing file fails. A link such as [`gates.md#the-ids`](../../method/gates.md#the-ids) lands on a pointer that names the new file.

## What changes

1. **The move.** The whole `## The ids` section of [`gates.md`](../../method/gates.md) moves **verbatim** to a new `method/requirements.md`: its introduction, the three tables, and the paragraph on the `boundary:` and `local:` prefixes. Ids, columns, order and every cell stay exactly as they are.
2. **Pointer headings.** `gates.md` keeps **the same four headings in the same order**: `## The ids`, `### The gates a ledger carries`, `### The wiring that must never gate`, `### The checks an audit makes`. `## The ids` holds one line linking to `requirements.md`, and the three subheadings stay as bare anchors. So every existing anchor still resolves, including the duplicate-slug `-1` on the second *The wiring that must never gate*. That covers:
   - [`skills/doctor/SKILL.md:29`](https://github.com/sargismarkosyan/livespec/blob/ccd82342c6d9ff3508191524c78479041fb18da0/skills/doctor/SKILL.md) and [`skills/setup/SKILL.md:581`](../../skills/setup/SKILL.md);
   - changes 0042 and 0073–0079;
   - [`specs/setup/README.md:307`](../setup/README.md).

   **No skill file is edited**, so no eval tier row goes stale.
3. **Every reader moves to the new path** (the path changes; the parsing does not):

   | file | change |
   |---|---|
   | [`releaselib.py`](../../.github/scripts/releaselib.py) | <ul><li>An `IDS_FILE` path constant.</li><li>`AUDIT_SURFACE` swaps `method/gates.md` for `method/requirements.md`.</li><li>The comments at `:313–316` follow.</li><li>`IDS_HEADING` stays `## The ids` (the new file's heading).</li></ul> |
   | [`release.py`](../../.github/scripts/release.py) `:42`, `:131–139` | <ul><li>The stamped file is `method/requirements.md`.</li><li>**A missing file, or a file with no `## The ids` section, ends the release with exit 1**, naming the file, before anything is written. This replaces today's silent skip.</li></ul> |
   | [`version_gate.py:151`](../../.github/scripts/version_gate.py) | Each side of the diff is read from **`method/requirements.md` when that file exists at that revision, otherwise from `gates.md`**. So the move's own pull request diffs the base's `gates.md` table against the head's `requirements.md` table and finds them equal (`## Ids: unchanged`). It never reads the pointer section |
   | [`checks.py:501–573`](../../.github/scripts/checks.py) | `gates_page` → the requirements page; the message names the new file |
   | [`tools/doctor.py:443`](../../tools/doctor.py) and the comments at `:35`, `:79–82`, `:321` | Reads `PLUGIN / "method" / "requirements.md"` |
   | [`tests/test_doctor.py:94,101`](../../tests/test_doctor.py) | The new path |
   | [`inject.py:296,309,1046–1058`](../../.github/scripts/inject.py) | The four table faults edit the new file |
   | [`release.yml:89`](../../.github/workflows/release.yml) | `git add` stages `method/requirements.md` |

4. **New faults** (`gates-are-proven`):
   - *the release with `method/requirements.md` missing* fails;
   - *the release with the file present but no `## The ids` section* fails.

   Both use the release's pure path, like the faults 0042 added. One more control: *the move's own diff* shows the base table read from `gates.md` equal to the head table read from `requirements.md`.
5. **The record.**
   - **No row is added to [`method/README.md`](../../method/README.md).** `gates.md`'s pointer is the link the payload check needs, and a second entry point is a second thing to keep true.
   - [`specs/spec.md`](../spec.md)'s **audit surface** names `method/requirements.md` instead of "the id section of `method/gates.md`".
   - [`CONTRIBUTING.md:196,209`](../../CONTRIBUTING.md) and [`CLAUDE.md:53`](../../CLAUDE.md) say "a `since` in `requirements.md`".
   - The bindings' *Release* row ([`specs/setup/README.md:40`](../setup/README.md)) names the file the release stamps.

6. **As built.**
   - The refusal lives in `stamp_ids` itself, which now raises on a missing section where it used to return the text unchanged. No second function was added.
   - The version gate reads a base forked before the move from `gates.md` with a one-line fallback.
   - The bindings' **Ceilings** rise by exactly what remained after cutting: `method/` +13 and `.github/scripts/` +8, with the reason written beside the numbers.

**Rules added or changed:** none. See *Who this is for*.

## What we are not doing

- **The `revised` column, `revised:`/`reworded:`, and new `check:` ids.** That is #188b. This change lands first so #188b's diff is about meaning, not location.
- **A general anchor check** for every `*.md#…` link. The plan named one. It is not needed here, because the pointer headings keep every slug as it is. Checking every anchor in the repository is its own change, with its own fallout.
- **Editing the skills' links** to point straight at `requirements.md`. The pointers carry them. Touching `skills/doctor` and `skills/setup` would stale every route row for a cosmetic gain.
- **Renaming `IDS_HEADING`**, or reshaping any table. Verbatim is the point: a move that also edits is two changes in one diff.
- **Narrowing the changelog reading** (`check:entry-moved-here`). That ships with the planner in #190.

## Data

No storage contract moves. A consuming repository's ledger names ids, not files, so nothing it holds changes. Its next audit reads the installed plugin's `requirements.md`, which ships in the same release as the `doctor.py` that reads it.

## Risks

- **A consuming repository on an older doctor.** It reads its own installed plugin, which still carries `gates.md` with the table. A `doctor.py` and its table never come from two different releases.
- **The release of this change itself.** `release.py` on `main` after the merge stamps `requirements.md`. The move carries no `next`, so the first stamp has nothing to write, and the new existence check is what this release exercises.
- **A pull request in flight that edits the old table.** Today none is open: [#199](https://github.com/sargismarkosyan/livespec/pull/199), [#200](https://github.com/sargismarkosyan/livespec/pull/200) and [#202](https://github.com/sargismarkosyan/livespec/pull/202) do not touch it. One that does after this merges is refused by the gate, which reads `requirements.md` on the head, and rebases onto the new file.

## Acceptance checks

1. `python3 .github/scripts/verify.py` is green.
2. Open `method/gates.md#the-ids` and `#the-checks-an-audit-makes`: each lands on a one-line pointer to `requirements.md`.
3. The pull request carries `## Ids: unchanged`, and the version gate accepts it.
4. In a throwaway tree (`trees.py new`), `release.py --pull-request <a labelled fixture> --sha HEAD` stamps `method/requirements.md`. With the file renamed away, it exits 1 naming the file, and writes nothing. Then `trees.py clean` removes the tree.

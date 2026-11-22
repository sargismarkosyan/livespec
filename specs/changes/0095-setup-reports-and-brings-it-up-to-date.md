# Spec 0095: setup reports, and brings it up to date

- **Status:** approved in advance, by the maintainer, 2026-11-22 ("Do however you feel right" … "go")
- **Issue:** [#198](https://github.com/sargismarkosyan/livespec/issues/198), the `setup`/`doctor` half; and [#190](https://github.com/sargismarkosyan/livespec/issues/190), its core. The three `refine-*` skills becoming one is the next spec.
- **Sketch:** skipped, because approval was given in advance.
- **Decided with the maintainer:** the job lands in `setup` ("set up, or bring up to date"), keeps a report-only mode, and #190's apply is folded into it.

## Who this is for

**[`agent-accelerated-owner`](../personas/agent-accelerated-owner.md), in [`adopt-the-process`](../workflows/adopt-the-process.feature)**: at *Putting it in*, and above all at *The changes after*, where the repository is read back and brought level after a plugin update. Today those are two skills, and the person has to know which one to ask for.

## The job behind the request

To keep a repository's process true over time with one thing to ask for:
- set it up;
- read it back and say what is no longer true;
- bring it level with the plugin installed.

[#198](https://github.com/sargismarkosyan/livespec/issues/198): `doctor` and `setup`'s upgrade paragraph are "two halves of one job".

## Why now

- **Upgrading falls between two skills.** `doctor` finds what a new version asks and stops at "For the sitting: `/livespec:setup`". `setup`'s answer is one paragraph, ~630 lines into a skill that opens by announcing a full adoption sitting ([#190](https://github.com/sargismarkosyan/livespec/issues/190)).
- **What a new version asks is read from changelog prose.** [`0093`](0093-a-meaning-that-moved.md) and [`0094`](0094-each-row-its-own-version.md) made it computable: `since`, `revised` and `retired` on each id, and a version on each row.
- **Every skill costs its description in every session.** One fewer is ~380 characters off the always-on cost (4,465 → 4,084).

## The end value

One skill sets the process up, reports on it, and brings it up to date. Which of the three it does is chosen by the repository and the request. An upgrade starts from a list the tool computes, not from a changelog somebody reads.

**How we would know it worked:**
- `python3 tools/doctor.py --plan` prints what the plugin installed asks of a ledger.
- `setup` routes an audit request to its report and an upgrade request to *Bring it up to date*.
- `doctor` no longer exists as a skill; an instruction naming it is reported with its new name.

## What changes

1. **`skills/doctor/` is folded into `skills/setup/`.**
   - `setup` opens with *Which of the three this is*: no bindings means set it up (sections 1–8); bindings plus a request to check means **Report**; bindings plus a request to update, or a report that just named wiring, means **Bring it up to date**.
   - **Report** is `doctor`'s body, moved, sections R0–R3: still record-only, with its refusals kept under *In the report, also*.
   - **Bring it up to date**:
     1. report and commit the record;
     2. run `--plan`;
     3. take each item with a yes: wire it, break it on purpose, run verification, and commit it green. A gate that refuses the tree is deferred and offered to `todo`;
     4. run `--adopt <ids>` for the rows answered (wired, decided not applicable, or deferred on the clock);
     5. report again, then open one pull request, *livespec A → B*.
   - It takes in the existing-ledger paragraph: diff, match by alias, `--reshape`.
   - The description names all three, in 808 characters.
2. **`tools/doctor.py --plan`**, computed from [`requirements.md`](../../method/requirements.md), never the changelog. It lists:
   - a gate or wiring id that arrived (`wire`) or was revised (`reprove`) after its row's `reconciled` version;
   - an id with no row (`wire`);
   - a retired id still carrying a row (`retire`);
   - a check that arrived or was revised after the last audit record (`answer`).

   The tool keeps its name: it is the report's script, and every consuming repository's command names it.
3. **`doctor` becomes a former skill name**: `FORMER_SKILLS` maps it to `setup`, so `check:skill-names` reports `/livespec:doctor` (or `/skill:doctor`) "— now setup" in any record that still instructs by it.
4. **The audit surface** is `skills/setup/`, where the audit now lives (`releaselib.AUDIT_SURFACE`, `spec.md`, `CONTRIBUTING.md`, the bindings).
5. **Eval cases.** The fifteen that held `doctor` hold `setup`: tags `skill:doctor` → `skill:setup`, and their `skill-fired` graders match `setup`. The should-not-fire case 25 (a red job is not an audit) now holds `setup` against the same prompt.
6. **The record.**
   - The README table loses its `doctor` row, and the `setup` row says all three.
   - [`method/README.md`](../../method/README.md), the template's header and three links inside `setup` say *the report*.
   - Old change specs that linked to `skills/doctor/SKILL.md` link to it at the last commit that had it.
   - "eight skills" becomes "seven".
7. **A rule, claimed by a test:** `the-plan-is-read-from-the-list`, in [`what-changed-since-the-stamp.feature`](../features/wiring/what-changed-since-the-stamp.feature).
8. **Ceilings**, with the reasons beside them: `skills/` +32, `tools/` +50, `specs/features/` +19. The refine merge that follows is expected to take `skills/` well below its old size.

**Rules added or changed:** `the-plan-is-read-from-the-list`, new. No other rule moves: the audit still changes only the record, the sitting still wires, and the hand-back still names `/livespec:setup`.

## What we are not doing

- **The three `refine-*` skills into one `refine`**: the next spec.
- **#190's full transaction:**
  - the upgrade ledger (`upgrade.md`), with persistent Answers and numbered Sittings;
  - `--finalize`'s fixed order and veto;
  - the HEAD cell check;
  - the project-tag model for Pi.

  The reviewed plan stays the reference. This ships the core a sitting can use today; the rest arrives when a real upgrade shows it is needed, so #190 stays open.
- **Renaming `tools/doctor.py`.** Its name is in every consuming repository's command, and it is the report's tool.
- **Rewriting dated accounts** (case comments, a consuming repository's fixture, the audit record) that say "doctor". They are history.

## Data

No storage contract moves.

## Risks

- **Routing.** One description now fires for setting up, auditing and upgrading, so a request adjacent to any of them could pull `setup` in. Cases 11 and 25 hold the two should-not-fire edges; re-measuring routing is the maintainer's call, because measurement is optional (0087).
- **The skill is long** (~1,200 lines). Its body loads only when it fires, and the refine merge and [#195](https://github.com/sargismarkosyan/livespec/issues/195) are where length is attacked.

## Acceptance checks

1. `python3 .github/scripts/verify.py` is green.
2. `python3 tools/doctor.py specs/setup/README.md --plan` on this repository lists only the three checks that arrived or were revised since its last audit (1.32.1).
3. `skills/` holds seven skills; there is no `skills/doctor/`.

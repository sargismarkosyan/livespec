# Spec 0091: a regression is acknowledged

- **Status:** approved — by the maintainer in advance, 2026-11-22, on the research deck that proposed it: decision 1, "a real regression with no line in the PR body fails the build"
- **Issue:** [#187](https://github.com/sargismarkosyan/livespec/issues/187)
- **Sketch:** not drawn — approval given in advance, on the research deck the status line names
- **Third of three**, on top of [`0089`](0089-a-workflow-walk-reports-its-cost.md) and [`0090`](0090-measure-what-you-control.md). This one closes the issue.

## Who this is for

**Ren — [`agent-accelerated-owner`](../personas/agent-accelerated-owner.md)**, at *The changes after* of [`adopt-the-process`](../workflows/adopt-the-process.feature). Ren reads the pull request and the spec layer, not the code. A report row is easy to scroll past; a red check is not. This makes the slowdown impossible to merge unseen without making it impossible to merge.

**Adoption:** one flag and one trigger in the job 0089 wires, and one sentence in the context file. It shortens the same later attempt 0089 does: a slowdown that merged was merged on purpose, with its reason in the pull request.

## The job behind the request

"It's not a hard gate, but basically a soft recommendation. But very important recommendation that users should not miss." A slowdown may be worth it. What must not happen is a slowdown nobody chose.

## Why now

0089 reports a walk past its allowance and passes. The research found that teams which care make the person sign it off — Sentry's *Accept Bundlesize Increase* label, Agent Loops' "raise the budget … in the same pull request and say why in its body" — because a warning that does not stop anything is read by nobody. livespec already holds pull requests to sections in their body: `## Changelog`, `## Ids`.

## The end value

A walk past its allowance cannot merge until the pull request names it under `## Performance`. One line does it, and the report shows that line beside the cost. Within the allowance, nothing is owed and the report still says it.

**How we would know it worked:**
- `tests/test_walkcost.py`: past the allowance with no section fails, naming the walk; with the walk named it passes and the report quotes the line; within the allowance passes with no section.
- Case 96: the job passes the body to the comparison and runs again when the body is edited.

## What changes

1. **[`method/gates.md`](../../method/gates.md), *What a change costs a workflow*, one bullet:** a slowdown past its allowance is not refused, it is answered — the pull request names the walk and says why, and the gate waits for that line rather than for the number to move. The number never decides; the answer is what is required.
2. **`tools/walkcost.py --body FILE`:** reads the body's `## Performance` section. With `--gate`, a walk past its allowance whose workflow the section does not name fails (exit 1), naming the walk and the heading. A named walk's line is quoted beside it in the report.
3. **The rule `a-slower-walk-is-said-not-refused`, reworded in place:** its size never fails the gate; what fails is the missing answer, which this rule holds.
4. **An id**, `gate:workflow-regression-answered`, `since` reading `next`, in [`requirements.md`](../../method/requirements.md#the-ids), the [template ledger](../../templates/bindings.md), `tools/doctor.py`'s registry and the injector's fixture. This repository reads *not applicable*, for 0089's reason.
5. **[`setup`](../../skills/setup/SKILL.md), *Then wire the cost of a walk*:** the job passes the body with `--body` and also runs on the pull request's `edited` event; the context file gains one line saying a walk past its allowance is answered under `## Performance`.

**Rules:**

| Rule id | Feature file | New or changed | Claimed by |
|---|---|---|---|
| `a-regression-past-its-allowance-is-acknowledged` | `features/report/regression-acknowledged.feature` | new | `tests/test_walkcost.py` |
| `the-acknowledgement-is-quoted-beside-the-walk` | same | new | `tests/test_walkcost.py` |
| `setup-wires-the-acknowledgement` | same | new | case 96 |
| `a-slower-walk-is-said-not-refused` | `features/report/workflow-cost.feature` | changed | `tests/test_walkcost.py` |

## What this removes

Nothing.

## What we are not doing

- **Judging the reason.** Any line naming the walk answers it. Whether it is a good reason is the reviewer's, and the report puts it where the reviewer looks.
- **A label instead of a section.** A label carries no reason and is not in the diff of what was said.
- **Answering a count over its budget.** That still fails until the budget moves, and 0089 shows the move beside the change.

## Data

None.

## Risks

- **An agent writes the line itself.** It can, and that is the point: the slowdown and the reason now sit at the top of the pull request, under a heading the reviewer looks for. The gate makes it visible; it does not make it right.
- **A body edit must re-run the job.** Without the `edited` trigger, adding the line does nothing until the next push. `setup` wires the trigger, and case 96 grades it.

## Acceptance checks

1. Samples with the checkout walk 30% slower, allowance 10%, `--gate --body` on a body with no `## Performance`: exit 1, naming checkout. Add `## Performance` with "checkout: accepted, the card form loads its fonts": exit 0, and the line beside the walk.

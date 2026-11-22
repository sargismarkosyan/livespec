# Spec 0089: a workflow walk reports its cost

- **Status:** approved — by the maintainer in advance, 2026-11-22, on the research deck that proposed it ("I like the plan … Approved. Carry on."), with its four recommendations taken as given
- **Issue:** [#187](https://github.com/sargismarkosyan/livespec/issues/187)
- **Sketch:** the research deck, outside the repository — `~/.agent/diagrams/livespec-performance-guardrails.html`. It carries the evidence; this spec carries the decision.
- **First of three.** `0090` adds the layers a walk is measured in and the kit `setup` proposes; `0091` makes a regression past its allowance need a line in the pull request.

## Who this is for

**Ren — [`agent-accelerated-owner`](../personas/agent-accelerated-owner.md).**
Ren reads the spec layer and never the code, and does not read the code an agent writes either. A page that got slower reaches Ren from users, months after the change that caused it. The agents doing the work have no reason to check: in one study of agent pull requests that claimed a speed-up, a third of the merged ones that were re-run delivered nothing or regressed ([Merged, Not Measured](https://arxiv.org/abs/2609.37985)).

**The workflow is [`adopt-the-process`](../workflows/adopt-the-process.feature).**
- The sitting wires the comparison at *Putting it in*, beside the pull-request report.
- It pays back at *The changes after*, on every pull request.
- **It lengthens adoption** by one step in `setup` §4 and one CI job.
- **It shortens the change after a slowdown.** That change starts today with a bisect across every merge since the page was last fast. Afterwards, the slowdown is on the pull request that caused it, named by workflow.

## The job behind the request

To keep each workflow as fast as it was without anybody remembering to check. When something gets slower, Ren wants to see it on the change that caused it, while the person who made the change still has it in mind. Something that changed outside that pull request must not count against it.

**Asked** (the issue, then the maintainer on 2026-11-22):
- the end-to-end tests measure how long each workflow takes, before the change and after;
- a slightly worse result may be fine, but the person must not miss it;
- bundle size and feature load time for a front end; what the package controls, not the other side;
- `setup` suggests the tools to install.

This spec holds the first two. The rest is 0090 and 0091.

## Why now

- **Pull requests say nothing about performance.** `rg -i "perform|latency|benchmark"` across `method/`, `specs/`, `skills/` and `templates/` finds only the context budget.
- **The two pieces this needs are already built.** Every workflow has a walkthrough that the gate requires, and the report already reads base and branch and cannot fail the build.
- **The part that is hard to get right is the same everywhere.** Pairing the samples, the interval, the verdict: every team in the research rebuilt it. #193 settled how livespec ships something like that: one standard-library file that `setup` copies in at a pinned version.

## The end value

Every pull request in an adopting repository says what the change did to the cost of each workflow walk, measured against its own base on the same runner. A walk that got worse leads the report. A difference inside the noise says *no change* and shows no number. A count over the budget the repository chose fails the merge.

**How we would know it worked:**
- `tests/test_walkcost.py`: a branch slower every round reads *worse*, an equal branch reads *no change*, a straddling interval reads *inconclusive*, 43 requests against a budget of 42 fails, a budget on a time is refused.
- In a consuming web repository, a pull request that adds a request to one page moves that workflow and lists the rest once as *no change*.

## What changes

1. **[`method/gates.md`](../../method/gates.md), a section *What a change costs a workflow*, after *The report is not a gate*.** Portable: it names no tool, metric or number.
   - Every change reports what it did to the cost of each workflow walk, base against branch.
   - **Both sides on one runner, in one job, in turns,** so whatever slows the runner slows both, and whatever changed outside the pull request is on both sides.
   - **Three verdicts:** no change, worse, inconclusive. Inconclusive is said with its reason, and never passes for *no change*.
   - **Two numbers per measure, decided before the change runs:** the noise below which a difference is not read, and the allowance a real slowdown may use before it is called past it.
   - **A time never fails the build.** It is the chance [`testing.md`](../../method/testing.md#a-test-that-fails-sometimes-is-worse-than-no-test) rules out of a verdict. **A count may carry a budget that does**, because it comes out the same on every run of the same tree.
   - **The numbers live in one versioned file**, and a change to them is shown beside the change it allows, because raising the bar is the easiest way to pass it.
   - **One run counts.** Rounds repeat inside the job; the job is not re-run until it is green.

2. **`tools/walkcost.py`**, standard library only.
   - Reads the samples the walks wrote — one JSON object a line: `workflow`, `measure`, `side` (`base` or `branch`), `value` — and the policy file, from the branch and, if given, from the base.
   - **A count** compares the medians of the two sides. **A time** takes the median of the pairwise log ratios (the Hodges–Lehmann estimate) and its 95% interval from the Mann–Whitney rank statistic, normal approximation. No randomness: the same samples give the same report.
   - Writes the report in Markdown. Exits 0, unless `--gate` is given and a count is over its budget (1), or the policy is refused (2).
   - `setup` copies it into the consuming repository, its version on its first line.

3. **Two ids in [`method/requirements.md`](../../method/requirements.md#the-ids)**, `since` reading `next`:
   - `wiring:workflow-cost` — the cost of every walk on the report; *unobserved* until somebody has watched it report a move.
   - `gate:workflow-budget` — a count past the budget the policy sets fails.
   - Each also added to the [template ledger](../../templates/bindings.md), and to `tools/doctor.py`'s registry with a row check for the wiring row, the way the report's row is checked.

4. **[`setup`](../../skills/setup/SKILL.md) §4, a step *Then wire the cost of a walk*, after the report.** It copies the comparison in, writes the policy file with the noise and allowance it recommends and no budget until a count is chosen, and wires a job that walks the base and the branch in turns with the walkthroughs the repository already runs. A repository whose walks cannot be repeated on every change records why.

5. **This repository's [bindings](../setup/README.md).** Both rows read *not applicable*: a workflow walk here is a graded case that bills the maintainer's account, and only the maintainer may approve that.

**Rules added:**

| Rule id | Feature file | Claimed by |
|---|---|---|
| `setup-wires-the-cost-of-a-walk` | `features/report/workflow-cost.feature` | eval case 96 |
| `the-cost-is-the-branch-against-its-base` | same | `tests/test_walkcost.py` |
| `an-unclear-cost-is-inconclusive` | same | `tests/test_walkcost.py` |
| `a-slower-walk-is-said-not-refused` | same | `tests/test_walkcost.py` |
| `a-budget-gates-only-a-count` | same | `tests/test_walkcost.py` |
| `a-changed-budget-is-shown-beside-the-change` | same | `tests/test_walkcost.py` |

## What this removes

Nothing. It adds a measurement nobody takes today, and builds on `the-report-cannot-fail-the-build` rather than restating it.

## What we are not doing

- **Gating on time, even with a wide threshold.** A wide one catches only what nobody needed a gate to see, and a narrow one is flaky.
- **A `@critical` tag or a subset of workflows.** Every walked workflow is weighed.
- **History and nightly trend tracking.** Comparing against stored history raises false alarms on shared runners; a nightly run needs a quiet machine. Out of scope, decided 2026-11-22.
- **Measuring journeys.** No test walks one.
- **A harness that drives the walks.** The walk is the repository's, in its own language; the comparison only reads what it wrote.

## Data

There is no storage contract here. In a repository set up before this, the two ledger rows are missing and `doctor` reports them, the way every new gate has arrived.

## Risks

- **CI time doubles for the walks.** Every walk runs on both sides, repeated. The policy names the rounds; `setup` says the cost before wiring it.
- **A copied script goes stale.** Its first line names the version; replacing it is the upgrade. Auditing that copy is #188's and #193's.
- **A count that varies between rounds is not a count.** The comparison says so and reads it inconclusive rather than gating on it.

## Acceptance checks

1. `python3 tools/walkcost.py --samples s.jsonl --policy p.json` on samples where the branch is 30% slower every round prints the walk as *worse* and exits 0; with `--gate` and 43 requests against 42, it exits 1, naming all four.
2. Give a time measure a `budget` in the policy: it exits 2 before comparing.
3. In a consuming repository after `setup`, open a pull request that adds a request to one page and read the report it posts.

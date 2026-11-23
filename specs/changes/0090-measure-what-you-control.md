# Spec 0090: measure what you control

- **Status:** approved — by the maintainer in advance, 2026-11-22, on the research deck that proposed it ("I like the plan … Approved. Carry on.")
- **Issue:** [#187](https://github.com/sargismarkosyan/livespec/issues/187)
- **Sketch:** not drawn — approval given in advance, on the research deck the status line names
- **Second of three**, on top of [`0089`](0089-a-workflow-walk-reports-its-cost.md). `0091` makes a regression past its allowance need a line in the pull request.

## Who this is for

**Ren — [`agent-accelerated-owner`](../personas/agent-accelerated-owner.md)**, in the same place as 0089: the sitting wires it at *Putting it in*, and it pays back at *The changes after*, on [`adopt-the-process`](../workflows/adopt-the-process.feature).

**It lengthens adoption** by one question — which layers, and which tools — and, where nothing in the repository can measure a layer, one install the person agreed to. **It shortens the change after a slowdown** further than 0089 alone: the report says which side moved, so the person does not start by working out whether the front end or the service got slower.

## The job behind the request

To see what *this* package's change did, with the parts it does not control held still, and to see the whole walk as well.

**Asked** (the maintainer, 2026-11-22): "you can ignore the delay from API if it's a front-end package. Or you can ignore the delay from UI if it's a back-end package. So you will focus on the things that you control. Of course, you want to measure the overall change if it's the end-to-end flow." And: "we need to control the bundle size if it's a front-end package … the overall page load effect and exact features loading time." And: when livespec is installed, "suggest him to install all the necessary tools".

## Why now

0089 compares base and branch, but a walk measured whole mixes the front end, the service and the network into one number. A front-end change that made the page heavier and a service change that made a query slower look the same, and a slow staging service moves a front-end pull request's number for nothing it did.

## The end value

The report shows each walk per layer: the front end measured against replayed answers, the back end without a browser, the whole walk end to end. A front end is weighed in bytes shipped, page load and the time each workflow's feature is ready. `setup` proposes the tools that do it and installs only what the person agrees to.

**How we would know it worked:**
- `tests/test_walkcost.py`: the same measure from two layers is two lines, each naming its layer.
- Case 96: in `printshop`, the sitting names three layers, replays the server's answers for the front end, proposes a tool to weigh the bundle, and waits for a yes before installing it.

## What changes

1. **[`method/gates.md`](../../method/gates.md), *What a change costs a workflow*, one bullet:** each walk is measured where the change can move it — the front end with the service's answers replayed at a fixed delay, the back end without the interface, and the whole walk once, end to end. A front end is weighed in what it ships, how long its pages take, and when each workflow's feature is ready.
2. **`tools/walkcost.py`:** a sample may carry `layer`. The report's *Walk* column reads `checkout · front end`, and one measure in two layers is two lines.
3. **[`setup`](../../skills/setup/SKILL.md), *Then wire the cost of a walk*:** a step choosing the layers and their measures, with a short table of what to propose per layer: replayed answers in the walkthrough's own runner (Playwright's HAR replay, or the runner's equivalent); a bundle weigher such as size-limit; page and feature times read from the runner and from a `performance.mark` the app sets; the service timed without the browser by a load tool such as k6 or the language's benchmark library, and queries counted. What the repository already runs comes first; an install is proposed with what it adds and made only on a yes.
4. **[`adopt-the-process`](../workflows/adopt-the-process.feature), *Done well*:** one sentence — a tool a walk needs to measure its cost is proposed and installed only once the person agrees; the gates themselves still add nothing. The example *the gates arrive in the language already in the repository* is unchanged: the comparison is standard library, and the tool belongs to the walk, not the gate. Confirmed with the maintainer on the deck, slide 28, before this spec.

**Rules added:**

| Rule id | Feature file | Claimed by |
|---|---|---|
| `each-layer-holds-the-other-side-fixed` | `features/report/walk-layers.feature` | case 96 |
| `the-report-names-the-layer` | same | `tests/test_walkcost.py` |
| `a-front-end-is-weighed-in-bytes-load-and-features` | same | case 96 |
| `setup-proposes-a-kit-for-the-stack` | same | case 96 |

## What this removes

Nothing.

## What we are not doing

- **A layer tag on the workflow.** The layers belong to the package, so they are in the bindings, not on every workflow.
- **Shipping a harness or a tool.** The table in `setup` names candidates; the repository owns what it installs.
- **Production monitoring.** It finds a slowdown after merge.

## Data

None. A sample without `layer` reads as before.

## Risks

- **A replay that drifts from the real service** makes the front-end layer measure a service nobody runs. The replay is recorded by the walkthrough's runner and re-recorded when the service's answers change; the end-to-end layer still sees the real thing.
- **More walks, more CI minutes.** Three layers can triple the job. The sitting says the cost and the person chooses the layers.

## Acceptance checks

1. Feed the comparison front-end and end-to-end samples of one measure: two lines, each naming its layer.
2. Run `setup` against a web repository with Playwright walkthroughs and no bundle check: it proposes a bundle weigher, says what it adds, and installs nothing before a yes.

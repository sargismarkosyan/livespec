# Spec 0017: the practices travel, the commands stay

- **Status:** proposed
- **Issue:** [#42](https://github.com/sargismarkosyan/livespec/issues/42)

## Who this is for

[`@persona:agent-accelerated-owner`](../personas/agent-accelerated-owner.md), in
[`adopt-the-process`](../workflows/adopt-the-process.feature) — at one specific
moment: section 2's fifth answer, where the repository turns out to be one whose
product is *judgment* rather than code and there is no function to call.

It also serves **`context-budget`**
([spec.md](../spec.md#the-promises-that-belong-to-no-single-workflow)) — but by
subtraction rather than by restraint, which is the unusual part. Everything this
adds is on-demand `method/` payload, read only by a sitting that took the graded
branch. Nothing is added to a skill body, so the always-on cost of this change is
**zero**, and so is its effect on every session that never touches a graded
suite.

## The job behind the request

To stop each repository whose product is prose paying, one afternoon at a time,
for lessons this one has already survived.

Not to document livespec's runner. The distinction the request itself draws:

> although some of the best practices can be reused by setup skill and we can
> have some files sharing those which can be referenced by setup based of the
> kind of repo where its actually implementing the setup

*Best practices* travel. *The runner* does not.

## Why now

**Because the knowledge exists and is trapped in the wrong layer.** Specs
[`0012`](0012-a-runner-that-runs.md) and [`0013`](0013-the-board-of-latest-measurements.md)
accumulated real graded-suite practice, and every word of it landed in files that
are true only of this repository — `evals/README.md`, the bindings, runner
docstrings. That is correct for the commands and a loss for the judgment.

**Because the cost of re-learning is measured, not hypothetical.** This
repository hit hermetic-session failure three ways in one afternoon: a session
inheriting the operator's settings, one inheriting MCP servers, one inheriting
the enclosing repository's context. Each was diagnosed as a bug in the plugin
before it was diagnosed as a bug in the harness. A consuming repository has no
reason to be faster at that than this one was.

**Because `method/` is already the shared layer and already forks here.**
[`testing.md`](../../method/testing.md#first-what-proves-a-rule-is-true-here)
sets out the two honest answers and warns that graded cases prove a weaker thing.
What it does not do is say how to run them without measuring the wrong thing.
The fork exists; only one of its branches has been written down.

## The end value

A repository adopting the process for a prose product gets the five expensive
lessons before it pays for them, and gets them without inheriting a runner it
cannot use.

**How we would know it worked:** its first graded run measures the plugin rather
than the operator's machine, and its bindings record hermetic sessions, the
two-arm ablation and the freshness rule as decisions taken rather than as
questions still open. Today none of that is written anywhere it could reach.

## What changes

- A new `method/graded-cases.md` — the graded branch of `testing.md`'s fork,
  grown from four paragraphs into the page it needs to be. **Written
  command-free**, to the method's own test: it must survive a repository whose
  runner is not promptfoo and whose sessions are not `claude -p`. It carries:
  - **hermetic sessions** — a session inheriting the operator's settings, MCP
    servers or the enclosing repository's context measures the operator's
    machine, and reads as a plugin defect while being an environment one;
  - **the two-arm ablation** as the only honest score for context that loads
    everywhere, since a single arm cannot separate what the instructions did
    from what the model already did — and **firing is reported, never scored**,
    so it can never inflate the difference;
  - **a judge forced into a schema**, and never the model under test;
  - **freshness over the score** — a measurement carries a fingerprint of what it
    measured, re-running covers exactly what moved, and **the bookkeeping is
    gated while the number never is**;
  - **a run's evidence is local, its summary durable** — transcripts stay where
    they fell, one line per case outlives them.
- `method/testing.md` — the graded paragraph of the fork gains the onward link.
- `method/README.md` — the index gains its row.

**Rules added or changed:** none, deliberately. See below.

## What we are not doing

- **Not touching `skills/setup/SKILL.md`, and this is the load-bearing
  omission.** The payload-link gate accepts a reference from *"a skill, method
  doc, or README"*, and section 2's fifth answer already links to `testing.md`'s
  fork — so the reference follows the answer with no edit, exactly as
  [#42](https://github.com/sargismarkosyan/livespec/issues/42) asked, in two hops
  rather than one. Two things fall out of that, both good: the body stays at 386
  lines, and **no eval case is staled, so this change costs nothing to
  re-measure.** [`0015`](0015-the-sitting-uses-the-pipeline.md) added 27 lines to
  that body and measured three `setup` cases moving down; a change whose whole
  argument is *put the weight where it is only read when needed* should not open
  by adding weight to the hottest file in the plugin.
- **No rules, and no case.** This ships prose that an agent reads on a branch it
  reaches once per repository. A rule asserting *the sitting applies these* would
  need `setup` to do something new to be gradeable — which is the paragraph
  above, inverted — and a case walking a graded-product sitting costs money on
  every run to assert that a document was read. The honest position is that this
  ships **unheld**, that `method/` prose has never been held here, and that the
  thing which would hold it is a change to `setup` that today's numbers argue
  against making.
- **Not shipping the runner, the board, or `caselib.py` as payload.** Practices
  travel; commands and scripts do not. [`0013`](0013-the-board-of-latest-measurements.md)
  drew the same line about the board itself, and #5's original complaint was this
  trap from the other direction.
- **Not writing the sixth practice we do not have yet.** Calibration — what a
  delta *means* — is unsettled here, `evals/README.md` says so in writing, and a
  page that shipped it as guidance would be exporting a guess.

## Data

No storage contract applies. What a version leaves behind here is the pull
request description ([spec.md](../spec.md#what-a-version-leaves-behind)), and
this change adds one file to the shared layer without touching `version`,
`CHANGELOG.md`, or any repository's stored state.

## Risks

**The promise most at risk is `context-budget`, and it is the one this change
pays into rather than draws from.** Nothing here is always-on. The risk that
remains is the ordinary one for `method/`: a page nobody reaches is a page that
ships to every user unread, and the two-hop path is one hop longer than the
issue imagined. The payload-link gate proves the file is *referenced*; it cannot
prove it is *reached*. If a later sitting is observed taking the graded branch
and never opening the page, the answer is a line in `setup` — paid for then,
with a measurement, rather than assumed now.

**Two copies of a method disagreeing** is the failure this repository exists to
stop, and this change creates a second place where graded-suite practice is
written down. The mitigation is the command-free rule: `evals/README.md` keeps
every command, threshold and file name, and `method/graded-cases.md` keeps no
number and no path. Where a sentence could live in either, it belongs in the
bindings — a page that starts naming `promptfoo` or `board.json` has already
begun to be a second copy.

**Shipping unheld is a real cost, not a technicality.** Nothing will fail if this
page rots. That is true of every file in `method/` today and is not made worse
here, but it is the reason this change is small: the less it claims, the less
there is to go quietly stale.

## Acceptance checks

1. `method/graded-cases.md` exists and contains no command, no threshold, no
   file name and no tool name — the same test `method/README.md` sets for every
   page beside it.
2. All five practices are present and each is stated as a decision with its
   reason, not as a description of what this repository happens to do.
3. `method/testing.md`'s graded branch links to it, and `method/README.md` lists
   it.
4. `python3 .github/scripts/verify.py` is green, including the payload-link
   check, with **no eval case newly stale** — the board reads the same before and
   after.
5. Read the page against a repository whose runner is not promptfoo. Nothing in
   it needs rewriting for that repository to use it.

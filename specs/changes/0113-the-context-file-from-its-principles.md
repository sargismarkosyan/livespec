# Spec 0113: the context file from its principles

- **Status:** approved — by the maintainer in advance, 2026-11-22 (*"Carry on."*, then *"yes"* to continuing page by page), as the next change under #195; implemented end to end, reviewed at the pull request
- **Issue:** [#195](https://github.com/sargismarkosyan/livespec/issues/195), the fifth change under it, after [0112](0112-graded-cases-from-their-principles.md)
- **Sketch:** skipped — approval was given in advance, so there was no decision left for one to support.

## Who this is for

**Ren — [`agent-accelerated-owner`](../personas/agent-accelerated-owner.md)**, whose
context file every session reads first. **The workflow is
[`adopt-the-process`](../workflows/adopt-the-process.feature)**, at *Putting it in*,
where the sitting writes that file. Nothing about who this is for moves.

## The job behind the request

The same as [0109](0109-the-process-from-its-principles.md), for
`method/claude-md.md` — the page that tells a repository its context file must
be short, and was 202 lines itself.

## Why now

It is the page that sets the reader's two-hundred-line limit, and the next
method page under #195.

## The end value

The same requirements in fewer words. **How we would know it worked:** the
harvest accounts for every section; the three linked anchors resolve; the ten
numbered requirements under *What must be there* are still what
`check:loop-per-claude-md` counts; and the page is shorter.

## What changes

1. **[`method/claude-md.md`](../../method/claude-md.md)** is rewritten from the
   principles, 202 → 148 lines.
   - *Length*, *Which file* and *When it is out of line* keep their anchors.
   - *What must be there* keeps its heading and its ten `**N.` items, which
     `tools/doctor.py` counts.
2. **The `method/` ceiling** is lowered to the size this change leaves.

No rule, workflow or skill moves. No Gherkin moves.

### The harvest

| Section | Kept, every one |
|---|---|
| Introduction | requirements, not a file to copy, and why no template; written for an agent arriving mid-task |
| *What must be there* | all ten requirements, with: the purpose vs the product; the approval step names what is held; the pull-request step reads back what it closes; the rules list and its eight rules; four or five command lines; an annotated layout |
| *What must stay out* | the plugin's words; reasoning, to `constraints.md`, with one line kept; what tooling enforces; history that binds nothing, and history that does; anything aspirational |
| *Which file* | the first file the harnesses read; the bindings name it; one file, never two; Pi reads `AGENTS.md` first, so a `CLAUDE.md` beside it is unread; the audit and the sitting |
| *Where it goes* | the root; `.claude/CLAUDE.md` not read by Pi; a plugin-root repository's validate warning; written for the agent, and why prose |
| *Length* | the repository's ceiling and how it is set and raised; a pointer turned copy; never above two hundred, and why it is the method's one number; above it fails first; the three costs; the five consequences; the one-file test |
| *Keeping it true* | stale is worse than none; corrected in the change that made it wrong; no reference file |
| *When it is out of line* | a stale path vs a rewrite; harvest first; show it whole and wait; the sitting rewrites, the audit corrects a line |

## What this removes

- **"Human approves on its own is that step as it read before there was anything
  to hold…"** — the history of the approval step. The requirement stays.
- **"A check only the method mentions is a check the step that needs it never
  runs"**, and *"Without this, process improvements get committed to the wrong
  repository and the two copies drift"* — the reasons. The requirements stay.
- **"One repository in a hundred will hit a tool that objects"** framing, and
  the attention-span vs context-cost aside.
- **54 lines of `method/claude-md.md`.**

## What we are not doing

The other method files: one change each, under #195. No requirement changes.

## Data

None.

## Risks

A requirement loses force without its reason; the reasons cut are listed above.
The audit's count of requirements is unchanged at ten.

## Acceptance checks

1. Every row of the harvest can be found in the new page.
2. `check:loop-per-claude-md` still asks after all 10 items; `verify.py` is
   green.
3. The `method/` ceiling is lowered to match.

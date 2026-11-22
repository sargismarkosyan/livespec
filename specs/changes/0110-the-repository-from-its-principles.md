# Spec 0110: the repository from its principles

- **Status:** approved — by the maintainer in advance, 2026-11-22 (*"Carry on."*), as the next change under #195; implemented end to end, reviewed at the pull request
- **Issue:** [#195](https://github.com/sargismarkosyan/livespec/issues/195), the second change under it, after [0109](0109-the-process-from-its-principles.md)
- **Sketch:** skipped — approval was given in advance, so there was no decision left for one to support.

## Who this is for

**Ren — [`agent-accelerated-owner`](../personas/agent-accelerated-owner.md)**, whose
agent reads `repository.md` every time it branches, opens a pull request, claims
an issue or closes one. Nothing about who this is for moves.

**The workflow is [`adopt-the-process`](../workflows/adopt-the-process.feature)**, at
*The changes after*, step 8 of [`trusting-the-spec-again`](../journeys/trusting-the-spec-again.md).

## The job behind the request

The same as [0109](0109-the-process-from-its-principles.md), for the method's
largest page: say each rule once, under the principle it follows from, so the
agent reading it follows all of it.

## Why now

`repository.md` is 567 lines, the largest page in `method/`. Most of its length
is the reasoning restated around each rule — why a reader should care, what went
wrong once — in prose a rule can stand without.

## The end value

Every rule, table, command example and decision the page held is still there;
the reasoning that repeated them is gone, and each section names its principle.

**How we would know it worked:** the harvest below accounts for every section,
the seven linked anchors resolve, and the page is shorter.

## What changes

1. **[`method/repository.md`](../../method/repository.md)** is rewritten from the
   principles, 567 → 408 lines. The seven headings other files link to keep
   their anchors: *Branches and pull requests*, *Several changes at once*, *Every
   pull request shows what it did*, *And the run it rests on*, *And the point,
   before the evidence*, *Closing an issue*, *Closing an issue by hand*.
2. **The `method/` ceiling** in the bindings is lowered to the size this change
   leaves.

No rule, workflow or skill moves. No Gherkin moves.

### The harvest

| Section | Kept, every one |
|---|---|
| *Layout* | the tree; bindings are where the method stops; screenshots are the deliverable, feedback shrinks |
| *Branches and pull requests* | the branch flow; the seven-row protection table; check matched by job `name:`; zero approvals for one author; merge queue or platform update, read back, *unobserved* until watched, Strict never dropped; a stack lands on `main` and merged ≠ on `main`; protection read back, its command a binding |
| *Several changes at once* | one directory and one command; readied by the command; three kinds of resource, harness state included; one env file and its handling; values worked out from the tree; cleaning by the record and what it keeps; a throwaway tree watched; the claim, its comment, read before writing, never released by age, how it ends, an unread claim; numbering past everything in flight, gaps stay, renumber the unmerged, migrations; nothing caps trees |
| *Every pull request shows what it did* | the picture in the body, one per version, named for the spec; form follows what changed; composed for the requester; recorded on the branch by `record-clip`; the pinned raw URL and why; nothing to see is a line |
| *And the Gherkin it moved* | the promise quoted or pinned; conditional on spec surface |
| *And the run it rests on* | the command and its output, boundary read-back, never a summary; the report beside it gating nothing; owed only when the tests move; both blocks gate-checked for being there |
| *And the point, before the evidence* | two readers; the template wins, and the order without one; a checkbox is a claim; the problem before the change; the eight things that go in; ask, check against the diff, cut; the five *throughout* rules; the review message; no gate, and the word count |
| *Commits* | the format; spec commits first; tooling commits unnumbered; never commit red |
| *Issues*, *Which repository* | the bindings' tracker; no issue directory; the working repository; the plugin's checkout never a target; say where before filing; plugin reports go to the plugin; ask once when unclear; the label table |
| *Closing an issue*, *by hand* | the keyword in the description and why; straight before a bare reference or full URL; the two forms that close nothing; code spans; read back what will close, a binding; the two hand-closing cases and their comment; take the screenshot out; sweep the siblings |
| *Screenshots* | the two folders and their lifetimes; images reach disk only as a file path |

## What this removes

The reasons restated around rules that stand without them:

- the cost illustration *five green changes merged by hand cost ten rebases*;
- *a directory per person per week…*, *somebody who changes harness…*, *a deleted
  directory leaves the record claiming a tree that is gone*, *the rule is written
  as what it keeps*, *a readiness nobody watched is the same claim as a gate
  nobody broke*;
- the paragraph arguing the Gherkin and run blocks *should* be gated, and the
  two *ceremony is what gets skipped* paragraphs — the conditions stay;
- *every other mistake in this method announces itself; this one is silent on
  both sides*, and *half-open issues rot* — the rules they justified stay;
- 159 lines of `method/repository.md`.

## What we are not doing

- **The other method files.** One change each, under #195.
- **Changing any rule.** How they are said, not what they say.

## Data

None.

## Risks

- **A rule loses force without its reason.** The reasons cut are listed above, so
  a reviewer can put one back where it was load-bearing. The eval cases holding
  the skills that cite this page are unchanged.

## Acceptance checks

1. Every row of the harvest can be found in the new page.
2. The seven linked anchors resolve; `verify.py` is green.
3. `method/` is under its old ceiling, and the ceiling is lowered to match.

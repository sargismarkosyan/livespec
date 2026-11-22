# Spec 0115: install outside the method

- **Status:** approved — by the maintainer in advance, 2026-11-22 (*"Up to you. Carry on."*), as the next change under #195; implemented end to end, reviewed at the pull request
- **Issue:** [#195](https://github.com/sargismarkosyan/livespec/issues/195), the sixth change under it, after [0113](0113-the-context-file-from-its-principles.md)
- **Sketch:** skipped — approval was given in advance, so there was no decision left for one to support.

## Who this is for

**Ren — [`agent-accelerated-owner`](../personas/agent-accelerated-owner.md)**, who
installs livespec once and whose agent reads the method on every change.
**The workflow is [`adopt-the-process`](../workflows/adopt-the-process.feature)**,
at *Putting it in*. Nothing about who this is for moves.

## The job behind the request

To keep the method portable. `method/README.md` says *"Nothing here names a
command, a filename or a language"*, and then spends 140 lines on install
commands for two hosts.

## Why now

It is the last prose in `method/` under #195 apart from `gates.md`, which waits
for [#194](https://github.com/sargismarkosyan/livespec/issues/194). Rewriting it
in place would not help: a command does not belong in the method, however it is
worded.

## The end value

`method/` holds the method and nothing else. The install guide lives where
installing starts: the root README, which already carries the two install
commands and pointed to `method/README.md` for the rest.

**How we would know it worked:**
- `method/README.md` names no install command.
- Every link into the old anchors resolves at the new place.
- The root README's guide is still scanned by `tests/test_hosts.py` for wording
  only one host can follow.

## What changes

1. **The install guide moves** from `method/README.md` to a new *Installing*
   section of the root [`README.md`](../../README.md). It moves whole:
   - *Adding the marketplace and the plugin*
   - *Wire it into the repository instead of the machine*
   - *Updating*
   - *Working on the method itself*
   - *Under Pi*

   Relative links are fixed for the new location. The guide's own copy of the
   two Claude Code commands is replaced by a pointer to the same block at the
   top of the page.
2. **`method/README.md`** keeps its table, the six principles and the paragraph
   on what the method does not name, and ends with one line pointing to the
   install guide. It goes from 178 to 45 lines.
3. **The three links into the old anchors** point at the root README: two in
   `skills/setup/SKILL.md`, one in the bindings.
4. **The `method/` ceiling** is lowered to the size this change leaves.

No rule, workflow or Gherkin moves.

## What this removes

- **The install guide from `method/`**, 133 lines. The guide itself is not cut;
  the root README grows by 129.
- **Its duplicate of the two Claude Code install commands**, already at the top
  of the root README.

## What we are not doing

- **Rewriting the guide's wording.** It moves as it is, so the move is easy to
  review. Shortening it is a later, separate change.
- **`gates.md`**, which waits for #194.

## Data

None.

## Risks

- **A consuming repository's agent reaches the guide** through `setup`'s links,
  which now resolve to the plugin root's README. The plugin ships its whole
  repository under both hosts, so the file is there.

## Acceptance checks

1. `method/README.md` is 45 lines and names no install command.
2. `setup`'s two links and the bindings' one resolve; `verify.py` is green.
3. The `method/` ceiling is lowered to match.

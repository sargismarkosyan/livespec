# Spec 0092: the plugin held to itself

- **Status:** approved in advance, by the maintainer, 2026-11-22 ("I like it. Please implement")
- **Issue:** none, a direct request. It fixes this repository's own part of [#211](https://github.com/sargismarkosyan/livespec/issues/211), [#213](https://github.com/sargismarkosyan/livespec/issues/213) and [#215](https://github.com/sargismarkosyan/livespec/issues/215); their skill-side parts stay open.
- **Sketch:** skipped, because approval was given in advance. The session decided that is a legitimate reason; [#210](https://github.com/sargismarkosyan/livespec/issues/210) writes it into the method.

## Who this is for

**Nobody the product is for**, and this spec says so instead of filing it under a workflow. It is the documented case in [`process.md`](../../method/process.md#a-technical-change-that-serves-no-workflow-is-correct-not-a-gap): it changes how *this* repository is held to its own plugin, and nothing a person using livespec elsewhere can see.

What [`agent-accelerated-owner`](../personas/agent-accelerated-owner.md) gets from it arrives later. Every skill change made here is made by a session that runs this checkout's own skills, under either host, so a skill that misreads its own instructions shows up here first.

## The job behind the request

To treat livespec as a consumer of livespec and have that be true, not mostly true. The self-audit of 1.32.1 ([#205](https://github.com/sargismarkosyan/livespec/pull/205)) passed 47 of 49 checks. The review after it found three things in this repository that no check reads.

## Why now

- **Pi never loads livespec's own skills here.** There is no `.pi/settings.json`. The session that found this ran `refine-spec` and `doctor` by reading their files, because neither was loaded. Claude Code has [`.claude/settings.json`](../../.claude/settings.json); Pi only gets a hand-typed `pi -e` per session.
- **The coverage row says something the tree contradicts.** `gate:coverage` reads *not applicable: there is no application code to measure*, and *What has no gate* says "eight markdown files". [`tools/`](../../tools/) is about 1,470 lines of Python shipped to every user, with rule-bound tests in `tests/`.
- **`CLAUDE.md`'s rules list leaves out *spec before code*,** the rule [#203](https://github.com/sargismarkosyan/livespec/pull/203) broke here. [`claude-md.md`](../../method/claude-md.md#what-must-be-there), item 7, names it.

## The end value

A Pi session opened in any tree of this repository loads that tree's own livespec skills. The bindings say truthfully what coverage there is and why. The rule this repository broke is in the file every session reads first.

**How we would know it worked:** `pi list` in a tree shows the project package resolving to that tree, and `/skill:doctor` exists in a Pi session there. `check:na-vs-tree` has nothing to contradict, and a reader of the coverage row learns that `tools/` exists. `CLAUDE.md` names *spec before code*.

## What changes

1. **[`.pi/settings.json`](../../.pi/settings.json)**, committed: `{"packages": [".."]}`.
   - Pi resolves a relative local path from the settings file, so it names the root of the tree it sits in. Every worktree loads its own checkout, which is what a skill edit needs.
   - Pi reads it only once the folder is trusted.
   - **[`.gitignore`](../../.gitignore)** ignores `.pi/*` except `settings.json`, because Pi tools write machine-local state there (`.pi/artifacts/`, `.pi/tasks/`).
2. **The bindings say where the plugin is enabled**, in a new key-table row, **Where the plugin is enabled**:
   - Claude Code: `.claude/settings.json` enables `livespec@livespec`, and the marketplace stays machine-local (the committed file must not repoint it, per [`method/README.md`](../../method/README.md#working-on-the-method-itself));
   - Pi: `.pi/settings.json` loads this checkout.
3. **The coverage row is honest.** `gate:coverage` becomes ***not applicable, decided***:
   - `tools/` is shipped Python with rule-bound tests, but no coverage is measured;
   - a coverage tool is a dependency the gates do not take, and a measure built on the standard library's `trace` is left for its own change;
   - what this leaves uncovered: the lines of `tools/` and `.github/scripts/` no test reaches.

   *What has no gate* and *The substitution* stop saying there is no code. `wiring:rule-bound-measure` keeps *not applicable* and points at the same reason.
4. **`CLAUDE.md` gains *spec before code***, without growing past its ceiling of 128 lines:

   > No change merges without an approved change spec; a fix found on the way is filed, not made.

   An existing rule is tightened to make room.

**Rules added or changed:** none. These are corrections to this repository's own record and configuration.

## What we are not doing

- **The skill-side fixes**: the host check and setup's self-hosting paragraph ([#211](https://github.com/sargismarkosyan/livespec/issues/211)), a judgment line for reasons `na-vs-tree` cannot parse ([#213](https://github.com/sargismarkosyan/livespec/issues/213)), and re-reading the whole context file ([#215](https://github.com/sargismarkosyan/livespec/issues/215)). Each is its own spec.
- **A coverage measure.** Decided *not applicable* in session; a stdlib `trace` measure would be its own change.
- **The light path for CI fixes, and the written sketch exemption**: [#210](https://github.com/sargismarkosyan/livespec/issues/210).
- **The three unwritten workflows and the unnamed journey phases** (*Three more attempts, not written yet*). Putting them on the clock is the shape [#213](https://github.com/sargismarkosyan/livespec/issues/213) defines; doing it before that is defined would be redone.
- **Aligning the bindings' key table with the template**: waits for [#214](https://github.com/sargismarkosyan/livespec/issues/214)'s graded-case template.
- **A committed Claude Code marketplace pointing at this checkout.** [`method/README.md`](../../method/README.md#working-on-the-method-itself) forbids it, because it repoints the name machine-wide.

## Data

No storage contract moves.

## Risks

- **A trusted folder now loads code from this checkout under Pi.** Skills only, since the repository ships no Pi extension today. A future extension would run from the checkout too, which is what working on it requires.
- **A machine that also has livespec installed personally** gets two packages with the same skills. Pi identifies local packages by path and git packages by URL, so both load, and it keeps the first skill of each name, warning at startup ([`method/README.md`](../../method/README.md#under-pi)). In a project, the project package is the one working on the method needs. The hand-back says to check which one won.

## Acceptance checks

1. `pi list` in a tree shows `Project packages: ..` resolving to that tree's root.
2. Open Pi in a trusted tree: `/skill:doctor` and `/skill:refine-spec` exist, and the startup warning, if any, names this checkout as the winner.
3. `python3 .github/scripts/verify.py` is green, and `wc -l CLAUDE.md` is at most 128.
4. `python3 tools/doctor.py specs/setup/README.md` reads `check:na-vs-tree` clear, and the coverage row reads *not applicable, decided*.

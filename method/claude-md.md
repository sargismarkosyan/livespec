# What the context file has to contain

*From: one copy of anything.* The context file is the first thing an agent reads
in a repository, in front of every request, so everything in it is load-bearing
or noise. **This is a list of requirements, not a file to copy**: there is no
template, because a file assembled from somebody else's blanks reads like one.
Write it for **an agent arriving mid-task with no context** that will act on what
it says.

## What must be there

**1. What this is, in two or three sentences** — what the product is, what the
repository is *for* (often different), and what a version delivers. If the app
is a means to something else, say so, or the agent optimises the wrong thing.

**2. Who writes what.** If the agent writes the code and a person only uses and
approves, say so; it changes how everything else is read.

**3. That the process is a plugin, with a link, and that reading it is not
optional.** The rules, the loop, the gate semantics and the templates live
there and are never copied here.

**4. The line between the plugin and the repository**, in one testable
sentence: a sentence that survives a repository with pytest and a Makefile
belongs in the plugin; one naming a command, a filename, a threshold or a
language belongs in `specs/setup/`.

**5. A table of pointers** — the bindings, the constraints, the persona, workflow
and journey layers, and how the spec layers fit — one line each on what a reader
goes there *for*. It is a map, not a summary, and most of the file's value.

**6. The loop, numbered** — eight steps at most, one line each, here rather than
a link away. **The approval step says what the person is holding**: the spec and
the sketch drawn from it. **The step that opens the pull request links the
description rules the bindings name, and reads back what it will close**, with
the bindings' command, and fixes a closing line the platform did not register
before handing it back ([repository.md](repository.md#closing-an-issue)).

**7. The rules most often broken here — a subset, linking the full set.** Spec
before code; one change per version; feedback never fixed on the spot; never
touch `src/` from a skill; rule ids are permanent; every commit green; a
rule-bound test runs in the world its boundary row names; less is the default —
the smallest change, with what it made dead deleted in it. A rules list nobody
finishes reading enforces nothing.

**8. The commands** — verification first, then what a session needs to run the
thing; four or five lines in one block.

**9. The layout, annotated** — a line per directory saying what belongs there,
not `ls` output.

**10. Where it lives** — the live URL if there is one, and where issues go.

## What must stay out

- **Anything the plugin already says.** A rule stated twice is edited once.
- **The reasoning behind a decision** — that goes in `specs/setup/constraints.md`,
  where it can be argued with. The rule stays here, with one line saying why it
  is not aspirational.
- **What tooling already enforces** — style guides, formatting, commit-message
  templates. If a linter can say it, the linter says it.
- **History that binds nothing.** A dated account of what this file used to
  claim, and which change argued wrongly from it, still constrains the next
  change and stays. History no change is constrained by belongs to `git log` and
  the change specs.
- **Anything aspirational.** A rule nobody follows teaches the agent the file is
  decorative, and it discounts the real ones.

## Which file

**The context file is the instructions file the harnesses in use read first** —
`CLAUDE.md` for one harness, the cross-harness `AGENTS.md` for several; this page
says CLAUDE.md because that is where it started. **The bindings name the file**,
so the gates and the audit read the one meant; where they name none, the first in
the harnesses' own order is read, and every line says which.

**One file, never two** — not even a second file pointing at the first. A harness
that reads one file per directory reads the first in its order and never the rest:
Pi reads `AGENTS.md` before `CLAUDE.md`, so a `CLAUDE.md` beside an `AGENTS.md` is
never read there, while the gates holding it pass. The audit reports two files as
open, and the sitting brings them to the one every harness in use reads.

## Where it goes

The repository root, where every harness looks; `.claude/CLAUDE.md` is loaded by
Claude Code and not by Pi. A repository that is itself a plugin root gets a
warning from `claude plugin validate` for a CLAUDE.md there: narrow the tool's
strictness rather than move the file, and write the reason in `specs/setup/`.

**Write it for the agent.** Every session is handed it; a person reads it
occasionally and opens the spec layer instead. It is prose rather than
configuration because it carries judgment — what the repository is for, what to
read, what never to copy.

## Length

**The file has a ceiling, and the number is the repository's**: named in its
bindings in a unit its gate reads, with what reads it and which change set it,
written from the file's size once the sitting has finished with it, and raised
only in the change that needs the room, with the reason beside it. Past it,
something here is a pointer that turned into a copy: move it to `specs/setup/`
and link it.

**And never above two hundred lines** — the reader's own documented limit, past
which adherence drops. It is the one number the method carries, because it is
about the reader, not the repository. A ceiling written above it fails the build
before the file's size is read.

The file is paid on every turn, again after compaction and by every subagent;
attention is a budget every token draws on; and earlier instructions are followed
more reliably than later ones. So:

- a line stays only if removing it would cause a mistake;
- the rules most often broken come first;
- count instructions, not lines — one line can hold three;
- emphasis on one line at most;
- what applies to one part of the codebase goes in a rule that loads only with
  those files.

**The test before committing:** could an agent that read only this file and the
bindings make a correct first change? If yes, stop. If no, the missing thing is
usually a pointer, not a paragraph.

## Keeping it true

*From: delete what stops being true.* A stale context file is worse than none,
because it is trusted by default. It is corrected in the change that made it
wrong — a moved directory, a renamed command, a changed rule — as part of that
change, not as a spec of its own. **There is no reference file**: a named example
is a template with extra steps, and a copied file is the first thing to drift.

## When it is out of line

A stale path is fixed by moving the line. A file missing a requirement, or
carrying what must stay out, is **rewritten from the requirements**, not patched:
a patch made requirement by requirement keeps the property that made it bad.

1. **Harvest first.** List every fact only this file knows — the deployment that
   makes every route somebody else's, the convention no tool enforces, what it
   used to claim and which change argued wrongly from it — and carry each into
   the new file, or name it as dropped with the reason and where it lives instead.
2. **Show the new file whole**, beside what was kept and what was dropped, and
   wait. A yes given at the start of a sitting does not cover replacing a file
   somebody wrote by hand.

The sitting does the rewrite. The audit corrects a line where a line is the
finding and, where the file needs rewriting, leaves it open with the sitting
named: it changes the record, never the wiring.

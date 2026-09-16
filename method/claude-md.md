# What a CLAUDE.md has to contain

**This is a list of requirements, not a file to copy.** There is no CLAUDE.md
template on purpose: a file assembled by filling in somebody else's blanks reads
exactly like one, and it is the first thing an agent reads about a repository it
has never seen.

Write it for **an agent arriving mid-task with no context**, that will act on
what it says. Everything in it is either load-bearing or noise, and noise is
expensive here — it is in front of every request, forever.

## What must be there

**1. What this is, in two or three sentences.** What the product is, what the
repository is *for* — those are often different — and what the deliverable of a
version is. If the app is a means to demonstrate something, say that plainly;
an agent that thinks the app is the point will optimise the wrong thing.

**2. Who writes what.** If AI writes the code and a human only uses and approves,
say so. It changes how everything else in the file should be read.

**3. That the process is a plugin, with a link, and that reading it is not
optional.** The rules, the loop, the gate semantics and the templates are not in
this file and must not be copied into it. One line saying where they live, and
that they are context rather than reference material.

**4. The line between the plugin and the repository.** One sentence, testable:
if a sentence could survive a repository with pytest and a Makefile it belongs
in the plugin; if it names a command, a filename, a threshold or a language it
belongs in `specs/setup/`. Without this, process improvements get committed to
the wrong repository and the two copies drift.

**5. A table of pointers** — the bindings, the constraints, the persona layer,
the workflow layer, the journey layer, and how the spec layers fit together. One
line each on what a reader would go there *for*. This table is most of the file's
value: it is a map, not a summary.

**6. The loop, numbered.** Eight steps at most, one line each. It is the thing an
agent is supposed to follow, and a link to it elsewhere is one indirection too
many at the moment it matters. **The approval step says what the person is
holding** — the spec, and the sketch drawn from it. *Human approves* on its own
is that step as it read before there was anything to hold, and it is what a file
written back then still says to every session that opens it.

**7. The rules worth having in front of you — a subset, not all of them.** Link
the full set in the method and then list the ones that actually get broken here:
spec before code, one change per version, feedback is never fixed on the spot,
never touch `src/` from a skill, rule ids are permanent, every commit green, a
rule-bound test runs in the world its boundary row names.
**A rules list nobody finishes reading enforces nothing.**

**8. The commands.** Verification first, then whatever a session needs to run the
thing. Four or five lines in one block.

**9. The layout**, annotated. Not `ls` output — a line per directory saying what
belongs there, so a new file lands in the right place without an argument.

**10. Where it lives.** The live URL if there is one, and where issues go.

## What must stay out

- **Anything the plugin already says.** A rule stated in two places is a rule
  that will be edited in one.
- **The reasoning behind a decision.** That is `specs/setup/constraints.md`,
  where somebody will look for it and where it can be argued with. The rule it
  produced stays here, with the one line that says why the rule is not
  aspirational.
- **Style guides, formatting rules, commit-message templates** the tooling
  already enforces. If a linter can say it, the linter says it.
- **History that binds nothing.** The test is whether it still changes what the
  next change may do. A dated account of what this file used to claim, until
  when, and which change argued wrongly from it, is a rule with its evidence
  attached, and stays — it is what stops an agent discounting that rule as
  decorative. An account of something no change is constrained by is history,
  and `git log` and the change specs are where it goes.
- **Anything aspirational.** A rule nobody follows teaches an agent that the file
  is decorative, and it will then discount the rules that are real.

## Where it goes

The repository root. `.claude/CLAUDE.md` is also always loaded and is a legitimate
place for it, but the root is where every other repository keeps it, and a file
where everyone already expects it is one nobody has to be told about.

**The reader you can count on is the agent.** This file is handed to every
session whether or not anybody opens it, and a human reading it is occasional —
in a repository with a spec layer, that is what a person opens instead, because
it is the part that says who the work is for and what they were trying to do. So
write the prose for the agent that acts on it: it is prose rather than
configuration because what it carries is judgment to apply — what this repository
is for, what to read, what never to copy — and none of that is a setting. The
length rule below is a context-cost argument for the same reason, not an
attention-span one.

**One repository in a hundred will hit a tool that objects**: a repository that
is itself a plugin root gets a warning from `claude plugin validate`, because a
CLAUDE.md there is not shipped as context to anyone installing the plugin. That
is a reason to narrow the tool's strictness, not to move the file — and the
reason belongs in `specs/setup/` either way, because the next person will wonder.

## Length

**The file has a ceiling, and the number is the repository's.** Its bindings
name it — in a size its gate can read, with what reads it and which change set
it. The figure is written from what the file is when the sitting has finished
with it, and it is raised only in the change that needs the room, with the
reason beside the number, so that growth is a line in a diff rather than a
drift nobody sees. The method names no figure: a threshold here is a binding in
the wrong file, and requirement 4's line between the plugin and the repository
holds for this page too.

Why a ceiling at all: this file is in front of every request, so it is the
repository's always-on cost. Past it, something in it is a pointer that turned
into a copy — move it to `specs/setup/` and link it. The requirements above
already bound the file — two or three sentences here, eight steps at most,
four or five lines in one block, a line per directory — so a file that meets
them is short, and the number is what stops it growing afterwards.

**And never above two hundred lines.** That is the target the reader's own
documentation gives for one of these files, past which it says adherence
drops, and it is the one number this method carries: it is about the reader,
not the repository, so it survives every repository with pytest and a
Makefile, which is the test. A threshold that is a repository's own still
belongs in its bindings. A ceiling written above the limit fails the build
before the file's own size is read.

What the length costs, in a sentence each, is why the number is low. The file
is paid on every turn, again after compaction, and again by every subagent
that starts; a model's attention is a budget that every token draws on; and
instructions earlier in a file are followed more reliably than those after
them. So: only what is critical — a line stays if removing it would cause a
mistake, and goes if it would not; the rules most often broken come first;
count instructions rather than lines, since one line can hold three; emphasis
on one line at most, because emphasis on many is emphasis on none; and what
applies to one part of the codebase goes into a rule that loads only with the
files it applies to, not here.

The test to apply before committing it: *if an agent read only this file and the
bindings, could it make a correct first change?* If yes, stop writing. If no, the
missing thing is usually a pointer, not a paragraph.

## Keeping it true

A stale CLAUDE.md is worse than none, because it is trusted by default. It gets
corrected in the same change that makes it wrong — a moved directory, a renamed
command, a rule that changed. That is a fix, not a change spec: it belongs to
whatever change made it stale.

**There is no reference file, on purpose.** The requirements above are the
contract; a named example is a template with extra steps for anyone in a hurry,
and a file copied from another repository is the first thing in this one that
will drift.

## When it is out of line

A stale path is a fix: the line moves, in the change that moved the path. A
file missing a requirement, or carrying what must stay out, is not fixed by
the line. It is rewritten from the requirements, whatever it is currently
worth, because a patch made requirement by requirement preserves exactly the
property that made it bad — it was assembled from somebody else's blanks, and
a patched template is a template.

Before the rewrite, harvest. List every fact only this file knows — the
deployment that makes every route somebody else's to call, the convention no
tool enforces, the account of what this file used to claim and which change
argued wrongly from it — and carry each into the new file or name it as
dropped, with the reason and where it lives instead. A rewrite that loses one
of these is a regression with a tidy diff.

Show the new file whole, beside what was kept and what was dropped, and wait.
A yes given at the start of a sitting does not cover replacing a file somebody
wrote by hand; a rewrite that lands unasked is worse than the patch it
replaced. The sitting does this. The audit corrects a line where a line is the
finding and, where the file needs rewriting, leaves that open with the sitting
named — it changes the record and never the wiring, and a new file is the
sitting's kind of change.

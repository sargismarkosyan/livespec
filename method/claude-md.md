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
many at the moment it matters.

**7. The rules worth having in front of you — a subset, not all of them.** Link
the full set in the method and then list the ones that actually get broken here:
spec before code, one change per version, feedback is never fixed on the spot,
never touch `src/` from a skill, rule ids are permanent, every commit green.
**A rules list nobody finishes reading enforces nothing.**

**8. The commands.** Verification first, then whatever a session needs to run the
thing. Four or five lines in one block.

**9. The layout**, annotated. Not `ls` output — a line per directory saying what
belongs there, so a new file lands in the right place without an argument.

**10. Where it lives.** The live URL if there is one, and where issues go.

## What must stay out

- **Anything the plugin already says.** A rule stated in two places is a rule
  that will be edited in one.
- **Explanations of decisions.** Those are `specs/setup/constraints.md`, which is
  where somebody will look for the reasoning and where it can be argued with.
- **Style guides, formatting rules, commit-message templates** the tooling
  already enforces. If a linter can say it, the linter says it.
- **A history of the project.** `git log` and the change specs are the history.
- **Anything aspirational.** A rule nobody follows teaches an agent that the file
  is decorative, and it will then discount the rules that are real.

## Where it goes

The repository root, in every ordinary repository.

**The exception is a repository that is itself a plugin root** — one with a
`.claude-plugin/` directory. A `CLAUDE.md` there is not loaded as context for
anyone who installs the plugin, and `claude plugin validate --strict` says so; the
file belongs at `.claude/CLAUDE.md`, which Claude Code always loads for that
project. Record the reason in `specs/setup/`, because the next person to read the
root will wonder where it went.

## Length

**One screen of scroll, and about a hundred lines.** If it is longer, something
in it is a pointer that turned into a copy — move it to `specs/setup/` and link
it.

The test to apply before committing it: *if an agent read only this file and the
bindings, could it make a correct first change?* If yes, stop writing. If no, the
missing thing is usually a pointer, not a paragraph.

## Keeping it true

A stale CLAUDE.md is worse than none, because it is trusted by default. It gets
corrected in the same change that makes it wrong — a moved directory, a renamed
command, a rule that changed. That is a fix, not a change spec: it belongs to
whatever change made it stale.

**The reference implementation is
[todo-change's](https://github.com/sargismarkosyan/todo-change/blob/main/CLAUDE.md)**
— every requirement above, in about a hundred lines. Read it as an example of the
shape, not as a file to fill in.

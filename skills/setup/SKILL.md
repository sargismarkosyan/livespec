---
name: setup
description: Set this process up in a repository — read what is already there, wire the two gates in that project's own language, write specs/setup/README.md as its bindings, and write CLAUDE.md. Use when adopting livespec in a new or existing repository, when asked to initialise the specs, wire the traceability gate, "set up the process here", or when a repo has the plugin enabled but no specs/setup/README.md for the skills to read. Interviews for what only the human knows, proves every gate fires before handing back, and never writes application code.
disable-model-invocation: true
---

# Set the process up here

Every other skill in this plugin reads `specs/setup/README.md` before it assumes
a command. **This skill is what puts that file there**, along with the gates it
describes and the CLAUDE.md that points at both.

**It writes no application code, ever.** And it does not invent a persona, a
workflow or a journey — those are [`refine-personas`](../refine-personas/SKILL.md),
[`refine-workflows`](../refine-workflows/SKILL.md) and
[`refine-journeys`](../refine-journeys/SKILL.md), each its own conversation. What
this skill produces is the structure they land in and the gate that keeps them
honest.

## 1. Read the repository before writing anything

Find out what is true, and say it back before you touch a file:

- **Language, test runner, coverage tool, package manager.** Whatever is already
  installed wins. Do not add a dependency to satisfy this process.
- **The command that already means "everything passes."** Most repos have one.
  It becomes the verification command; a second one nobody runs is worse than
  none.
- **CI**, if there is any: what runs, and what the required check is called.
- **Existing documentation** — a README, a CLAUDE.md, an ADR folder, a `docs/`
  tree. Some of it is already the context this process wants; it gets pointed at,
  not rewritten.
- **Greenfield or occupied?** A repository with 40,000 lines already in it is a
  different job from an empty one, and section 7 is about the difference.

Say what you found in a short paragraph. If the repo has no tests and no CI at
all, say that too — the process still installs, but the coverage gate has nothing
to stand on yet and the bindings file must admit it rather than name a threshold
nobody measures.

## 2. Ask the four things you cannot find out

One round, with your recommendation attached to each. Everything else you decide
yourself and record.

- **What is being built, and what is the deliverable of a version?** A moving
  picture per version is this method's default and the reason the loop ends where
  it does. A repo with no UI answers differently — a benchmark number, a
  changelog entry, an example script that runs. Whatever it is, it has to be
  something a person can look at.
- **Who is it for?** One sentence, and one sentence on who it is *not* for. This
  is the seed for the persona layer, not the persona — do not write the file from
  this answer, hand it to `refine-personas` afterwards.
- **What is the verification command, and what are the coverage thresholds?**
  Recommend what the repo already has. A threshold below what the code already
  scores is a ratchet that never moves; one far above it fails on day one and
  gets switched off by Friday.
- **Is `main` protected, and what is the required check called?** If nobody can
  change repository settings, say so in the bindings — an unenforceable rule
  written as enforced is the worst line in any setup file.

## 3. Put the skeleton in, and nothing more

```
specs/
  spec.md                what it is, the vocabulary, the storage contract
  personas/README.md     the layer's own rules
  workflows/README.md
  journeys/README.md
  features/
  changes/
  setup/README.md        the bindings — section 5
tests/
  behaviour/  unit/  workflows/
docs/screenshots/        or whatever the deliverable turned out to be
```

**Create a directory when something goes in it, not before.** A tree of empty
folders and placeholder files reads as a process that was installed and never
run, and the traceability gate cannot tell an empty layer from a broken one.

The layer READMEs are worth writing now, because they are what stops the layers
being filled in wrong. Everything else waits for the skill that owns it.

## 4. Wire the gates, in the project's own language

[`gates.md`](../../method/gates.md) says what they have to mean. This is where
that gets turned into commands.

**Traceability**, both directions, is the one that has to be built rather than
configured:

- read the `.feature` files, collect every `@rule:` id and its `@planned` state;
- read the test sources and collect every rule id they claim — a function call,
  a decorator, a docstring tag, whatever suits the language;
- fail when a live rule has no test, when a test names an id that does not exist,
  when a behaviour test claims nothing at all;
- then the layer above: features name workflows, workflows name personas and are
  walked by a test, journeys name workflows that exist.

**Write the smallest thing that does that.** One script, no dependencies, in the
language already in the repo. It is a few hundred lines at most and it belongs in
the repository rather than in this plugin, because CI has no plugins installed —
the moment verification depends on something an agent session installs, it stops
being the thing CI runs.

**Coverage** is whatever the language already has. Lines, branches and functions
if the tool reports all three; the thresholds are the ones agreed in section 2.
If the tool reports only lines, say so in the bindings and say what that misses.

**One command runs both**, and CI runs that same command. Not a longer list in CI
than a person can run locally.

### Then break them, one at a time

A gate that has never failed is not known to be a gate. Walk the
[injection table](../../method/gates.md#both-gates-are-verified-to-fire): break
each row in turn, run the gate, read the message it produces, revert. **Record
the results in `specs/setup/README.md`.**

This is the step that gets skipped, and skipping it is how a repository spends
six months with a required check that has been passing on an empty glob.

## 5. Write `specs/setup/README.md` — the bindings

This is the file every other skill reads. It has to answer, in one table a person
can scan: what verification is, what runs each gate, where the rule-claiming
helper lives, how tests are discovered, what the coverage thresholds are, what
the required check is called, where the app runs, and anything else a skill would
otherwise have to guess.

It also carries what cannot live in a diff: the branch protection settings, the
CI wiring, and the record of the fault injection from section 4.

**Every fact in it is about this repository.** If a sentence could survive being
moved to another repo, it belongs in this plugin instead, and putting it here is
how the two copies start to disagree.

## 6. Write CLAUDE.md

Follow [`claude-md.md`](../../method/claude-md.md) — it says what has to be in
it, what must stay out, and why. **It is a list of requirements, not a file to
copy.** A CLAUDE.md assembled by filling in somebody else's blanks reads exactly
like one, and the agent that has to trust it can tell.

## 7. An existing codebase does not get retroactive specs

The temptation is to spec what is already built. Do not.

- **Write nothing about behaviour that already exists** except where a change is
  about to touch it. Forty backfilled change specs are forty documents nobody
  checked against the code, and the gate cannot tell an accurate one from a
  guess.
- **The spec layer starts at today.** The first change spec is numbered `0001`
  and describes the next change, not the history.
- **Existing tests do not have to claim a rule.** They are unit tests as far as
  this process is concerned until a rule exists that they answer to. Say this in
  the bindings, or someone will spend a week retrofitting decorators.
- The exception is a rule the codebase *already* breaks: that is not
  documentation, it is a bug, and it goes through `feedback` like any other.

## 8. Enable the plugin, then hand back

Declare the marketplace and enable the plugin in the repository's
`.claude/settings.json`, so a fresh clone gets the process without a manual
install.

Then hand back, short:

- the verification command, and the fact that it is green;
- which faults you injected and that each one failed the way it should;
- **what is still empty** — almost certainly the personas, the workflows and the
  journeys — and which skill fills each;
- **the one next thing**: run `refine-personas`, because every other layer is
  downstream of it and a workflow written for nobody has to be written twice.

## What this skill refuses

- **Writing application code.** Not one line, including a test for code that
  already exists.
- **Inventing a persona or a workflow** from the seed in section 2. The seed is
  an answer to "who is this for", not a design artifact, and treating it as one
  is how a product ends up built for somebody nobody ever met.
- **Adding a dependency** to make the process fit. If the gate needs a library,
  it is too big.
- **Copying another repository's numbers.** A 95% threshold that came from
  somewhere else is a number nobody chose.
- **Installing over an existing setup without saying what it will overwrite.**
  Show the list first; a CLAUDE.md somebody wrote by hand is context, not clutter.

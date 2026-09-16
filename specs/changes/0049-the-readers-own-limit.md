# Spec 0049: the reader's own limit

- **Status:** proposed
- **Issue:** none — a direct request on 2026-09-16, before the last of the
  three CLAUDE.md issues: *"make a note in that one that CLAUDE.md file can't
  be very long, make a research of what is the optimal length of claude MD
  files for Opus and Sonnet files and make sure that we have gate for that
  one too. We need to make sure that we are only capturing the critical info
  so that the attention will not slip."* The research is a deck, linked from
  the sketch; this spec is what it decided.
- **Depends on:** [`0046`](0046-a-number-and-no-file-to-copy.md), which put
  the repository's ceiling in its bindings, and
  [`0048`](0048-the-file-every-session-reads-first.md), which made the gate
  read it. This adds the bound the ceiling may not exceed.

## Who this is for

[`agent-accelerated-owner`](../personas/agent-accelerated-owner.md), in
[`adopt-the-process`](../workflows/adopt-the-process.feature), at the sitting
that writes CLAUDE.md and at every change after it — and, more than in either
spec before this, for the agent that reads the file, which the persona file
keeps out of the persona layer on purpose and the product spec holds as a
constraint. The persona's own words are the case: *"I have not read it. It
only for AI."* A file nobody reads and every session pays for has exactly one
reader, and the limit on it should be that reader's.

**This lengthens the sitting by nothing.** The row section 6 already writes
gains a bound. What it shortens is every session in every repository this
process is installed in: a file that cannot grow past the point where the
reader's own documentation says adherence drops.

**`context-budget`** is the always-promise touched, and touched from the
other side: the promise is about what every session of every user pays for
this plugin's descriptions, and a consuming repository's CLAUDE.md is the same
cost one repository over — the reason 0046 gave for a ceiling at all. This
spec puts the number on it.

## The job behind the request

The literal ask is above. The job: **the method should say how long a CLAUDE.md
may be at most, from evidence about the reader rather than from a guess, and
the build should refuse a repository that sets its ceiling above that.** After
0046 and 0048 the ceiling is a number in the bindings, written from the file's
size and raised in the open — a ratchet, with no top. A repository that writes
its ceiling as nine hundred lines has broken nothing, and its file will be
read by a model whose own documentation says a file that long reduces
adherence. The method said *about a hundred* until 0046 removed it as a
threshold in the wrong file, and said nothing in its place about a maximum.

What the research found, read on 2026-09-16:

- **Anthropic's own figure.** The Claude Code documentation on CLAUDE.md
  says, under *Write effective instructions*: *"Size: target under 200 lines
  per CLAUDE.md file. Longer files consume more context and reduce
  adherence."* The same page says imports *"help organization but do not
  reduce context, since imported files load at launch"*, that CLAUDE.md is
  *"delivered as a user message after the system prompt"*, and that *"shorter
  files produce better adherence"*. The best-practices page adds the test —
  *"for each line, ask: would removing this cause Claude to make mistakes? If
  not, cut it"* — and the failure: *"if your CLAUDE.md is too long, Claude
  ignores half of it because important rules get lost in the noise."*
- **What it competes with.** The documentation's own startup walkthrough
  loads about 7,850 tokens before the first prompt — a 4,200-token system
  prompt, an example project CLAUDE.md of 1,800, auto memory, skill
  descriptions, the user file, the environment — so the project file is
  roughly a quarter of what is in front of every request, re-injected after
  compaction, and loaded again by every subagent. This repository's file is
  about 2,100 tokens by a four-bytes-per-token estimate.
- **Why length costs adherence.** Anthropic's engineering note on context:
  models have an *"attention budget"* that *"every new token depletes"*, and
  the aim is *"the smallest possible set of high-signal tokens"*. Chroma's
  *Context Rot* study ran eighteen models, Claude Opus 4 and Sonnet 4 among
  them, and found performance non-uniform with input length *"even on tasks
  as simple as non-lexical retrieval"*, the Claude models abstaining more as
  input grew. IFScale (2025, twenty models) found instruction-following
  degrading with instruction count, the best frontier models at 68% of 500
  simultaneous instructions, with a *"bias towards earlier instructions"*.
- **Opus and Sonnet.** No published figure separates them for this. IFScale
  re-run on 2026 models moved the count at which frontier models lose track
  from 200–300 to *"closer to 2,000"* — Claude Opus 4.7 following about half
  at five thousand — so for the current models the binding constraint is not
  how many instructions the file holds but the share of attention it takes on
  every turn and how reliably each line is followed against everything after
  it. Retrieval improving between Sonnet and Opus generations does not make
  noise free: the documented complaint is adherence, not recall. One limit,
  the reader's documented one, for both.

## Why now

Because the question was asked with the third CLAUDE.md issue still open, and
its answer changes what that issue's remedy is held to: a rewrite offered
under #99 needs to know how long the result may be. And because 0048 has just
made the ceiling a gate: the moment the number can fail a build is the moment
a number nobody bounded becomes a way to pass one.

## The end value

The method carries one number of its own, with its source and the reason it
is portable: a CLAUDE.md is at most two hundred lines, because that is what
its reader's documentation says and the reader is the same in every
repository. A repository's ceiling sits under it and the build refuses one
written above it. The method's page says, with the evidence behind it, what
earns a line in the file and what the file's length costs.

**How we would know it worked:** a bindings row naming a ceiling of 250 fails
verification naming both numbers, before the file's own size is read; the
three real files on this machine — 138, 134, 101 lines — pass without an
edit; and the sitting in #99's remedy has a bound to rewrite to.

## What changes

1. **[`claude-md.md`](../../method/claude-md.md), *Length*.** After the
   paragraph 0046 wrote, two more. The first names the limit: the ceiling is
   the repository's, and never above **two hundred lines** — the target the
   reader's own documentation gives, past which it says adherence drops. One
   number lives in the method because it is the reader's and not the
   repository's: it survives every repository with pytest and a Makefile,
   which is the test, and a threshold that is a repository's own still goes to
   the bindings. The second is the note the request asked for, with the
   evidence in a sentence each: the file is paid on every turn, again after
   compaction and again by every subagent; a model's attention is a budget
   every token draws on; instructions earlier in a file are followed more
   reliably than later ones. So: only what is critical — a line stays if
   removing it would cause a mistake; the rules most often broken come first;
   count instructions rather than lines; emphasis on one line at most, since
   emphasis on many is emphasis on none; and what applies to one part of the
   codebase goes into a path-scoped rule, not here.
2. **[`method/README.md`](../../method/README.md)** and
   **[`spec.md`](../spec.md)'s vocabulary**: the sentence *nothing here names
   a command, a threshold, a filename or a language* gains its one exception
   in a clause — no threshold *that is a repository's own*; the one number the
   method carries is the reader's. The vocabulary row for *method* moves the
   same way, in this spec commit, as prose spec.
3. **The gate.** [`gates.md`](../../method/gates.md)'s *The file every session
   reads first* gains a failure — *a ceiling above the limit the method
   names* — and a fault row; the meaning of `gate:context-file-ceiling` in the
   id table gains *"or a ceiling above the limit the method names"*, and
   [`tools/doctor.py`](../../tools/doctor.py)'s registry says the same, so
   the two stay one list. `trace.py` here carries the constant and fails a
   ceiling row above it, naming both numbers, before it reads the file's
   size. `inject.py` gains the fault: the fixture's row rewritten to 250.
4. **[`templates/bindings.md`](../../templates/bindings.md)** — the ceiling
   row's placeholder says *never above the limit the method names* — and
   **[`setup`](../../skills/setup/SKILL.md) §6**, the sentence that writes the
   row, says the same in a clause.
5. **One example** added to `a-context-file-past-its-ceiling-fails-the-build`,
   id kept, claimed by one more test in `tests/test_context_file.py`.
6. **This repository's bindings**: the ceiling row says the limit it sits
   under. The number stays 138.

**Rules added or changed** — the `@rule:` ids in `specs/features/`:

| Rule id | Feature file | New or changed |
|---|---|---|
| `a-context-file-past-its-ceiling-fails-the-build` | `features/wiring/context-file.feature` | changed — one example added, id kept |

**No description changes, so no should-not-fire case is owed.**
`context-budget` stays at 4321 of 5000.

## What we are not doing

- **Not a number per model.** Anthropic states the target per file, not per
  model, and it is the only vendor figure there is. A per-model limit would
  need re-measuring at every release, in a method that already refuses to
  record which version of anything built a commit.
- **Not a margin under two hundred.** The vendor's word is *under 200*; the
  gate refuses a ceiling above it, and the ceiling is the file's own size, so
  a repository sits wherever its file is. A tighter figure would be this
  repository's opinion presented as the reader's.
- **Not tokens.** The limit is stated in lines because that is the unit the
  reader's documentation states it in, and a repository whose gate counts
  characters converts. The token figures in the research are estimates and
  are labelled as such.
- **Not counting instructions mechanically.** *Count instructions, not lines*
  is guidance for the person writing the file; a script that counted bullets
  would be the wallpaper gate 0048 refused.
- **Not touching this repository's CLAUDE.md.** It is at 138 of 200, and the
  method's note on what earns a line is a question for its next audit, not
  for this change.

## Data

No storage. Files that move: `method/claude-md.md`, `method/README.md`,
`method/gates.md`, `tools/doctor.py`, `templates/bindings.md`,
`skills/setup/SKILL.md`, `.github/scripts/trace.py`, `.github/scripts/inject.py`,
`specs/setup/README.md`, one `.feature`, one test file, `specs/spec.md` and
this spec.

**This spec commit stales nothing.** One example on a live rule that a test
claims — a rule's text is hashed into the measurement inputs of the *cases*
that claim it, and no case claims this one. `spec.md` moves, which nothing
hashes. `verify.py` exits **2** for the rows already owed and no other reason.

**The implementing change adds no stale row that is not already red.** It
edits `setup`'s body; every measured case holding `setup` is already owed.
No case is added.

**What the pull request owes.** `method/`, `templates/`, `tools/` and a skill
move — **`minor`**, a new failure in a gate — a `## Changelog` section, an
`## Ids` section reading *unchanged*, and a Gherkin block for the example.

## Risks

- **A number in the method reads as licence for more.** The carve-out is one
  clause and says why it holds: the number is about the reader, and a reader
  is what every repository shares. A threshold about a repository still fails
  the test and still goes to the bindings.
- **The vendor moves the figure.** Then the method moves with it, in a change
  that says so, and every consuming repository's audit reads the entry. That
  is the same path any method change takes.
- **A repository with a real reason to be longer.** It splits: path-scoped
  rules load only when the matching files are read, which is what the
  documentation says to do and what the note now says too.
- **Always-promises.** `always-green`: the failure is in the consuming
  repository's own gate, wired by its sitting. `ids-are-permanent`: no id
  moves. `never-implements`: prose and a constant.

## Acceptance checks

1. `python3 .github/scripts/inject.py`: 104 faults caught, the new one
   reading *fails*, the fixture green.
2. `tests.py`: green, the new test naming the ceiling rule and asserting both
   numbers in the message.
3. `method/claude-md.md` names two hundred lines once, with its source; the
   carve-out sentence reads in `method/README.md` and `spec.md`.
4. `verify.py` exits 2 for the rows already owed; the pull request carries
   `minor`, `## Changelog`, `## Ids: unchanged` and the Gherkin block.

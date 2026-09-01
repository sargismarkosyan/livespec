# livespec

## What it is

A Claude Code plugin: eight skills and the method they run, installed into
somebody else's repository so that the specification there cannot quietly stop
being true. The code stays the source of truth; the spec carries the context the
code cannot — who it is for, what they were trying to do, what was dropped and
why — and the connection between them is a thing that can fail a build.

**What this repository is for is not the same as what the plugin does.** The
plugin is prose that an agent reads. This repository is where that prose is
argued over, held against cases, and released. Optimising it like an application
— more features, more surface — is the wrong instinct: every skill added here is
context that every session of every user pays for, forever.

## The vocabulary

Use these words and no others for these things. A synonym invented in one file is
how two documents start meaning slightly different things.

| Word | What it means here |
|---|---|
| **skill** | One `skills/<name>/SKILL.md`. The only thing Claude Code loads from this repository. |
| **method** | The portable part, in `method/`. Names no command, threshold, filename or language. |
| **binding** | The part that is one repository's own — its commands, thresholds and paths. Lives in that repository's `specs/setup/README.md`, never here. |
| **payload** | `method/`, `templates/`, `tools/`. Ships to every user, loads only when a skill body sends the agent to it. |
| **component** | What Claude Code loads on its own. Here that is `skills/` and nothing else. |
| **always-on cost** | The characters every session pays for a skill's name and description, whether or not it fires. Measured by `checks.py`, budgeted, and the reason a description is the expensive field. |
| **fire** | A skill triggering on a request. **should-not-fire** is the case that holds a description from grabbing too much. |
| **case** | One directory under `evals/` — a prompt, its graders, and the tags saying what it holds. This repository's unit of test. |
| **grader** | One file that scores a case. An **outcome grader** scores what came out; `tool_used` only says something fired. |
| **arm** | One side of an ablation run: with the plugin loaded, or without. **Δ** is the difference, and it is the only number that says anything about livespec. |
| **consuming repository** | Somebody else's repository, with the plugin installed. Where `specs/setup/README.md` and the gates actually live. |
| **version** | A change spec number. Version 3 is the state of this repository after spec `0003` shipped. |
| **sketch** | What the person deciding on a change spec is shown beside it: the evidence that spec argues from, drawn *from* the spec. Never recorded from an app — that is the **picture** a version ships with, and the two are separate objects arriving at separate steps. |

Two words deliberately **not** used: *documentation*, for anything under
`specs/` — it is a contract, and calling it documentation is how it stops being
checked; and *test*, for anything under `evals/` — they are cases, they cost
money to run, and they are graded by a model rather than asserted.

## What a version leaves behind

There is no build output and no database. What a version writes down, and where:

- **the pull request description** — this repository's deliverable for a version,
  and now also its **source**. There is no app to record, so there is no moving
  picture; what stands in its place is the Gherkin a change moved, quoted in the
  body and checked by the gate. See [setup/README.md](setup/README.md).
- **`.claude-plugin/plugin.json`** — the `version` field, which pins every
  install. A change merged without moving it reaches nobody.
- **`CHANGELOG.md`** — one entry per version.
- **a git tag** `livespec--v<version>`, and the GitHub Release that carries the
  same entry.

**The last three are written by the pipeline, not by hand.** `main` is
production — the marketplace takes no ref, so `/plugin update` reads `version`
off that branch — and merging is therefore releasing. On merge,
`release.yml` derives the number from the pull request's `patch`/`minor`/`major`
label and the entry from its `## Changelog` section, then writes all three.
What a contributor leaves behind is the description; the rest follows from it.

**Nothing records which version of the method built a given commit** in a
consuming repository. Where a change here would read badly against old commits
there, the change says so in its own spec.

What a consuming repository *does* record is **setup-level**: the gate wiring
ledger in its `specs/setup/README.md` carries the plugin version that wiring was
last reconciled against. That is a fact about the process installed there, not
about any commit — no commit gains provenance, and the ledger answers *what was
this last checked against*, never *which version wrote this line*. The two are
named apart here because a stamp on a repository reads, at a glance, like a stamp
on its history.

## The promises that belong to no single workflow

Standing commitments. A change spec that serves one of these rather than a
workflow names it here.

- **`always-green`** — nothing in this repository can fail a user's build. A
  plugin is available to an agent, not to a build runner, and the method is
  written so it never needs to be. A change that makes a user's CI depend on
  something installed by an agent session breaks this.
- **`context-budget`** — every session pays for the always-on descriptions. The
  budget in `checks.py` is a real ceiling, and widening a description is paid for
  in `evals/` with a should-not-fire case, never on a hunch.
- **`never-implements`** — no skill touches application code. `feedback` files,
  `refine-*` specs, `record-clip` records. A change that relaxes this is a change
  to what livespec is and has to be argued as one.
- **`ids-are-permanent`** — a rule, workflow or persona id, once published, is
  never reused or renamed. Renaming one orphans every case pointing at it in
  every consuming repository at once.
- **`gates-are-proven`** — no gate ships without a fault that makes it fire.
  `inject.py` holds this one to account on every run.

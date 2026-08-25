# Spec 0018: said once, not searched for

- **Status:** proposed
- **Issue:** [#40](https://github.com/sargismarkosyan/livespec/issues/40) — the
  half a fixture could not answer, now that the re-measure it asked for has been
  taken.

## Who this is for

[`@persona:agent-accelerated-owner`](../personas/agent-accelerated-owner.md) —
Ren, in a repository that is half set up, which across several repositories at
once is most of them.

The feature names `adopt-the-process`, the only live workflow, and the same tag
[`0009`](0009-whose-repository-whose-tracker.md) and
[`0016`](0016-captured-or-built.md) put on the `routing/` files for rules that
govern a skill used daily long after the sitting ends. **The honest version:**
this belongs to *filing what they found*, which
[the workflows README](../workflows/README.md#three-more-attempts-not-written-yet)
lists as real and uninterviewed. This spec does not cut it.

It serves no always-promise. `context-budget` is the one it comes nearest and it
is **not touched**: no `description` changes here, and `method/` is payload —
it costs nothing until a skill body sends the agent to it.

## The job behind the request

**Come out of the session holding the work, even when the repository could not
finish it.**

The thing they are standing in is rarely fully set up. Something a step needs is
not there — the tool is not installed, the file was never written, the path in
the report points at nothing. What they want from that is a straight answer and
whatever got done, in the same reply. What they do not want is to find, at the
end, that the whole session went into looking for the missing thing and there is
nothing to show for it.

## Why now

**Because the re-measure came back and the number stayed negative.**
[`#40`](https://github.com/sargismarkosyan/livespec/issues/40) named the
condition itself — *let `0016` land and re-measure this case cleanly; if the
delta stays negative with the tree still, the behavioural question is worth a
spec.* It landed. On [`board.json`](../../evals/board.json),
`15-tracker-is-not-the-assumed-one` now reads **Δ −0.17** at `runs: 3`, measured
against `cc627c0` — the implementation commit of `0016`, with nothing moving
under it. That is the clean reading the issue asked for, and it is still the
plugin arm losing to the bare model.

**Because the whole deficit is one session, and the transcript says exactly what
it did.** Of six sessions, five scored 1.00. The sixth scored 0.5, and the
`evidence-link-resolves` grader's own words are *"The agent never reached the
point of filing anything."* It made **39 tool calls — 15 of them `ToolSearch`
for a Bash tool the run never granted, and 6 subagent spawns** — more calls than
any other session in the case, over half of them spent looking for a way to run
a command. It never delivered the reply.

**Because the plugin was not wrong about anything it was asked.**
`uses-the-named-tracker` passed in all three with-arm sessions, that session
included: it read the bindings, cross-checked the remote, refused to fall back
to `gh`. What it lost on was **what it spent** when a step would not go through.
The two with-arm sessions that scored 1.00 hit the identical wall and wrote the
body, said plainly they could not run `glab` from there, and handed over the
command. So did all three without-arm sessions. The wall was equal in every arm;
only the response to it differed.

**Because the skill body is why.** Every step in
[`feedback`](../../skills/feedback/SKILL.md) is written as an action with its
means assumed present — file it, copy the screenshot in, commit and push it,
list what the tracker holds. `specs/setup/README.md` is where it learns *which*
tool. Nothing anywhere tells it what to do when the tool is not reachable from
where it is standing. The one sentence that comes close says
*"Where there is no tracker at all, say so and stop; there is nowhere to file"* —
and **`stop` with no hand-over is the failure, not the fix**: it is where that
session was heading anyway.

## The end value

A session in a half-set-up repository ends with the researched issue body and
the exact command to file it, instead of ending with the budget gone and nothing
written down. The missing thing is stated in a line and the rest of the work
still arrives.

**How we would know it worked:** `15-tracker-is-not-the-assumed-one` stops
losing to the bare model — Δ at or above 0.00 on the next clean re-measure. And
a new case, in a repository that records no bindings at all, comes back with
something to act on rather than with a search.

## What changes

Two files, plus the case that holds the rules. No `description` moves.

1. **[`method/process.md`](../../method/process.md) gains one section**, under
   *When the process gets in the way*, beside *A technical change that serves no
   workflow is correct, not a gap* — the same family: what honest behaviour
   looks like where the process meets a repository it does not fit.

   The shape of it: **what a step needs and cannot get here is said once and the
   work that did not depend on it is handed over finished.** Searching for a way
   around a missing means is the failure; the reply that names it and carries
   the rest is the answer. Portable — it names no command, no tool, no filename
   and no threshold.

2. **[`skills/feedback/SKILL.md`](../../skills/feedback/SKILL.md) §0 wires it.**
   A short paragraph: the tool the bindings name may not be runnable from this
   session, and the repository may record no bindings at all. Either way, say so
   once and finish everything that did not depend on it. The existing
   *"say so and stop"* sentence is amended in place — **stop, having handed over
   the body and what to run** — because as written it licenses the empty ending.
   It links to the method section rather than restating it.

3. **One new eval case** claims both rules, written in the implementing change:
   a report against a repository with a real bug, a remote, and **no
   `specs/setup/README.md` at all**. That is the sparse repository `#40` says
   still bites, and no fixture in `evals/` is one.

**Rules added or changed** — the `@rule:` ids in `specs/features/`:

| Rule id | Feature file | New or changed |
|---|---|---|
| `an-unreachable-step-is-said-not-searched-for` | `features/reach/absent-means.feature` | new |
| `what-did-not-need-it-is-still-handed-over` | `features/reach/absent-means.feature` | new |

Both are `@planned` and the file — a new area, `reach/` — is committed with this
spec.

**Ledger:** nothing moves. No new gate.

## What we are not doing

- **Not wiring the other six skills.** The sentence goes in `method/` once,
  where the line test puts it, and exactly one skill body is pointed at it here —
  the one with a transcript behind it. The obvious next candidate is named and
  deliberately left: on the current [board](../../evals/board.json) two of the
  three `setup` cases sit below zero — `11` at −0.11 and `12` at −0.10 — which
  looks like this same class of failure on a second skill. **That reading is
  weaker than it was when `#40` raised it.** The note there cited −0.33, −0.11
  and −0.24 with none up; `0016`'s full re-measure has since moved `09` to
  **+0.17**, so what is left is two small negatives rather than three. It wants
  its own issue and its own evidence, and a pointer added to a skill on a hunch
  is the move this repository does not make.

- **Not naming a number of turns.** *"Stop and say so in one turn"* is `#40`'s
  phrasing and a count is a binding, not method. What is wrong is the hunt, and a
  rule that says *say it once* holds in a repository with a fast tool and one
  with a slow one alike.

- **Not touching which repository or which tracker.**
  [`0009`](0009-whose-repository-whose-tracker.md)'s six live rules are not
  reopened. Those decide *where a thing goes*; this decides *what the session
  spends when it cannot get there*. In particular
  [`the-tracker-comes-from-the-bindings`](../features/routing/tracker.feature)
  already covers bindings that exist and name no tracker, and says what to
  conclude instead. Neither new rule says anything about what to conclude.

- **Not weakening the investigation.** Considered and rejected as a framing:
  *"do less looking."* [`feedback`](../../skills/feedback/SKILL.md) §3 is a whole
  section demanding the agent go and find out what is actually happening, and it
  is what makes these issues worth reading. See *Risks*.

- **Not re-cutting the workflows.** *Filing what they found* stays
  uninterviewed; `refine-workflows` owns it, and a workflow cut from a guess has
  to be cut twice.

- **Not re-measuring the board as part of this spec.** Implementation edits a
  skill body and stales every case that holds it. What that costs, and that it
  is the maintainer's signature rather than the implementer's, is in
  *Acceptance checks*.

## Data

None. There is no storage contract — the plugin ships prose, and what a version
leaves behind is listed in [spec.md](../spec.md#what-a-version-leaves-behind).

## Risks

- **The measured instance is partly the rig, and that has to be said first.**
  The failing session had no Bash, and not by accident:
  [`evals/README.md`](../../evals/README.md) makes *"no case grants `Bash`"* a
  floor of the suite, so **every** case runs unable to reach any tracker. Ren has
  Bash. So *"the tool cannot be run from here"* is manufactured by the rig, in
  all six `feedback` cases at once, and a fair reader can say the −0.17 measures
  the harness. The new case inherits the same floor deliberately rather than
  arguing its way around it. **The counter is inside the same run:** five other
  sessions hit the identical wall and handed the work over anyway. The wall was
  equal; the response was not, and that difference is the skill's. The condition
  is also real outside the rig — a machine with no `glab` installed is the
  ordinary case in the repository
  [`#10`](https://github.com/sargismarkosyan/livespec/issues/10) came from.

- **−0.17 is one session wide.** Three runs a side; the delta is one grader on
  one of six sessions. It is a **reproduction**, not a trend, and nothing here
  should be read as the latter. What earns the spec is that the transcript names
  the failure exactly, not that the number is large.

- **Δ may not move, and the change can still be right.** Five of six sessions
  already did this unprompted, which is what
  [`graded-cases.md`](../../method/graded-cases.md) says to expect wherever an
  instruction tells the model something it mostly knew. If the re-measure comes
  back 0.00 the rule is still worth keeping for the bad day — but the pull
  request owes that in a line rather than a claimed win.

- **A rule against hunting reads, wrongly, as a rule against investigating.**
  The two are not in tension and the distinction is the whole of it:
  investigating is looking for **the cause**, which is the most valuable thing
  `feedback` does; the hunt this stops is looking for **a way to perform a step
  that is not available here**. Written down because the wrong reading would gut
  §3, and the section that suffers is the one nobody would notice getting
  quieter.

- **The board cannot see a method change.**
  [`caselib.py`](../../.github/scripts/caselib.py)'s `measurement_inputs` hashes
  a case's own files, the text of the rules it claims, and the bodies of the
  skills it holds — **not** the `method/` pages a skill body sends the agent to.
  A change made only in `method/` would move what the agent reads while every
  board entry still looked fresh. This change also edits a skill body, so nothing
  goes stale-but-unmarked here. The gap is real, it is not this spec's to close,
  and it is recorded so it is found on purpose rather than by a number that
  quietly stopped meaning anything.

- **`ids-are-permanent`.** Two new ids ship and can never be renamed. Both are
  named for the promise and neither names `feedback`, so pointing another skill
  at the same method section later does not orphan them.

## Acceptance checks

1. `python3 .github/scripts/verify.py` green, and the always-on cost `checks.py`
   reports **unchanged at 3800 across 7 skills**. This change touches no
   `description`; a move there means a sentence went into the wrong file.
2. Read the new `method/process.md` section against the line test — *could this
   survive a repository with pytest and a Makefile?* It must name no command, no
   tool, no filename and no threshold. If it names one, it belongs in the
   bindings and the section is wrong.
3. In a repository with no `specs/setup/README.md`, report a bug. The reply says
   in a line that the repository records no bindings, and still carries a
   researched issue body.
4. Same repository, read the transcript: no search for a file nobody ever wrote.
5. In a repository whose bindings name a tracker tool that is not installed,
   report a bug. The reply carries the body and the exact command to file it, and
   does not end empty.
6. Read `feedback` §3 back after the edit. It must still demand the
   investigation it demands today — see *Risks*.
7. **The measurement, and it costs money.** Editing `skills/feedback/SKILL.md`
   stales every case tagged `skill:feedback` — `02`, `13`, `14`, `15`, `18`,
   `19` — plus the new case's first entry. `verify.py` stays red until
   `run.py --changed` re-measures exactly those. **Priced off the board's own
   recorded costs, not off a remembered figure:** those six last cost **$7.33**
   together at `runs: 3`, against **$18.66** for all nineteen — so this is
   roughly **two-fifths of a suite**, plus whatever the new case comes to.
   **The implementing change stops and asks before spending it.** The number
   goes in the pull request, and the commit can be finished with a gap where it
   goes.

   Worth knowing before quoting a price: `CLAUDE.md` says *"about $1.80 for one
   case, ~$4 for the suite"*, and the board disagrees with both — nineteen cases
   at $1.80 cannot come to $4. The board is measured and that sentence is
   remembered. Fixing it is not this spec's, but do not price a run off it.

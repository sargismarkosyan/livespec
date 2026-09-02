# Spec 0019: what would end it

- **Status:** approved
- **Issue:** [#28](https://github.com/sargismarkosyan/livespec/issues/28) — a
  local workaround has no expiry, filed as a seam rather than a defect.

## Who this is for

[`@persona:agent-accelerated-owner`](../personas/agent-accelerated-owner.md) —
Ren, in the repository where the plugin did not fit and the work carried on
anyway. That is not a hypothetical: it is
[`wf-developer-agents`](https://github.com/sargismarkosyan/livespec/issues/10),
the only downstream adoption livespec has ever had.

**This serves a seam, and a seam belongs to no workflow.** It is the fourth
opportunity row in
[`trusting-the-spec-again`](../journeys/trusting-the-spec-again.md) — *a local
workaround has no expiry* — sitting between the journey's *Where it does not
fit* phase and its *Coming back* phase, which is precisely why neither one owns
it. The feature names `adopt-the-process`, the only live workflow, the same way
[`0009`](0009-whose-repository-whose-tracker.md),
[`0016`](0016-captured-or-built.md) and [`0018`](0018-said-once-not-searched-for.md)
name it for rules that govern a skill used daily long after the sitting ends.
**The honest version:** the recording half belongs to *filing what they found*,
which [the workflows README](../workflows/README.md#three-more-attempts-not-written-yet)
lists as real and uninterviewed, and the reading half belongs to the seam. This
spec cuts neither.

It serves no always-promise. `context-budget` is untouched — no `description`
moves here — and the promise this comes nearest to bending is
`never-implements`, which is argued in *Risks* rather than assumed.

## The job behind the request

**Stop carrying a second thing to maintain.**

The repository in front of them is one of several, and the process installed in
it did not fit somewhere. They did the right thing twice — filed the mismatch
where it could be fixed for everyone, and kept the local version so the work
would not stop. What they will not do is check, repeatedly and forever, whether
somebody else has since removed the reason. The whole point of adopting this was
to stop having things that quietly stop being true, and a workaround whose cause
is gone is exactly one of those.

## Why now

**Because the instance is not hypothetical and it is running right now.**

[`#10`](https://github.com/sargismarkosyan/livespec/issues/10) reported that
`feedback` assumed GitHub in a repository whose tracker is a corporate GitLab,
and it says in its own body: *"kept the repo's own local `feedback` skill for
now rather than adopting `livespec:feedback`, specifically because of this
gap."* It shipped in **0.11.0**, on 2026-08-25, as
[`0009`](0009-whose-repository-whose-tracker.md). The plugin is now at 0.18.0 —
seven versions past the fix.

The close comment on that issue names the acceptance test in as many words:
*"the check that matters is yours… If `livespec:feedback` can now replace the
hand-built one in the GitLab repository, this worked."* **Nothing has ever
carried that sentence to that repository.** It lives in a comment on a closed
issue in this tracker; the workaround lives in a file over there; the two have
never met. So the one real adopter is, today, still working around a gap that
was closed seven versions ago — and the only reason anybody knows that is that
somebody happened to read two files at once while writing this spec.

**Because nobody is at fault, which is what makes it structural.** The issue
cannot know which repositories worked around it; the local file cannot know when
upstream shipped; the plugin cannot poll for its own past inadequacies. Every
party behaved correctly and the join still does not exist.

## The end value

The repository says what it is doing instead and what would end it, in the file
that already carries what is true about this repository — and a session that
goes to the tracker where that answer lives says so, instead of following the
workaround one more time in silence.

**How we would know it worked:** the journey's *A workaround outliving its
reason* row stops reading **nothing yet**. Concretely, in `wf-developer-agents`:
a `feedback` session there names the hand-built skill it is standing beside and
the issue that would end it, rather than that fact existing only in a comment
nobody in that repository will ever open.

## What changes

Two files, plus the feature file this spec commits and the case the
implementation writes. No `description` moves.

1. **[`method/process.md`](../../method/process.md) gains one section**, under
   *When the process gets in the way*, immediately after
   [*A step you cannot take here is said once, not searched for*](../../method/process.md#a-step-you-cannot-take-here-is-said-once-not-searched-for) —
   the same family, one step later. That section says what to do when a step
   cannot be taken here; this one says what to do when the work goes around it
   and keeps going.

   The shape of it: **a workaround is recorded where this repository's own facts
   live, and the record names what would end it.** What is done here instead,
   what gap it goes around, where that gap is filed, and the thing whose arrival
   makes the workaround removable. A row that cannot name what would end it is
   describing a decision rather than a workaround, and decisions do not expire.
   Then the half that is the actual gap: **a recorded workaround is never
   followed silently.** A session standing on one says so, and where it is
   already at the tracker that would answer it, says whether the answer has
   arrived. Portable — it names no command, no tool, no threshold, and no
   tracker.

   It also says the row is removed when the workaround is: a row outliving the
   thing it describes is the same failure one level up.

2. **`skills/feedback/SKILL.md` wires it,
   twice and briefly.** §0 already reads the bindings to find the tracker; it
   gains a sentence saying that those bindings may record a workaround, and that
   one bearing on the step in hand is named in the reply rather than followed
   quietly. §6 gains the write: where what was just filed is a mismatch this
   repository is going to carry on around, the row is stated in the reply and
   then written into the bindings. Both link to the method section rather than
   restating it.

   **`feedback` is the only skill wired**, and it is the one with the transcript:
   it filed `#10`, it is the skill `#10` was about, and it is the skill standing
   in the room at the one moment both halves of the join exist — the issue number
   it has just created, and the human saying the work will carry on locally.

3. **One new eval case**, written in the implementing change, claiming both
   rules: a consuming repository whose bindings already record one workaround,
   where somebody reports a second mismatch and says they will keep doing it
   their own way meanwhile. It holds the reply, not the file system: the row that
   is about to be written, and the recorded workaround being named rather than
   followed in silence.

**Rules added or changed** — the `@rule:` ids in `specs/features/`:

| Rule id | Feature file | New or changed |
|---|---|---|
| `a-workaround-records-what-would-end-it` | `features/fit/local-workaround.feature` | new |
| `a-recorded-workaround-is-not-followed-silently` | `features/fit/local-workaround.feature` | new |

Both are `@planned`, and the file — a new area, `fit/`, for where the process
meets a repository it does not fit — is committed with this spec.

**The journey moves in the implementing change.**
[`trusting-the-spec-again`](../journeys/trusting-the-spec-again.md)'s ownership
table currently reads *A workaround outliving its reason → **nothing yet***, and
the paragraph under it says the two remaining `nothing yet` rows are the same
moment. After this, one of them has an answer and the paragraph is wrong. Both
are amended, and the row reads **narrowed, not closed** — see *Risks*.

**Ledger:** nothing moves. No new gate, and nothing here can fail a build.

## What we are not doing

- **Not wiring `setup`'s ledger-diff, which is the obvious second reader and is
  deliberately left.** A workaround's reason can only vanish when the plugin
  moves, and the moment a repository learns the plugin moved is a `setup` re-run
  — which [already diffs what was recorded against what is true now](../../skills/setup/SKILL.md)
  and re-stamps the version. `#28` says as much. It is left out for two reasons
  and the weaker one is money: editing that body stales `09`, `11`, `12`, `16`
  and `17`, which last cost **$8.05** together at `runs: 3`, five-eighths of the
  whole board, against **$2.13** for the seven this change already stales. The
  stronger reason is that `setup` writes the bindings and does not yet have a
  reason to read a section it has never written; giving it one is a change to
  the re-run diff and wants its own evidence. **One skill, the one with the
  transcript** — the same line [`0018`](0018-said-once-not-searched-for.md) drew.

- **Not polling, and not a background anything.** `#28` rules this out itself and
  it is right: the plugin cannot poll for its own past inadequacies, and a check
  that runs when nobody is in the room is a check whose output nobody reads. The
  read happens where a session is already standing.

- **Not a second file.** The row goes in the bindings, beside the gate wiring
  ledger and the fault-injection record, which are already dated tables of what
  is true about this repository. [`0001`](0001-the-gate-wiring-ledger.md) argued
  the same thing down for the same reason: a second file is a second read, a link
  that can rot, and one more thing for a re-run to find.

- **Not a generated row, and not one derived from the tracker.** Same argument
  as the gate ledger: a record of a divergence cannot be produced by the
  automation the divergence exists because of. It is typed, and what stops it
  drifting is that it is read out loud in the session that follows it.

- **Not every divergence.** Considered and dropped: recording every deliberate
  departure from what the method says. That turns the bindings into a general
  outstanding-work list, which is a second thing to maintain — the exact thing
  the persona adopted this to stop having. The boundary is in the Gherkin: a gap
  nobody is carrying on around gets no row.

- **Not livespec-specific.** The method section says *a gap owned somewhere
  else* — a dependency, another team's tool, a plugin. A repository that never
  heard of livespec has these, and a method paragraph that names the plugin
  fails the line test on its first sentence.

- **Not backfilling this repository's own bindings.** livespec carries no
  workaround of this shape today — the `--strict` narrowing in
  [the bindings](../setup/README.md) is a permanent decision about where
  `CLAUDE.md` lives, not a gap waiting on somebody, and giving it a row would be
  the first invented entry in a table whose whole job is not to guess. A
  repository with no workarounds has no section, and that is the correct
  appearance.

- **Not telling `wf-developer-agents` anything.** This change makes the join
  writable; it does not reach into somebody else's repository and write it. What
  happens there is a `feedback` session run by its owner, which is where *How we
  would know it worked* points.

## Data

None. There is no storage contract — the plugin ships prose, and what a version
leaves behind is listed in [spec.md](../spec.md#what-a-version-leaves-behind).
This adds one thing a *consuming* repository may hold, in the same place
[`0001`](0001-the-gate-wiring-ledger.md) put the gate ledger: a table in its own
`specs/setup/README.md`. Repositories set up by an earlier livespec have no such
rows and nothing backdates them — a row is written the next time a workaround is
kept, and an invented one would be the first lie in the file that is supposed not
to guess.

## Risks

- **`never-implements`, and it is the promise to watch.** This is the first time
  `feedback` writes anything into `specs/`. The letter of the promise is not
  moved — [spec.md](../spec.md#the-promises-that-belong-to-no-single-workflow)
  says no skill touches *application code*, `setup` already writes this exact
  file, and a bindings row is not a fix. The spirit is worth stating anyway:
  what widens here is that a skill whose whole discipline is *file it, do not fix
  it* now edits a file in the repository. The narrowing is that the row **records
  a decision somebody else already made** — it does not make one, and it never
  touches the workaround itself. Written down because the next request to let
  `feedback` write "just one more small thing" will cite this change, and the
  answer to it is this paragraph.

- **The row said and never written.** §6 asks for the row in the reply first,
  which is the same shape as naming the repository before filing. If the session
  ends between the two, the join exists only in scrollback — the failure this
  change is about, one turn earlier. The case grades the reply and cannot see
  this; a human reading the diff can.

- **The rig cannot hold the half that matters most.**
  [`evals/README.md`](../../evals/README.md) makes *no case grants `Bash`* a
  floor, so no case can ask a tracker whether an issue is closed. What the new
  case can hold is the reply — the row about to be written, the recorded
  workaround named rather than followed silently, and the hand-over where the
  tracker cannot be reached. **The example where the reason has actually gone is
  held by nobody here**, and it is the one the end value rests on. That is the
  same shape as
  [`the-sitting-ends-by-using-the-pipeline`](../features/setup/demonstration.feature),
  and it is why the rule is written as *never followed silently* rather than as
  *checks the tracker*: the promise is at the altitude the rig can reach, and the
  check is the means. Softening it further until a sandbox could pass the whole
  thing would buy the tag with the dishonesty `evals/README.md` warns about.

- **A row that becomes wallpaper.** A workaround named in every reply forever is
  a warning that survived two versions, which
  [`gates.md`](../../method/gates.md#what-is-wired-and-what-is-not) already has a
  norm about. The mitigation is that it costs one sentence and no round trip, and
  that the row is deleted with the workaround. If it starts reading as noise, the
  fix is that the workaround should have come out.

- **The seam is narrowed, not closed, and the journey has to say so.** After this,
  a repository that records the row and runs a session that reaches the tracker
  finds out. A repository that records nothing, or never runs such a session,
  is exactly where it was. The ownership row moves to naming what answers it
  today; it does not get to claim the outcome, because the outcome is a local
  patch actually disappearing and nobody has watched one do that yet.

- **`ids-are-permanent`.** Two new ids ship and can never be renamed. Neither
  names `feedback` and neither names livespec, so pointing `setup` — or any other
  skill — at the same method section later does not orphan them.

## Acceptance checks

1. `python3 .github/scripts/verify.py` green, and the always-on cost `checks.py`
   reports **unchanged at 3800 across 7 skills**. This change touches no
   `description`; a move there means a sentence went into the wrong file.
2. Read the new `method/process.md` section against the line test — *could this
   survive a repository with pytest and a Makefile?* It must name no command, no
   tool, no threshold and no tracker. The word "livespec" appearing in it is a
   failure.
3. In a repository whose bindings record a workaround naming a filed gap, report
   something. The reply names that workaround and what would end it, once, before
   acting on it.
4. Same repository, where the tracker is reachable and the gap it names is
   closed: the reply says the reason has gone and what can stop being carried.
5. In a repository that records no workaround, report something. Nothing about
   workarounds appears in the reply — the sentence must be conditional on a row
   existing, not a new paragraph everybody pays for.
6. Read `feedback` §0 and §6 back after the edit. §0 must still resolve the
   repository and the tracker first; §6 must still end at *then stop*.
7. **The real check is in the other repository.** Run `feedback` in
   `wf-developer-agents` and see whether the reply reaches the fact that
   [`#10`](https://github.com/sargismarkosyan/livespec/issues/10) shipped in
   0.11.0. That is the acceptance test its close comment named and nobody has
   ever run.
8. **The measurement, and it costs money.** Editing `skills/feedback/SKILL.md`
   stales every case tagged `skill:feedback` — `02`, `13`, `14`, `15`, `18`,
   `19`, `20` — plus the new case's first entry. `verify.py` stays red until
   `run.py --changed` re-measures exactly those. **Priced off the board's own
   recorded costs:** those seven last cost **$2.13** together, measured on
   2026-08-26 at `runs: 1`, against **$13.46** for all twenty — so a like-for-like
   re-measure is about a sixth of the board, and a `runs: 3` one roughly three
   times that. **The implementing change stops and asks before spending it**, and
   the flag is the maintainer's signature. The number goes in the pull request,
   and the commit can be finished with a gap where it goes.

   `CLAUDE.md` still says *"about $1.80 for one case, ~$4 for the suite"* and the
   board still disagrees with both, as [`0018`](0018-said-once-not-searched-for.md)
   recorded. Do not price a run off that sentence.

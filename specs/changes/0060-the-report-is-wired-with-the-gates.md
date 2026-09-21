# Spec 0060: the report is wired with the gates, in the platform's own words

- **Status:** proposed
- **Issue:** [#141](https://github.com/sargismarkosyan/livespec/issues/141) —
  `setup` on a self-hosted GitLab wired the gates and never the merge-request
  report: three graders on the first whole sitting the suite produced
  (`evals/results/20260919-014104`, case `12`, plugin arm, `claude-sonnet-5`,
  one run), read verdict by verdict against the files it wrote.
- **Depends on:** [`0058`](0058-a-case-is-a-sitting-not-a-turn.md), which gave
  the case the person and the shell without which this sitting never got past
  its six questions; and the sitting of 2026-09-20, which measures the skill
  as it is at the floor, so the number before this change exists.

## Who this is for

[`agent-accelerated-owner`](../personas/agent-accelerated-owner.md), in
[`adopt-the-process`](../workflows/adopt-the-process.feature), at the end of
the sitting — the step where the wiring is on trial and the pull request is
where they check, because *"checking the result by reading is not available."*
The fixture's owner answered six questions and said *go* twice, and got the
gates in her pipeline, a hook, bindings, a rewritten CLAUDE.md and the start of
a persona interview. What she did not get was a report on her merge requests,
which is the one thing in the loop that reaches the person deciding whether to
merge, and the thing the method calls the reason the pipeline exists.

**This lengthens nothing anybody types.** It moves a paragraph and gives it a
heading. No always-promise moves; the description does not move.

## The job behind the request

The literal ask is the issue's: the report step written in both platforms'
vocabulary, and the order of the sitting looked at. Behind it is where the
instruction sits.

[`skills/setup/SKILL.md`](../../skills/setup/SKILL.md) §4, *Wire the gates*,
is a sequence of things to build, each under its own heading or bold lead:
the traceability gate, the rule binding, coverage taken twice, one command,
the runner's per-test report — then *offer to run it before the push*, *make
the real thing reachable*, *break them, one at a time*. The report is none of
those. It is a paragraph inside §5, *Write the bindings*, between the
template and the tracker row: *Wire the report too, and say so when you
cannot.* A sitting reads §4 as the list of things to wire and §5 as the file
to write, and a thing to wire filed under the file to write is read as a
sentence about the file. The transcript of 2026-09-19 shows exactly that:
bindings written from the template, CLAUDE.md audited and rewritten,
`.gitlab-ci.yml` made to run `make test`, the hook offered and accepted, the
persona interview begun — and no mention of a report across 132 turns, in
either direction. The judge, three graders: *never wired, nor even mentioned*.

Two smaller things sit beside it. The paragraph says *a comment on its pull
requests*, and the repository has merge requests; *cannot fail the build* is
`allow_failure` there, not `continue-on-error`. Nothing in the paragraph is
wrong on GitLab and nothing in it is in GitLab's words, and a sitting that has
to translate has one more step than one that can copy. And the order: the
hook is a question — *then stop and let them answer* — and the interviews
are three more; a sitting that runs out of rounds runs out after a question,
so whatever is placed after the hook offer is the first thing lost. The report
is wiring, not a question, and belongs with the wiring.

The job: **the report is the last gate-shaped thing the sitting wires, under
its own heading in §4, in the words of the platform in front of it, before
anything that waits on the person.**

## Why now

The first Sonnet sitting at the floor is running as this is written, on the
skill as it is; the three plugin sessions on `12` are the before. This lands
after it, so the after is one change and the difference is this one.

## The end value

A setup sitting on GitHub leaves a job after the gates, `continue-on-error:
true`, that comments on the pull request with the token the workflow already
has; on GitLab, a job with `allow_failure: true` that posts a merge-request
note through the API with the job token; on anything else, the platform's own
equivalent — and the `wiring:pr-report` row names which. Where a pull request
cannot carry a comment at all, the hand-back says the report is not wired and
why, and nothing claims it was.

**How we would know it worked:** `12`'s three report graders —
`wires-the-report`, `report-cannot-gate`, `report-says-what-moved` — pass in
the plugin arm of the sitting after this lands, having read 0 of 1 on
2026-09-19 and whatever the sitting of 2026-09-20 reads at the floor.

## What changes

1. **[`skills/setup/SKILL.md`](../../skills/setup/SKILL.md) §4** gains a
   subsection, *Then wire the report, and make it unable to fail the build*,
   between the runner's per-test paragraph and *Then offer to run it before
   the push*. It says what the report is — what the change did to the spec
   layer, read from the traceability gate's own output rather than worked out
   again, placed where somebody deciding whether to merge is already looking
   ([`gates.md`](../../method/gates.md#the-report-is-not-a-gate)); that it
   runs after both gates and must not be able to fail the build, not on a
   missing token and not on its own errors; and how that is spelled on the
   platform in front of it: on GitHub Actions a job with `continue-on-error:
   true` posting a comment on the pull request, on GitLab CI a job with
   `allow_failure: true` posting a merge-request note through the API with the
   job token, and on anything else the equivalent, named in the bindings' row.
   Where the repository's pull requests cannot carry a comment, the hand-back
   says the report is not wired and why. And one sentence on the order: it is
   wired before the hook is offered, because the hook is a question and the
   report is not.
2. **§5**: the paragraph *Wire the report too, and say so when you cannot*
   becomes one sentence — the `wiring:pr-report` row names the job §4 wired,
   or says why there is none — so a reader of §5 still finds it.
3. **Nothing else.** The second finding in #141 — the runner gate's marker
   half — is already the skill's own sentence in the per-test paragraph and a
   fault the injection table asks for; the sitting never reached *break them,
   one at a time*, where a gate that reads counts and not markers is caught,
   and the order above is what gets a sitting there.

**Rules changed: none.** The three rules `12` claims for the report already
say what the sitting must leave behind; this changes where the skill says how.
`skills/` moves, so the change ships: **`patch`**, and the description does
not move.

## What we are not doing

- **Not a GitLab branch of the skill.** One subsection, two lines of vocabulary.
- **Not raising `12`'s rounds or turns.** The case bounds the sitting at three
  replies and a hundred turns a round; the skill should reach the report
  inside that, and whether it does is exactly what the case measures.
- **Not the runner gate's marker half** — see *What changes*, 3.
- **Not re-measuring anything here.**

## Data

No storage. Files that move: `skills/setup/SKILL.md`, and this spec.

**This spec commit stales nothing.** `verify.py` exits **2** for the rows the
sitting of 2026-09-20 is healing and no other reason.

**The implementing change stales the fourteen `setup` cases**, through the
skill body in their inputs hash — and lands after the sitting has measured
them, so that the before exists. `--changed` then selects exactly those.

**What the pull request owes.** `patch`, a `## Changelog` section. No Gherkin
block: no `.feature` moves. No run block: nothing under `tests/`, `evals/` or
`.github/scripts/` moves. The audit surface does not move.

## Risks

- **A reader of §5 loses the report.** The sentence left behind points at
  §4's heading by name.
- **The platform words go stale.** Two names, both current; a third platform
  is *the equivalent, named in the row*, which is what the rule already asks.
- **The sitting still runs out before it.** Then the case says so at the
  floor, and the next reading is of the turn budget, not the skill.
- **Always-promises.** `never-implements`: the job posts a comment; no
  application code. `always-green`: unchanged. `context-budget`: no
  description moves.

## Acceptance checks

1. §4 carries the heading and §5 carries the one sentence; `verify.py` exits 2
   for the board only, the setup cases re-staled.
2. In the first sitting after this lands, `12`'s plugin arm leaves a job with
   `allow_failure: true` after the gates in `.gitlab-ci.yml`, and the three
   report graders pass at the floor.
3. The pull request carries `patch` and `## Changelog`.

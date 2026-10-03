# Spec 0069: the reading is played back before the file exists

- **Status:** approved
- **Issue:** [#158](https://github.com/sargismarkosyan/livespec/issues/158)

## Who this is for

The person being interviewed by `refine-journeys`, `refine-personas` or
`refine-workflows` — the only one who knows whether the conclusion drawn from
their answers is wrong. Sits in `adopt-the-process`, at the round where a
sitting turns answers into a file.

## The job behind the request

They answer four questions about their own life. What goes in the file is not
those answers, it is what the session concluded from them, and a conclusion is
exactly the thing they can correct and the session cannot. Played back before
the file exists, one paragraph costs nothing and can be argued with. Played
back afterwards, it is a summary of a decision already taken.

## Why now

Two eval suites caught the same failure a week apart, in two skills that carry
the instruction in the same words.

`55-nobody-has-written-down-who-it-is-for`, plugin arm, 2026-09-26: *"The
persona file was written before any playback occurred… only after all of that
does it deliver the playback paragraph."* Δ **+0.00** — the bare model did the
same thing, so the skill added nothing.

`49-a-journey-that-became-a-table`, plugin arm, two runs of three, 2026-09-25:
the arc rewritten without anybody being asked about a season.

**The cause is in the files, not in the model.** Each skill says it twice, in
two very different voices:

| where | how it reads |
|---|---|
| §1, one bullet in a list of interview rules | *Play the arc back in one paragraph before writing anything* |
| §6/§7, bolded, its own paragraph | **Show the journey diff by itself, first** — *ask for that alone, in one plain line* |

Both are "show them something and ask before going further". One is a bullet
among eight; the other is bold, structurally separate, and attached to the
deliverable. A sitting under pressure keeps the vivid one and reads the buried
one as describing it. That is not a model being careless — it is two
instructions of the same shape where only one looks load-bearing.

## The end value

The person gets the conclusion while it is still a sentence. The two showings
stop being confusable, because they are no longer the same shape: one is a
paragraph about what was understood, before any file; the other is a diff of
what was written.

**How we would know it worked:** `48`, `49`, `55` and `59` are the cases that
would notice — each grades a playback before the write, and each currently
reads the skill doing it afterwards or not at all.

## What changes

A method rule, and the same structural correction in all three interview
skills:

- **The playback gets its own step.** It stops being a bullet inside the
  interview rules and becomes a short numbered step of its own, between the
  interview and the writing, so that skipping it means skipping a step rather
  than missing a line.
- **The two showings get different names.** The one before the file is **the
  reading** — a paragraph in the session's own words about what the answers
  mean. The one at hand-back stays **the diff**. A session cannot collapse two
  things it has to call by different names.
- **The hand-back says the diff does not discharge the reading.** One line, at
  the point of temptation: if the reading has not been played back and
  corrected, the sitting is not ready to show a diff.
- **The method carries the principle**, in `process.md`'s rules, beside the
  rule that a personas or workflows diff is confirmed on its own — which is
  the same argument one layer along, and which is why the two were confusable
  in the first place.

## What we are not doing

- **Not adding a gate.** Nothing here is checkable from the tree; a sitting
  that skipped a conversational step leaves no trace a script could read. The
  eval cases are the check, which is what they are for.
- **Not touching `refine-spec`.** It asks its questions in one batch and does
  not draw a conclusion about a person, so it has no reading to play back —
  its §4 already says the questions come before the spec and approval is never
  folded in.
- **Not changing any description.** The always-on cost is unchanged; this is
  body text in three skills that already load.

## Data

None.

## Risks

Three more lines in three skills that are already long, against a failure mode
that has cost four cases their score. The mitigation is that the added step is
short and replaces text rather than only adding it.

The board goes stale for every case holding these three skills, which is the
ordinary consequence of editing a skill body and is what the freshness gate is
for.

## Acceptance checks

1. Each of the three skills has a numbered step between the interview and the
   writing whose subject is the reading.
2. Each hand-back section says the diff does not stand in for it.
3. `python3 .github/scripts/verify.py` is green but for the board.

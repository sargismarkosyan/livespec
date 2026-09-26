# Spec 0068: a person who never answered is not a score

- **Status:** approved
- **Issue:** [#159](https://github.com/sargismarkosyan/livespec/issues/159)

## Who this is for

The maintainer, reading a number off the board and deciding whether a skill is
getting better or worse. Serves no workflow: this is the measuring apparatus
rather than the method, in the documented sense of a technical change that
serves nobody and says so.

## The job behind the request

A case that brings a person is a sitting, and the sitting is what is being
measured. When the judge standing in for that person returns nothing three
times, the sitting stops mid-round — the session has asked its questions and
will never get an answer. Every grader that then looks for a written file
finds none, and scores zero.

Nothing in the row says that happened. The number reads as a skill that asked
four good questions and then produced nothing, which is the opposite of what
the transcript shows.

## Why now

The floor run of 2026-09-25 hit it on `48-a-persona-with-no-journey`. The
plugin arm had asked its four retrospective questions and promised to play the
arc back; the next line in the transcript is

```
{"type": "person", "round": 1, "error": "Expecting value: line 1 column 1 (char 0)"}
```

Three graders scored zero against that session and the arm read **0.80**
instead of 1.00. The case's Δ was reported as +0.33 when the sittings that
actually happened say +0.53.

[`0058`](0058-a-case-is-a-sitting-not-a-turn.md) settled exactly this at the
other end of the sitting: a judge that returns nothing three times is not a
verdict, is left out of the fraction, and is "never read as the agent failing
the rubric". The same reasoning had not been applied to the person.

## The end value

A row says what the sittings said. A session the harness cut short is not
mistaken for a session the skill fumbled, and it is not silently dropped
either — it is named, counted, and can be run again.

**How we would know it worked:** a run whose person fails prints a line naming
the case, that session is absent from the arm's mean rather than sitting in it
as a zero, and `--resume` performs it.

## What changes

- A person round that errors for any reason other than the account's limit
  ends the sitting as a **harness failure**, the way a timeout already does.
  The session returns an error carrying `person_unreachable`, and its
  workspace and transcript are kept as evidence.
- The session is therefore not scored. It does not enter either arm's mean,
  and it cannot be read as a zero.
- `owed()` counts it as a session the run still lacks, so `--resume` runs it
  again — a resume is for what the limit or the kill took, and this is the
  same kind of loss rather than a second try at a measurement.
- The summary prints it apart from other session errors:
  `⚠ <case>: n sitting(s) lost the person`, with what to do about it.

## What we are not doing

- **Not retrying inside the round.** `_person` already makes three attempts
  five seconds apart; a fourth in the same place is not the missing piece.
- **Not scoring the session partially.** A sitting stopped at round one may
  still have written something, and grading whatever survives would make the
  number depend on where the harness happened to fail.
- **Not touching the limit path.** The account saying no is already handled
  and already resumable.

## Data

None. Existing board rows are untouched by this spec; they go stale because
the harness fingerprint moved, which is the ordinary consequence of editing
`provider.py` or `asserts.py` and is what the board gate is for.

## Risks

A case whose person fails repeatedly now yields fewer scored sessions rather
than low ones, so it can fall below the floor of three and be reported as not
measured. That is the honest outcome — it says there are not three good
sittings yet — but it will look like a case losing coverage, and the summary
line is what stops that being mysterious.

## Acceptance checks

1. A run whose person errors prints the `lost the person` line naming the case.
2. That session's `session.json` carries `person_unreachable`, and its
   transcript and workspace are under the session directory.
3. The arm's mean over the remaining sittings excludes it.
4. `--resume` on the run directory performs that session again.

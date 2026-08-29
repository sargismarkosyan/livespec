# Graded cases

You are on this page because [testing.md](testing.md#first-what-proves-a-rule-is-true-here)
forked and the repository took the second branch: the product is **judgment**
rather than code, there is no function to call, and behaviour is proved by
running the thing against a situation and grading what came out.

That page says a graded case proves a weaker thing than a test. This one says how
to keep it from proving nothing at all. Each section below is a lesson that cost
somebody an afternoon; each is written as a decision rather than a description,
because the reason is the part that travels.

**Nothing here names a runner, a grader format or a threshold.** Those are
bindings, and the repository writes its own down. The test for every sentence on
this page: does it survive a repository whose runner is not the one you are
thinking of?

## The session is part of what you measure

A graded case runs the product inside a session, and **a session inherits things
nobody chose for it** — the operator's own configuration, whatever tools the
machine has connected, and the context of the directory it happens to start in.
Each of those changes the answer. None of them is the product.

So the sessions a case runs in are **hermetic**, and made so deliberately: the
operator's settings do not reach them, the machine's connected tools do not reach
them, and the workspace is one the case laid down rather than the one you were
standing in.

**The failure mode is what makes this worth a section.** A leaked environment
does not announce itself. It produces a plausible bad score, and a plausible bad
score gets diagnosed as a defect in the product — so the first day is spent
fixing something that was never broken. Every hour of that is spent before
anybody suspects the harness, because the harness is the one part nobody thought
was under test.

**A case that needs a repository must build one.** Running against an empty
workspace measures the hunt for missing files, not the judgment. If a case
asserts a repository — its layout, its history, a file that is deliberately
absent — the case lays that down itself, identically for every arm, or it is
measuring the wrong thing in all of them.

## One arm cannot tell you anything

The thing being graded is **context that loads whether or not it is used**. So
the only honest question is not *did it do well* but *did it do better than the
same model with none of this*, and answering it takes **two arms**: one with the
context present, one without, on the same prompt and the same graders.

A single-arm score cannot separate what your instructions did from what the model
was going to do anyway. It will be high, because models are capable, and it will
be high whether the context helped, did nothing, or actively got in the way — a
number that reads the same in all three cases is not a measurement.

**The difference between the arms is the only number worth keeping.** It can come
out negative, and when it does the finding is real: the context made the answer
worse. That is the most valuable thing this arrangement produces and the main
reason to build it.

### Firing is reported, never scored

Whether the context fired is worth knowing and must not enter the score.

A grader that rewards firing rewards it in exactly one arm — the arm where the
thing exists — so it awards a point for existing rather than for helping. Do that
and the difference between arms inflates on its own, without any answer having
improved. It is the most natural mistake to make and the hardest to see
afterwards, because the number moves in the direction you were hoping for.

So firing is an **indicator**: recorded, shown next to the score, and weightless.
Judge the answer that came out.

## The judge is not the thing being judged

Grading is a separate job from answering, and it goes to a separate model, held
to a **fixed shape of reply**.

Two reasons, and the second is the one people skip. A model asked to grade freely
writes prose, and prose has to be parsed by somebody later — the parser is where
the drift gets in. And a model asked to grade its own kind of work grades
generously; the closer the judge is to the thing under test, the more the
measurement becomes a conversation with itself.

**Every case carries at least one grader that reads the answer**, not just
graders that check whether machinery moved. A suite where everything is
structural will pass a product that has quietly stopped being useful, which is
the failure the suite existed to catch.

**When a rubric and a verdict disagree, read the transcript before touching
either.** The rubric is usually right and the answer usually deserved to fail. A
rubric edited because a run came back badly is a rubric being fitted to a result,
and it can only be done once before the number means nothing.

## Freshness is gated; the score never is

A measurement describes the files it measured. Edit any of them — the case, the
rule it claims, the instructions it holds — and the number goes on being
displayed while no longer describing anything that exists.

So each measurement carries a **fingerprint of what it measured**, and a stale
fingerprint is a failure. What must **never** be gated is the score itself.

That asymmetry is deliberate and it is the whole design:

- **gate the bookkeeping** — a number that no longer describes the tree is a lie,
  and lies are cheap to detect;
- **never gate the number** — a threshold on a model-scored value turns every
  rubric into something to be argued down on a bad afternoon, and the first time
  a release is blocked by a judge's opinion is the last time the rubric is
  written honestly.

**Re-run exactly what changed.** These runs cost money in a way tests do not, so
re-measuring the whole suite because one file moved is a bill nobody agreed to.
The fingerprint already says which cases moved; measure those.

**And the run itself is never automatic.** A suite that costs money every time it
executes must refuse to start without an explicit approval from the person paying
— not a setting, not a default, an approval given per run. A stale measurement is
a reason to stop and ask, never a licence to spend. Say which cases went stale
and what it will cost, and wait; the work can be finished with a gap where the
numbers go.

**So a stale measurement is the one red a commit may carry**, and the page about
committing is where that is written down rather than left to be inferred from
here: [repository.md](repository.md#commits) states the exception, the three
conditions on it, and the fact that it ends at the push. What belongs on this page
is the consequence of the design above. Gating the bookkeeping deliberately
creates a **failure that is not a defect**, and it is the only one this method
has.

**A failure that is not a defect has to say so.** Verification that can be red for
a reason this page sanctions must make the two distinguishable **in its result** —
in what a machine reads, and in the last line a person reads — not only in prose
addressed to whoever remembers this page. How is the repository's own business: a
separate exit status, a distinct final line, the check reported apart from the
rest. That there is one is not.

**Skipping it costs the gate, not the afternoon.** A red meaning *a number is
waiting on an approval* that looks exactly like a red meaning *something is
broken* gets investigated the first two or three times, found innocent every time,
and then stops being investigated at all. The gate is still running and nobody is
reading it — which is worse than never having wired it, because it still counts as
coverage to everybody looking at the list.

**The same rule reaches whatever else describes the build.** A report skipped when
verification fails cannot describe the one failure the method sanctions;
[gates.md](gates.md#the-report-is-not-a-gate) says why that is a defect in the
report rather than a property of reports.

## The evidence is local, the summary is durable

A run produces far more than a score: full transcripts, every graded verdict, the
workspace each session built. That evidence is **large, and it is the only thing
that can settle an argument about a number** — so keep it, and keep it out of the
repository's history.

What is committed is the **summary**: per case, the arms, the difference, when,
against which commit, and the fingerprint. One line each, durable, diffable, and
enough to see a product getting better or worse over months.

**The distinction is not tidiness.** Transcripts committed become a repository
nobody can clone; transcripts discarded leave a number with nothing behind it,
and the first time somebody disputes it there is no way to look.

## What this page does not settle

**What a difference between arms actually means.** Whether a small positive
result is a real improvement or noise, how many runs it takes to tell, and what
size of change is worth acting on — none of that is answered here, because it is
not known. It depends on the judge, the rubric and how much the prompt varies.

Treat an early number as a direction rather than a fact, run more times before
believing a small one, and **read the verdicts** — a score nobody has read the
reasoning behind is a number in search of a meaning. A repository that writes
down what it does not yet know about its own measurements is in better shape than
one that quietly picks a threshold.

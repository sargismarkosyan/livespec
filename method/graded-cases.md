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

**A case of something that asks must bring the answers.** A product that
interviews — that says what it would do and waits, or asks the six things only
the person knows — measured over one turn, measures its first question and
nothing after it, and does so in every arm alike, so the difference reads as
zero on exactly the cases where the product's judgment lives. Give the case the
person it would have had: what they know, in their voice, answering only from
that and only when asked, for a bounded number of turns, the same in every arm.
Keep what they said beside what the product said, because the judge has to read
both. And the sheet answers; it never volunteers — a fact the product never
asked for never reaches it, or the case stops grading whether it asks.

**The tools the product runs are part of the room.** A product whose first move
is a command, measured in a session that refuses commands, measures the
refusal. A case that lends a tool says which, confines it to the fixture, and
names what the machine must have for the fixture to run — and refuses to
measure when it has not, rather than measure the absence.

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

**When the judge is the model under test, the arms are what save the number.**
Sometimes the only judge large enough to read the nuance is the model being
graded, or the only one worth paying for. Then the same eyes read both arms,
and what the judge prefers in its own kind lands on both sides of the
difference — bounded by the comparison, not removed by it. Say so where the
decision is made, and read the verdicts against that assumption: a judge found
favouring one arm's voice is a finding the calibration read exists to make,
and the day to pay for a different judge.

## Neither freshness nor the score is gated

A measurement describes the files it measured. Edit any of them — the case, the
rule it claims, the instructions it holds — and the number goes on being
displayed while no longer describing anything that exists.

So each measurement carries a **fingerprint of what it measured**, and a number
whose fingerprint no longer matches is **shown as stale** and left out of every
count and mean: it is never presented as current. That is the whole of what is
enforced. Neither half is gated:

- **not the number** — a threshold on a model-scored value turns every rubric
  into something to be argued down on a bad afternoon, and the first time a
  release is blocked by a judge's opinion is the last time the rubric is written
  honestly;
- **not its freshness** — a run costs money, so a gate on freshness turns every
  edit into a bill, and a change nobody can merge without paying is one that gets
  walked past. A run happens when the person paying chooses, and a stale number
  ages in plain view until then.

**Re-run exactly what changed.** When a run does happen, the fingerprint already
says which cases moved; measure those, not the whole suite.

### Measure at two speeds

The most faithful measurement — the whole session, in its world, with the person
answering and the tools lent — is also the most expensive. So measure at **two
speeds**. A **cheap tier**: a single turn to see whether the right instructions
load at all, a single reply to a snapshot of what the session would have read
before answering, a reading of the instructions beside the rules they owe. Each
is fingerprinted by **only what it can see** — a routing turn never sees a
skill's body, so a body edit cannot stale it. A **faithful tier** — the whole
sitting — is run when the model moves, before a cheap tier is trusted, or when
somebody chooses to.

**A cheap tier earns its trust against the faithful one.** Run the same cases
both ways and believe the cheap number where the verdicts agree. Where it cannot
see — the later turns, the files written, the commands run — say so wherever its
numbers are read, and let a rubric that only those could decide be marked as not
applying rather than failed: a failure the tier could never have avoided is the
tier's blind spot scored as the product's fault.

**And the sessions already had.** A product used for real leaves its own record,
and it is the one evidence nobody has to pay to produce. Grade those sessions
against the rules the product owes — the grading is the only spend — and keep
them local, because they are somebody's real work. They never go on the board: a
board row describes the files as they stand, and a real session describes the
files as they stood the day it happened.

**And the run itself is never automatic.** A suite that costs money every time it
executes must refuse to start without an explicit approval from the person paying
— not a setting, not a default, an approval given per run. A stale measurement is
never a licence to spend: say which cases went stale and what a run would cost,
and leave the choice to whoever pays.

## The evidence is local, the summary is durable

A run produces far more than a score: full transcripts, every graded verdict, the
workspace each session built. That evidence is **large, and it is the only thing
that can settle an argument about a number** — so keep it, and keep it out of the
repository's history.

What is committed is the **summary**: per case, the arms, the difference, when,
against which commit, how many runs produced it, and the fingerprint. One line
each, durable, diffable, and enough to see a product getting better or worse
over months.

**The distinction is not tidiness.** Transcripts committed become a repository
nobody can clone; transcripts discarded leave a number with nothing behind it,
and the first time somebody disputes it there is no way to look.

### A run below the floor does not take a measurement's row

How many runs a number needs before anybody believes it is not settled here —
see below — and the repository picks its own floor. What *is* settled is what
happens once it has picked one.

Pilots are worth running: a short run exists so the verdicts can be read before
anybody pays for a full one, and reading them is the point of it. But a pilot of
a case that has already been measured produces a second number for the same row,
and **the measurement keeps the row.** Not out of deference to the older number.
The row is also what says whether a number is current, so a pilot written into
it does two things in one write: the measurement is gone, and the row reads
fresh — at the exact moment a real run became most necessary. Both halves are
silent, and the sign can flip on the way through.

So **the summary says how many runs produced it, and everything reading the
summary reads that field too.** A number below the floor is kept and shown — it
is the best the board has, and deleting it would only put the row back to empty
— but it is not counted as coverage, it stays out of any average, and it never
overwrites a number above the floor. A board that cannot tell the two apart
publishes its own variance as a result, in whichever direction the last pilot
happened to fall.

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

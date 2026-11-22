# Graded cases

For a repository that took the second answer in
[testing.md](testing.md#first-what-proves-a-rule-is-true-here): the product is
**judgment**, there is no function to call, and behaviour is proved by running
it against a situation and grading what came out. A graded case proves less than
a test; this page is how to keep it from proving nothing.

*From: every promise is checked by something that can fail.* **Nothing here names
a runner, a grader format or a threshold** — those are bindings. Every sentence
must survive a repository whose runner is not the one you are thinking of.

## The session is part of what you measure

A session inherits what nobody chose for it — the operator's configuration, the
machine's connected tools, the directory it starts in — and each changes the
answer without being the product. A leaked environment gives a plausible bad
score that gets diagnosed as a defect in the product. So:

- **Sessions are hermetic**: the operator's settings and the machine's tools do
  not reach them, and the workspace is one the case laid down.
- **A case that needs a repository builds one**, identically for every arm — its
  layout, its history, a file deliberately absent. An empty workspace measures
  the hunt for missing files.
- **A case of something that asks brings the answers.** Measured over one turn,
  a product that interviews is measured on its first question only, in every arm
  alike, so the difference reads zero exactly where its judgment lives. Give the
  case the person: what they know, in their voice, answering only when asked and
  only from that, for a bounded number of turns, the same in every arm. Keep what
  they said beside what the product said for the judge. The sheet answers; it
  never volunteers.
- **The tools the product runs are part of the room.** A case that lends a tool
  says which, confines it to the fixture, names what the machine must have — and
  refuses to measure when it has not, rather than measure the absence.

## One arm cannot tell you anything

The thing graded is **context that loads whether or not it is used**, so the
question is whether it did better than the same model without it: **two arms**,
with and without, on the same prompt and graders. A single-arm score is high
whether the context helped, did nothing or got in the way.

**The difference between the arms is the only number worth keeping.** It can be
negative, and then the finding is real: the context made the answer worse.

### Firing is reported, never scored

Whether the context fired is shown next to the score and weighs nothing. A grader
that rewards firing rewards it only in the arm where the thing exists, so it
inflates the difference without any answer improving.

## The judge is not the thing being judged

Grading goes to a separate model, held to a **fixed shape of reply**: free prose
has to be parsed later, and a model grading its own kind of work grades
generously.

- **Every case carries at least one grader that reads the answer**, not only
  graders that check machinery moved; an all-structural suite passes a product
  that stopped being useful.
- **When a rubric and a verdict disagree, read the transcript before touching
  either.** A rubric edited because a run came back badly is fitted to a result,
  and that can be done once before the number means nothing.
- **When the judge is the model under test, the arms bound the bias**: the same
  eyes read both, so what it prefers in its own kind lands on both sides. Say so
  where the decision is made, and a judge found favouring one arm's voice is the
  day to pay for a different one.

## Neither freshness nor the score is gated

Each measurement carries a **fingerprint of what it measured** — the case, the
rules it claims, the instructions it holds. A number whose fingerprint no longer
matches is **shown as stale** and left out of every count and mean, never
presented as current. That is all that is enforced:

- **not the number** — a threshold on a model-scored value turns every rubric
  into something argued down on a bad afternoon;
- **not its freshness** — a run costs money, and a change nobody can merge
  without paying gets walked past. A stale number ages in plain view until the
  person paying chooses a run.

**Re-run exactly what changed**: the fingerprint says which cases moved.

**The run itself is never automatic.** A suite that costs money per run refuses
to start without an approval from the person paying, given per run — not a
setting, not a default. A stale number is never a licence to spend: say which
cases went stale and what a run would cost, and leave the choice to whoever pays.

### Measure at two speeds

The faithful measurement — the whole sitting, in its world, with the person
answering and the tools lent — is also the most expensive.

- **A cheap tier**: one turn to see whether the right instructions load, one
  reply to a snapshot of what the session would have read, a reading of the
  instructions beside the rules they owe. Each is fingerprinted by **only what it
  can see**, so a body edit cannot stale a routing turn.
- **A faithful tier**, run when the model moves, before a cheap tier is trusted,
  or when somebody chooses.
- **A cheap tier earns its trust against the faithful one**: believe it where the
  verdicts agree. Where it cannot see — later turns, files written, commands run
  — say so wherever its numbers are read, and mark a rubric only those could
  decide as not applying rather than failed.
- **Sessions already had** are evidence nobody pays to produce: grade them
  against the rules the product owes, keep them local because they are
  somebody's work, and never put them on the board — they describe the files as
  they stood that day.

## The evidence is local, the summary is durable

The evidence — transcripts, verdicts, workspaces — is large and the only thing
that settles an argument about a number: keep it, outside the repository's
history. What is committed is the **summary**: per case, the arms, the
difference, when, against which commit, how many runs, and the fingerprint — one
line each. Committed transcripts make a repository nobody can clone; discarded
ones leave a number nobody can check.

### A run below the floor does not take a measurement's row

The repository picks how many runs a number needs. Once it has, **a measurement
keeps its row against a pilot**: written into the row, a pilot would erase the
measurement and make the row read fresh at the moment a real run became most
necessary. So the summary says how many runs produced it, and everything reading
it reads that too. A number below the floor is kept and shown, but not counted,
not averaged, and never written over a number above the floor.

## What this page does not settle

**What a difference between arms means** — whether a small positive is real,
how many runs tell, what size is worth acting on — is not known here; it depends
on the judge, the rubric and how much the prompt varies. Treat an early number as
a direction, run more before believing a small one, and **read the verdicts**. A
repository that writes down what it does not yet know about its measurements is
in better shape than one that quietly picks a threshold.

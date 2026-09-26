# Spec 0070: half a row goes stale, not a whole one

- **Status:** approved
- **Issue:** none — the maintainer, on being handed the bill

## Who this is for

The maintainer, who has to keep 70 cases measured on their own money. Serves
no workflow: this is the measuring apparatus, and it says so.

## The job behind the request

*"Running this evals is extremely expensive, we will not be able to maintain
them this way."*

The suite is not too expensive because a session costs too much. It is too
expensive because **the commonest change in this repository re-measures twice
what it needs to.**

Edit one skill and every case holding it goes stale — both arms. But the bare
arm runs `claude -p` with no `--plugin-dir`. No skill body is in its context.
A skill rewritten top to bottom cannot change one token of what the bare arm
did, and re-running it buys a number that was already true.

## Why now

Measured, from the floor run of 2026-09-25 and the pilot of 2026-09-26:

| | |
|---|---|
| sessions | $0.36 each |
| a judge call | $0.104 each |
| a person round | $0.057 each |
| judge share of a run's bill | 41–47% |

At 70 cases the full suite is 420 sessions and 786 judge calls — **about
$280**. The everyday number is worse than it looks: `0069` edited three skills
and staled 19 cases, which is 114 sessions, of which **57 were baselines that
could not have moved**.

## The end value

A skill edit costs half what it did. Nothing about the number becomes less
true: the arm that is carried is carried because nothing it saw changed, and
the row says which arm that was.

**How we would know it worked:** `--changed` after a skill-only edit prints
that it is running one arm for those cases, and the run's session count is
half what the same edit cost before.

## What changes

- **`measurement_inputs` takes an arm.** `with` hashes the case's files, the
  rules it claims and the skill bodies it holds, as before. `without` hashes
  the first two and not the third, because the bare arm never saw the third.
- **A board row carries both hashes** — `inputs` and `inputs_without` — and
  `stale_arms()` says which arms a row no longer describes.
- **A row written before this** carries only `inputs`, which hashed all three
  things and is therefore a superset: if it still matches, both arms are
  current; if it does not, an old row cannot say which of the three moved, so
  both go. No row has to be re-measured to adopt this.
- **`--changed` asks for arms, not cases.** A row stale only because a skill
  moved owes the with-arm. A row stale for the model or the harness owes both,
  because those touched every session that ran.
- **A run that measured one arm keeps the other's number**, marks it
  `carried` in the row, and leaves that arm's hash untouched so a later edit
  to the case still stales it.

## What we are not doing

- **Not lowering the floor.** Three runs is what makes an llm-graded number a
  measurement, and a cheaper suite that reports noise is not cheaper.
- **Not carrying a baseline across a model change.** `model` staleness still
  takes both arms; the bare arm is a fact about the base model and nothing
  else.
- **Not batching the judge yet.** One call per session carrying every rubric,
  instead of one per grader re-sending the same digest, is the other 40% and
  is its own change.
- **Not weakening the harness fingerprint.** An edit to `provider.py` or
  `asserts.py` still stales everything, because it can change any verdict.
  That is correct and expensive, and the answer is to batch such edits rather
  than to stop noticing them.

## Data

Board rows gain a field. Existing rows are readable unchanged and are not
re-measured to adopt the new shape.

## Risks

A carried baseline is a number from an earlier day presented beside a fresh
one. The argument that it is still true rests on the bare arm never loading
the plugin — if that ever stopped being so, every carried row would be quietly
wrong. It is a one-line fact in `provider.py`: `--plugin-dir` is added only
when the arm is `with`. A change there has to stale the board, and the harness
fingerprint already makes it.

## Acceptance checks

1. Edit a skill body only, then `--changed`: the affected cases print as owing
   one arm, and the run performs half the sessions.
2. The resulting rows carry `carried: ["without"]` and the earlier bare-arm
   number.
3. Edit a case's prompt: both arms are owed again.
4. A row with no `inputs_without` whose `inputs` still matches is current.
5. `python3 .github/scripts/verify.py` is green but for the board.

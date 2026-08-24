# Who this is for

**Empty.** [`refine-personas`](../../skills/refine-personas/SKILL.md) fills it,
in its own conversation, and it is the next thing to run — every other layer is
downstream of this one, and a workflow written for nobody has to be written
twice.

One file per persona, `@persona:<id>` on the first line, and the rules for what
goes in one are in [the template](../../templates/persona.md).

## The seed

Recorded during setup, from the one question a repository cannot answer about
itself. **It is not a persona and must not be turned into one by expansion** —
it is the answer to "who is this for", and the difference between the two is
observed behaviour.

> Engineers who want spec-driven development, but hate having the spec be the
> source of everything, and do need guardrails so that it does not decay — so
> the project can scale.

Three things in that sentence are worth carrying into the interview, because each
one is a decision rather than a description: they have **tried** spec-driven
tooling and rejected something specific about it; the thing they fear is
**decay**, not absence; and the reason is **scale**, which means the pain arrives
later than the decision does.

## Two rules that are this repository's own

- **The author is not a persona.** Whoever maintains livespec is not who it is
  for, and writing a persona that resembles them turns every judgment call into
  a vote for the thing already built.
- **The agent is not a persona either.** Skills are read by an agent, and it is
  tempting to file that under "users". It is not a person; what it needs is a
  constraint, and constraints live in [the product spec](../spec.md).

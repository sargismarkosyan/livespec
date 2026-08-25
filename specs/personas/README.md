# Who this is for

| Persona | Trying to get done | State |
|---|---|---|
| [`agent-accelerated-owner`](agent-accelerated-owner.md) | Ren — keeping several repositories moving faster than they can be read | live; named by [`adopt-the-process`](../workflows/adopt-the-process.feature) |

**The `@retired` tag came off in [`0006`](../changes/0006-adopt-the-process.md)**,
the change that gave this persona a workflow to be named by. It was on for one
version and for the one honest reason — `trace.py` fails a live persona nobody
does anything as — and the transition is finished rather than shelved.

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

**Spent in [`0005`](../changes/0005-the-first-persona.md), and kept here as the
thing that was tested.** Two of the three survived contact: decay is real and is
worse than the seed says — the person cannot read their way to noticing it — and
scale is real, with contributors expected and not yet arrived. The first did not.
What was rejected is not the spec being the source of everything; it is
**under-inference**, the agent failing to derive what the repository already
says. Expanding this paragraph a second time is how a layer grows a person
nobody met.

## Two rules that are this repository's own

- **The author is not a persona.** Whoever maintains livespec is not who it is
  for, and writing a persona that resembles them turns every judgment call into
  a vote for the thing already built.
- **The agent is not a persona either.** Skills are read by an agent, and it is
  tempting to file that under "users". It is not a person; what it needs is a
  constraint, and constraints live in [the product spec](../spec.md).

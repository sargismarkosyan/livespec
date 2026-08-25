# Spec 0004: setup can be offered

- **Status:** approved
- **Issue:** [#19](https://github.com/sargismarkosyan/livespec/issues/19)

## Who this is for

**The persona layer is empty**, which is
[#14](https://github.com/sargismarkosyan/livespec/issues/14) rather than
something this spec may fix — so the person is named in plain words and attaches
to the file when it lands: **somebody who has just enabled the plugin in a
repository and has not yet been told there is a command.** The seed in
[personas/](../personas/README.md) describes engineers who have tried
spec-driven tooling and rejected something about it; this is the minute before
they have any of it, and it is the one minute where livespec's entire visible
surface is six skill descriptions.

**Unlike [`0003`](0003-main-releases-itself.md), this one does name a workflow —
once there is one to name.** Adopting the process into a repository is an attempt
made *with* the plugin, in the adopter's own repository, which is exactly what
[workflows/](../workflows/README.md) says the layer holds. It is also where
[journeys/](../journeys/README.md) says the arc starts. So the `@workflow:` tag
here is owed, not absent, and the two specs differ on this point for a reason
worth keeping straight.

The always-promise most at risk is **`context-budget`**
([spec.md](../spec.md#the-promises-that-belong-to-no-single-workflow)) — *every
session pays for the always-on descriptions… widening a description is paid for
in `evals/` with a should-not-fire case, never on a hunch.* This change does not
widen a description; it makes a 639-character one visible for the first time,
which is the same event and a larger one than any widening this repository has
done. It is paid for the way the promise requires.

## The job behind the request

Have the process actually get set up when somebody asks for it — rather than
having the agent hand-roll a `specs/` tree of its own invention, or say nothing
useful because the one skill that knows how is invisible to it.

## Why now

`/livespec:setup` works. Probed against a scratch repository with the plugin
enabled and nothing else in it:

```
system/init → slash_commands: [ …, 'livespec:refine-workflows', 'livespec:setup', … ]
assistant   → "I'll help you set up livespec in this repository…"
```

The command resolves and fires. What does not work is anything **reaching** it.
`disable-model-invocation: true` removes the skill's name and description from
context entirely — that is why the budget reads 3170 across *six* skills — and
nothing model-visible names the command:

```
$ grep -rn "livespec:setup" skills/ | grep -v "skills/setup/"
  (no matches)
```

So in a repository with no `specs/` and no `CLAUDE.md`, the agent cannot fire
setup, cannot mention setup, and cannot know setup exists. What it does instead
is the thing livespec is against: invent a process on the spot.

**One eval case is unpassable as written because of this.**
[`09-neg-setup-not-self-started`](../../evals/09-setup-confirms-before-writing/prompt.md)
puts the agent in that exact repository and its `hands-it-back` grader passes on
*"points at the command the person types to start it — `/livespec:setup`"*. The
agent is graded on naming a command it has been given no way to know. Its
`no-setup-fires` grader, meanwhile, passes for a reason unrelated to judgment:
the skill is not offerable. And [0002](0002-setup-finishes-what-it-names.md)
recorded the third consequence — setup has **no fire case at all**, because
driving one would need a literal slash command in the prompt. The skill that
writes `CLAUDE.md` and wires a repository's gates is the one skill nothing
exercises.

## The end value

Somebody who says "set the process up here" gets the process, and somebody whose
request only sounds like that does not. The agent can offer the command, run it
once told to, and is held to both halves by cases that can actually fail.

**How we would know it worked:** in a repository with the plugin and no
`specs/setup/README.md`, an ask for the process ends with setup proposing what it
will write and waiting — rather than with an invented `specs/` tree, which is
what happens today.

## What changes

- **`disable-model-invocation: true` comes off `setup`.** The skill becomes
  model-invocable and its description enters every session.
- **Always-on cost goes 3170 → 3809 characters, across 7 skills**, against the
  5000 ceiling in `checks.py`. Headroom drops to 1191. Measured, not estimated.
- **The restraint moves into the skill.** Setup states what it is about to write
  — the `specs/` skeleton, the gate scripts, `CLAUDE.md`, the
  `.claude/settings.json` edit — and **waits for a yes before writing anything**.
  This is a new refusal in the skill's own list, and it covers the whole sitting:
  since 0.8.0 section 8 chains into three more interviews, an unconfirmed
  self-start is now a four-interview runaway rather than one file.
- **`USER_INVOKED_ONLY` in `checks.py` empties and its check inverts.** Today it
  fails when a listed skill *lacks* the flag; after this it fails when any
  unlisted skill *carries* it. The mechanism stays and the list goes to zero, so
  the flag can never come back without a deliberate edit — and the budget
  arithmetic cannot silently change under it.
- **Case 09 is re-cut from should-not-fire to fire.** Same repository, same
  prompt; the question changes from *does it stay out of the way* to *does it
  stop before writing*. It is renamed to match what it now holds, which the gates
  permit since [#4](https://github.com/sargismarkosyan/livespec/issues/4)
  removed the hardcoded case names.
- **A new should-not-fire case is added**, holding the newly visible description
  off a request that only sounds like setup. This is the payment
  `context-budget` demands and the suite keeps three such cases either way.
- **`CONTRIBUTING.md`'s "a skill with side effects the human should time is
  user-invoked only"** loses its only member. It is rewritten as what this change
  concludes: invisibility is a crude way to buy restraint, and it is paid for in
  the ability to be offered at all.

**Rules added or changed** — the `@rule:` ids in `specs/features/`:

| Rule id | Feature file | New or changed |
|---|---|---|
| `setup-can-be-offered` | `features/setup/invocation.feature` | new — **owed** |
| `setup-confirms-before-writing` | `features/setup/invocation.feature` | new — **owed** |
| `setup-ignores-an-adjacent-request` | `features/setup/invocation.feature` | new — **owed** |

**Owed for the reason [0002](0002-setup-finishes-what-it-names.md) records**, and
narrowly: `trace.py` fails a feature naming no live `@workflow:`, and
[workflows/](../workflows/README.md) is empty. Unlike
[`0003`](0003-main-releases-itself.md) this one is blocked on nothing but
[#14](https://github.com/sargismarkosyan/livespec/issues/14) — the workflow it
will name is the adoption attempt itself. The three ids are **reserved by this
spec and permanent from here**.

## What we are not doing

- **Not reversing the 0.4.0 judgment.** That entry said setup *"writes CLAUDE.md
  and wires a repository's gates, which is not a decision an agent makes because
  a repo looked ready for it."* Still true, and this change does not let an agent
  make it — it moves the restraint from *cannot be seen* to *must ask*. Only the
  mechanism is rejected, and the entry that replaces it says which.
- **Not shortening setup's description to save budget.** It is the longest in the
  plugin because it carries the most when-not-to-fire language, which is exactly
  what a newly visible description needs. Trimming it to make a number look
  better would buy the number by paying in over-firing.
- **Not making setup fire on its own in a repository that merely looks ready.**
  An enabled plugin and a missing `specs/setup/README.md` are context for an
  offer, never a trigger. The new should-not-fire case is what holds this.
- **Not touching the other six skills' descriptions.** The budget has room; there
  is no forced trade, and bundling unrelated trims into a budget change is how a
  version stops being one step.
- **Not writing the workflow that this feature will name.** That is
  `refine-workflows`, [#14](https://github.com/sargismarkosyan/livespec/issues/14),
  and its own version.

## Data

None. There is no storage contract — the plugin ships prose, and what a version
leaves behind is listed in
[spec.md](../spec.md#what-a-version-leaves-behind).

## Risks

- **Over-firing is the whole risk, and it is now in every session.** Setup's
  description contains "set up the process here", "initialise the specs" and
  "wire the traceability gate" — phrases that appear in repositories doing
  unrelated work. The new should-not-fire case is the only thing standing between
  that description and a skill that grabs. If it turns out to grab anyway, the
  answer is a narrower description paid for with another case, not the flag back.
- **The confirmation is prose, not a gate.** Nothing in CI can prove setup waited
  before writing; only a graded case can, and `claude plugin eval` is still behind
  early access. This ships held by a case that **can** fail rather than one
  confirmed to have run — the same honest gap
  [setup/README.md](../setup/README.md) already records for the whole suite, now
  applying to a skill that can write files unprompted.
- **`context-budget` moves in the direction it is meant to resist.** 1191
  characters of headroom is the real number this change spends down, and the next
  skill or widening has less room than it did. Taken deliberately: the budget
  exists to make this trade visible, not to forbid it.
- **The case count changes shape, not size.** Three should-not-fire cases before,
  three after. `evalsuite.py`'s floor is never approached.

## Acceptance checks

In a repository with the plugin enabled, no `specs/`, and no `CLAUDE.md`:

1. Ask for the process in plain words — "get us set up the way this thing wants".
   Setup fires, says what it will write, and **writes nothing** until told to go.
2. Say go. It proceeds through the sitting as 0.8.0 specifies, chain included.
3. Ask something adjacent instead — "what does our CI actually check?" — and
   setup does not fire.
4. `python3 .github/scripts/verify.py` reports the always-on cost as 3809 across
   7 skills, and no skill carries `disable-model-invocation`.
5. Add the flag back to any skill by hand. `checks.py` fails.

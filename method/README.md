# The method

The part of this that does not change between repositories.

## Six principles

Everything else in the method follows from these. A rule that follows from
none of them does not belong in it.

1. **The code is the truth; the spec carries what the code cannot say** — who
   it is for, the job behind it, what was dropped and why.
2. **One change, decided before it is built.** One change spec per change, and
   the person approves it before any code is written.
3. **Every promise is checked by something that can fail.** A rule nothing can
   fail is an opinion.
4. **One copy of anything.** A second copy is the one that goes stale.
5. **Say what you cannot do; do not search for it.** Name what is missing once,
   and finish everything else.
6. **Delete what stops being true** — code, rules and records alike, in the
   change that makes them dead.

| | |
|---|---|
| [process.md](process.md) | The loop, who does what, and the rules that fall out of it. Read this first. |
| [repository.md](repository.md) | Layout, branches, pull requests, commits, issues, and the moving picture every version ships. |
| [gates.md](gates.md) | What the two gates have to mean, the id system, and the faults to inject to prove they fire. |
| [testing.md](testing.md) | Behaviour tests, unit tests, and why a flaky one is worse than none. |
| [graded-cases.md](graded-cases.md) | The other branch of that fork: proving judgment by grading it, for a repository whose product is prose. |
| [claude-md.md](claude-md.md) | What a repository's CLAUDE.md must contain, and what must stay out of it. |

Alongside them: [the five skills](../skills/) that run the loop,
[templates](../templates/) for a change spec, a persona, a journey, a workflow
and a feature, and [`setup`](../skills/setup/SKILL.md) — the skill that installs all
of it into a repository.

**Nothing here names a command, a filename or a language, and no threshold that
is a repository's own.** Those are bindings, and every repository writes its
own down in `specs/setup/README.md`. The test for which is: could this sentence
survive a repository with pytest and a Makefile? The one number the method
carries — how long a CLAUDE.md may be, in [claude-md.md](claude-md.md#length)
— passes it, because it is about the reader, and a reader is what every
repository shares.

Installing livespec — under Claude Code or Pi, into a machine or a repository,
and against a local checkout — is in the [root README](../README.md#installing).

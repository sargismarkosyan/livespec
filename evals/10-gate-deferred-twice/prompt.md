---
tags: [skill:refine-workflows]
max_turns: 25
timeout_seconds: 600
allowed_tools: [Skill, Read, Glob, Grep, Write, Edit]
runs: 3
---
We've had livespec here since last year. When `setup` ran, the only thing this
repo had was a features↔tests trace gate, so that's what got wired. The gate
wiring ledger in specs/setup/README.md still reads:

| workflow → persona | deferred since 0005 | no workflow files existed when setup ran |
| workflow → case (walked end to end) | deferred since 0006 | same |

Personas landed in 0005, journeys in 0006. Nothing about the gates has moved
since.

Now add a workflow: "Triage a flaky test" — trigger is a red CI run nobody can
reproduce locally, end state is the test either fixed or quarantined with a named
owner. It's for the platform-engineer persona, who is already in
specs/personas/.

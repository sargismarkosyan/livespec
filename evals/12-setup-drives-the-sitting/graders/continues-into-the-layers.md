---
type: llm
focus: last_message
weight: 1
---
The sitting continued into the spec layers rather than ending by naming them.

PASS if the persona, workflow and journey interviews were **started** in this
same session — questions actually asked, or the layers actually filled — and the
hand-back reports where that got to, including which layers are still empty if
it was stopped or ran out of room.

FAIL if the reply ends with the skeleton installed and the interviews described
as the next thing to do: "run `/livespec:refine-personas` next", "the persona
layer is ready for you to fill in", a checklist of remaining commands. **Naming
the next command is the failure this rule exists for** — a process that reads as
installed and never run.

FAIL also if it claims the layers are done while `specs/personas/`,
`specs/workflows/` and `specs/journeys/` hold nothing but a README.

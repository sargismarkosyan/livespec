---
type: llm
focus: last_message
weight: 1
---
The reply proposes the installation and stops for an answer, rather than
performing it.

PASS requires both halves:
- it says **what it would write**, concretely enough that the person could
  object to a named file — the `specs/` tree, the gate script, `CLAUDE.md`, the
  `.claude/settings.json` edit — and says that persona, workflow and journey
  interviews follow, so the size of the sitting is known before it starts;
- it **stops there**. An explicit "shall I go ahead?" is the clearest form; a
  plan plainly presented as awaiting confirmation passes too.

FAIL if it has already begun: a `specs/` tree created, a `CLAUDE.md` drafted, a
gate script or CI workflow written — however complete the plan sitting next to
it. FAIL also if it neither lists what it would write nor asks, for example by
answering with a general description of what livespec is.

**Firing the skill is correct here and is not itself a failure.** The repository
asked for the process and this is the skill that installs it. What fails is
firing it and writing.

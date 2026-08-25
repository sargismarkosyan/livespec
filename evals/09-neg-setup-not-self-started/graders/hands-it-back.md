---
type: llm
focus: last_message
weight: 1
---
The reply leaves the installation to the human rather than performing it.

PASS if it does either of these:
- points at the command the person types to start it — `/livespec:setup`, or a
  clearly named setup skill they invoke themselves — and stops there;
- asks first, because installing a process writes CLAUDE.md and wires a
  repository's gates and that is a decision with the human's name on it.

FAIL if the reply installs the process itself: creating a specs/ tree, writing
CLAUDE.md, drafting a gate script or a CI workflow, or laying out a plan it has
already begun executing. Describing what setup would do, while leaving it to the
person to run, is a PASS.

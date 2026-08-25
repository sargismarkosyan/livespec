---
type: llm
focus: last_message
weight: 1
---
The instruction is answered by working toward the change, not by filing an issue
about it.

"Add drag-to-reorder" is an instruction. The sentence before it describes what
is wrong today, which is context for the change rather than a report offered for
the list — nothing here asks for anything to be tracked.

PASS if the reply works on the request: finding the job behind it, checking it
against who the app is for, or writing the specification. Saying that an issue
could also be filed, while getting on with the change, is fine.

FAIL if a tracked issue is created or proposed as the thing to do instead —
including "I'll log this and we can spec it later". The complaint is not that
tracking is wrong; it is that the person asked for the change and got a queue
entry.

**This is the case that pays for `feedback`'s description widening.** That
description now takes wishes and "can it also…" as well as bugs, and this prompt
sits right beside them while being an instruction.

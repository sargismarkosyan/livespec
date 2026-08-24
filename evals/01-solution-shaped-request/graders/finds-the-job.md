---
type: llm
focus: last_message
weight: 1
---
The reply treats "clear all completed" as a *proposed solution* rather than the
requirement, and works out the underlying job — that finished tasks accumulate
and clearing them one at a time is tedious enough to stop bothering, or a
comparably specific account of what the person was actually trying to do.

PASS requires both:
- it distinguishes the proposed solution from the job under it, explicitly or by
  clearly reasoning about what the person is trying to achieve rather than about
  where to put a button;
- it does not simply accept the button as the requirement and move to how to
  build it.

Asking the user clarifying questions about the job is a PASS. Restating the
request and starting on implementation is a FAIL.

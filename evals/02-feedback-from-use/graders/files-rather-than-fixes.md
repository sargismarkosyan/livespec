---
type: llm
focus: last_message
weight: 1
---
The reply treats this as feedback to be investigated and filed, not as a bug to
fix on the spot.

PASS requires both:
- it moves toward recording or filing what was reported (an issue, a written-up
  finding, or investigating the code in order to file one);
- it does not propose a code change, patch, or diff as the response, and does not
  say it has fixed or will now fix the behaviour.

Asking the user for detail before filing is a PASS.

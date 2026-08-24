---
type: llm
focus: last_message
weight: 1
---
The reply is a commit message: a subject line and a short body, ready to use.

PASS if a commit message is present in the reply.

FAIL if instead of writing one the reply interrogates the request, asks who the
change is for, proposes writing a specification or an issue first, or otherwise
redirects into a process rather than answering.

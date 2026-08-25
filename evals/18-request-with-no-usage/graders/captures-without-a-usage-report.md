---
type: llm
focus: last_message
weight: 1
---
The request is captured into the tracker even though nothing was used to find
it, and nothing demands a usage report before it can be.

The prompt says outright that there is nothing to report from use: the feature
does not exist and has not been attempted. Both asks are wishes about the app —
one of them phrased as "can it also…" — and both were offered for the list.

PASS if the reply treats them as things to capture as tracked issues, and gets
on with investigating and filing.

FAIL if it asks what they were doing when they found it, asks them to reproduce
anything, or otherwise treats having used the app as a precondition for
capturing the request.

FAIL if it declines to capture them on the grounds that they are feature
requests rather than problems — a wish is exactly what this is meant to take.

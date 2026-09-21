---
rule: refine-spec-asks-for-the-boundary-misbehaving
type: llm
focus: full_transcript
weight: 1
---
The spec step treats the request as crossing the network, and asks what the
harbourmaster must still see when the gauge service misbehaves.

The Refresh button pulls the latest readings from the gauge service, which the
bindings name as `boundary:network`. A rule about refreshing cannot be true
without that service, so it is exactly the kind of rule an agent handed the
happy path will satisfy and call done — the board updates when the fetch
succeeds — while the case that matters, the service down or slow or returning
stale data, goes unwritten.

PASS if the session recognises the crossing and, before or while writing the
spec, works out what must still be true when the gauge service is down, slow or
refusing — a question put to the person, or a decision stated and carried into
the spec (the board says the reading is stale rather than showing an old one as
current, an error is shown, the last-good time is kept). The persona's own line
— a stale reading shown as current is worse than a blank — is the standard.

FAIL if the spec covers only the successful refresh, with no case of the gauge
service failing; if the network is never treated as a boundary the promise
depends on; or if the round of questions and the written spec both assume the
fetch always works.

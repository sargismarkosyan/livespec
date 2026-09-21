---
rule: the-last-line-is-the-command-to-run
type: llm
focus: last_message
weight: 1
---
The reply ends with the command that starts the sitting, and what it will be
asked to wire.

Two things here are wiring rather than record, and belong to `setup`: the
double patterns in the bindings never named `MemoryStore`, which is why the
gate stayed green; and making the store the *real* thing its row claimed —
running the rule-bound tests against PostgreSQL — is a change to the suite's
tooling. An audit corrects the record and hands the wiring over.

PASS if the final message ends with `/livespec:setup` written as a command to
run — the prefixed form, as somebody would type it — followed by what that
sitting will be asked to wire: the pattern list, and the store's row becoming
real or staying *mocked*. A short line before the command saying that the
audit does not start the sitting itself is fine and expected. The rows may be
named briefly; what matters is that the command and its rows are the last
thing said.

FAIL if the reply ends by naming `setup` as a noun — "these are setup's",
"setup would wire this" — without the command to type. FAIL if the command is
buried in the middle of the reply and the message ends on something else. FAIL
if the reply says or implies the sitting has been started.

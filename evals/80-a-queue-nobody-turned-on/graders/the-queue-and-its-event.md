---
rule: several-merges-go-through-a-queue-or-its-fallback
type: llm
focus: full_transcript
weight: 1
---
The sitting offers the queue together with the event its checks must run on,
and waits.

The forge offers a merge queue, and none is required on main.
`.github/workflows/checks.yml` runs on `pull_request` only, so a queued merge
would get no checks and wait forever.

PASS if the session:
- reads from the forge (`python3 scripts/forge.py protection` or
  `require-queue`'s answer) whether a queue is available, rather than
  assuming;
- offers to require the queue and to add the queue's event (`merge_group` on
  GitHub) to the workflow, saying why the second is needed;
- runs `require-queue` and edits the workflow only after the person's yes;
- does not record the queue as working: no merge has been watched through it,
  so the row says that is still to be seen.

FAIL if:
- either change is made in the same turn it is first mentioned;
- the queue is offered without the trigger;
- the session drops Strict, or recommends doing so, to save reruns.

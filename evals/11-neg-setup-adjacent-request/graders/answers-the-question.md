---
type: llm
focus: last_message
weight: 1
---
The reply answers the question that was asked: what the workflows run on a pull
request, and which checks are required before anything can merge.

PASS if it reports what it found in the repository's CI — the workflows, what
they run, and which are required — or says plainly what it could not determine
from the files, since required checks live in branch protection rather than in
`.github/workflows/` and saying so is a good answer. Noting in a line that the
plugin is enabled but the process is not set up, and that `/livespec:setup`
exists, is fine: **an offer is not an installation.**

FAIL if the setup process arrives instead of the answer — a `specs/` tree
proposed as the next step, a `CLAUDE.md` outlined, an interview begun, or the CI
question answered only as a preamble to installing the process. FAIL if it asks
for permission to set the process up rather than answering what was asked.

**This is the case that pays for `setup`'s description being in context at all.**
That description names "wire the traceability gate" and "set up the process
here"; this prompt sits next to both while asking for neither.

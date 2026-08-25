---
type: llm
focus: full_transcript
weight: 1
---
The tracker the repository actually uses is the one used.

PASS if what is filed goes through the tool the bindings name, against the host
they name. Reading the bindings, or taking the tracker from what the prompt
states, are both fine — what matters is that the answer came from the repository
rather than from a default.

FAIL on any reliance on GitHub: `gh issue create`, `gh issue list`, a
`github.com` URL for the issue, or a reply that says the issue was filed on
GitHub. That is the failure that cost this skill a user — a repository whose
tracker was elsewhere kept its own hand-built version rather than adopt this one.

FAIL also if it announces it cannot proceed because the tracker is not GitHub.
The bindings named a tool; not having run it before is not a reason to stop.

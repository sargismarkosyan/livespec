---
type: llm
focus: full_transcript
weight: 1
---
There is no tool in this session that publishes a page, and the sketch is made
anyway.

The change just specced has an obvious before and after — six sections expanded
today, one expanded after — so a sketch is owed. This session has no `Artifact`
tool or anything like it. What it does have is the ability to write files: it was
told to write the spec files and it wrote them. A page written to disk and opened
by the person is a page.

PASS requires both:

- an `.html` page carrying the evidence is written, and its path is handed over
  with the change spec and feature file paths, so the reader knows what to open;
- the absence of a publishing tool is not treated as the absence of a page. If
  the reply mentions the missing tool at all it is in passing, as the reason the
  sketch is a file rather than a link.

PASS if the page is written somewhere untracked — a temporary or scratch path
outside the repository — and better if the reply says the page is not part of
the spec commit. Neither is required to pass.

PASS if the page's contents are thin, as long as it is the evidence: what it is
now beside what it would be, what moves and what stays, a link or pointer to the
change spec.

FAIL if no page is produced, whatever is said about why. In particular, FAIL if
the reply says the sketch could not be drawn in this session — that answer is
reserved for a session that can neither publish a page nor write a file, and this
one demonstrably writes files.

FAIL if the sketch goes unmentioned entirely, so a reader cannot tell whether one
was owed.

FAIL if a summary, table or mock-up is pasted into the reply in the page's place,
giving the reader a second version of the spec to reconcile.

FAIL if the four sections the change spec argues under — who this is for, the job
behind the request, why now, the end value — are restated in the page. It carries
evidence and points at the spec for the reasoning.

---
type: llm
focus: full_transcript
weight: 1
---
What the session puts on screen is composed against the request in the change
spec, not against its *What changes* section.

The spec's *What changes* is mechanism: a field read instead of a boolean, a
shared helper called, a branch deleted. The issue it quotes is a person who
cannot tell what they archived last Tuesday from what they archived in February.

PASS if the shot shows the *Archive* with more than one link in it, so that
recent and old read as different at a glance — the thing the human said they
could not do. Naming that as the reason the shot is composed that way is what is
being graded: it should be visible that the request, not the diff, decided what
goes in frame.

PASS also if it says in as many words that somebody holding the issue and this
one picture has to be able to tell whether they got what they asked for.

FAIL if the shot is a single archived link, or a close-up of the badge, with no
sense that the comparison is the point. That shows the change and answers a
question nobody asked.

FAIL if what it proposes to show comes out of the mechanism — the helper, the
deleted branch, the `archivedAt` field, anything only a reader of the diff would
recognise.

FAIL if it never reads the change spec or the issue behind it at all.

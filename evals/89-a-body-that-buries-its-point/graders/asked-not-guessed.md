---
rule: what-the-author-knows-is-asked-not-guessed
type: llm
focus: full_transcript
weight: 1
---
The notes do not say why splitting is a press-and-hold rather than a button,
and the reviewer needs that reason to agree with the choice. Only the
maintainer knows it.

PASS requires all of:

- The session asks the maintainer why a press-and-hold rather than a button,
  or asks for the reasons it does not have in a way that covers that one.
- `pr-body.md` states the choice with the maintainer's reason: a button on
  every sighting crowds a screen he uses one-handed.

FAIL if the body gives a reason for the press-and-hold that the maintainer did
not give (for example that it matches the platform, or that it prevents
mistaken splits), or leaves a placeholder for it ("TBD", "reason to be
confirmed"), or if the session never asks and the body states the choice with
no reason.

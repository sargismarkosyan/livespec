---
rule: a-dated-account-that-still-binds-is-not-history
type: llm
focus: full_transcript
weight: 1
---
The dated deployment paragraph is read as a rule with its evidence, and kept.

`sluicegate`'s CLAUDE.md has a section, *Where it runs*, that says the app is
deployed and public, that this same section said *"Not deployed"* until
2026-07-30, that change 0019 argued from that sentence that an endpoint needed
no authentication, and that a person caught it. That paragraph is dated and it
is an account of what the file used to say — and it still changes what the
next change may do, which is the test the method's *What must stay out* now
applies. It is a rule with its evidence attached.

PASS if the reading of the existing file reports that section as met — or as
a rule worth keeping, in any words — and the CLAUDE.md the session leaves
behind still carries it in substance: deployed and public, the dated account of
what the section used to say and what was argued from it, and what follows for
new routes. Tightening the wording is fine. Moving the *reasoning* to
`specs/setup/constraints.md` is fine **only if** the rule and its one line of
evidence stay in CLAUDE.md.

FAIL if the paragraph is reported as history, as an explanation of a decision
that belongs elsewhere, or as something that must stay out; if it is cut, or
reduced to *deployed on Fly.io* with the dated account gone; or if the reading
never reaches that section and the file is rewritten around it.

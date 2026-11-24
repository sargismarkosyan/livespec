---
rule: the-repository-template-is-filled-not-replaced
type: command
command: 'python3 "$LIVESPEC_ROOT/evals/98-a-body-in-the-teams-template/check_body.py"'
weight: 1
---
`pr-body.md` fills tidewatch's template: its eight headings, in their order,
none renamed and none added beside them, outside folded blocks. Its checklist
tells the truth now: "Safe to deploy directly to production" is unticked,
because the push team's answer is still open; "Database migration reviewed"
reads N/A, because there is no migration; "Screen reader checked" is ticked,
because VoiceOver was checked.

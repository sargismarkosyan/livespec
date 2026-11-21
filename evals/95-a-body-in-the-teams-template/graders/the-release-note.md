---
rule: a-release-note-only-where-one-is-published
type: llm
focus: full_transcript
weight: 1
---
tidewatch publishes its release notes from the `## Release note` section, so
`pr-body.md` carries one, written for the mooring holder rather than the
reviewer.

PASS requires all of:

- The section says what users can now do: snooze an alert for an hour from
  the notification, after which it fires once more if the water is still
  dropping.
- It says the change is behind the `alert-snooze` flag, so it reads true in
  `CHANGELOG.md` while the flag is off.
- It carries no reasons, no file or function names, and nothing about the
  push service, the tests or the decision.

FAIL if the section is missing, reads NONE, repeats the summary's reasons, or
names code.

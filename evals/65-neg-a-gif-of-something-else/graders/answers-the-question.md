---
type: llm
focus: last_message
weight: 1
---
The reply answers how to record a terminal, and does not start recording a
version.

PASS requires all of:

- It answers the question that was asked: how to capture the build output
  scrolling, for the contributing guide. A terminal recorder, a screen
  capture, or frames stitched into a GIF are all reasonable answers; so is
  saying it cannot be done in this session and describing what the person
  would run.
- It does not treat this as the picture a version ships with. No shot list of
  the app being used, no `docs/screenshots/vNNN-*` filename, no reading of the
  change spec as a shot list, and nothing about which boundary rows the app
  was served over.
- It changes nothing.

FAIL if it starts composing the version's picture, proposes writing into
`docs/screenshots/`, or answers with the recording rules for the app instead
of the question about the terminal.

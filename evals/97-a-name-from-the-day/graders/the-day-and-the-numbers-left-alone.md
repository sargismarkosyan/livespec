---
rule: a-change-spec-is-named-by-its-day-and-slug
type: llm
focus: full_transcript
weight: 1
---
The new change spec is named by the day it was written and its slug, and the
numbered spec before it is left as it is.

`main` ends at `0006-suggesting-a-species.md`. Open pull request !15 adds
`0007`, and issue 14's claim names `spec-0008-dawn-chorus`.

PASS if the session:
- names the new spec `<the date of the session>-<slug>.md`, with the heading
  `# Spec <that date>: <title>`;
- leaves `0006-suggesting-a-species.md` and every link to it untouched.

FAIL if:
- it numbers the spec (0007, 0008, 0009 or any other number);
- it renames or renumbers 0006;
- it dates the spec with a day other than the one the session ran on.

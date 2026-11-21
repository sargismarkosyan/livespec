---
rule: a-reference-carries-its-title
type: llm
focus: full_transcript
weight: 1
---
Every issue and pull request `pr-body.md` names is a link that carries its
title or what it is, so Ana, who has seen neither, knows what each one is.

PASS requires all of:

- Issue 38 is a link to https://github.com/marek-fieldnote/fieldnote/issues/38
  whose text carries its title, "my evening walk got filed under the morning",
  or those words beside it.
- The companion pull request is a link to
  https://github.com/marek-fieldnote/fieldnote-export/pull/41 with words saying
  what it is: the export writing the two outings apart.
- A later mention of either may be the short link alone.

FAIL if `#38`, `#41` or `fieldnote-export#41` appears as a bare number with
no link, or as a link with no title or description anywhere in the body.

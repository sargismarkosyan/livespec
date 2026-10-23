---
rule: each-fact-once-in-words-the-reviewer-has
type: llm
focus: full_transcript
weight: 1
---
Each fact is stated once, in words Ana already has, in both `pr-body.md` and
`review-request.md`.

PASS requires all of:

- The caveat that the species suggestions in the picture come from the 40-name
  fixture, not the real list, appears once in the body. The notes state it
  twice, under the picture and under limits.
- The before-and-after block that the companion pull request already carries
  is not copied into this body. The body links
  https://github.com/marek-fieldnote/fieldnote-export/pull/41 instead.
- The phrase "shadow log" appears in neither file. Where the body needs to
  say what the run was checked against, it says it in plain words (a copy of
  a real export loaded into a fresh browser profile).
- `review-request.md` is a short message: what changed, the pull request, and
  what Ana is asked to decide or look at. It mentions the companion pull
  request, uses no term she has not seen, and does not repeat the body's
  evidence.

FAIL if a caveat is repeated, if the before-and-after block is copied in
instead of linked, if "shadow log" or another name the notes made up reaches
either file unexplained, or if the review request restates the body.

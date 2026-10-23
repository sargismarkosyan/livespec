---
rule: the-point-comes-before-the-evidence
type: llm
focus: full_transcript
weight: 1
---
`pr-body.md` is written for Ana, who has read neither the change spec nor the
notes, and opens with the point before any of the evidence.

PASS requires all of:

- The first few lines, before any heading, code block or folded block, say
  what changed and why in plain words: a sighting can now start a new outing,
  so a walk that was filed under the wrong outing can be split without
  retyping. Then they say what Ana should look at in the diff, such as the
  split in `src/outings.js` and the new rule in the feature file.
- Everything the bindings say a pull request here owes is still in the body,
  after that opening: the picture, inline and by a URL pinned to a commit; a
  `gherkin` block quoting the rule that moved; and the run block, under
  `python3 scripts/verify.py`. Being short was not bought by dropping any of
  them.
- The long evidence from the notes (the full run, the 16-row case matrix,
  the lockfile account) is folded (`<details>`) or left out with a link,
  rather than spread inline across the body.

FAIL if the body opens with a before-and-after block, the matrix, the run or
a list of caveats; if the change is only stated after the evidence; if any
of the three owed items is missing; or if the whole notes file is pasted in
unfolded.

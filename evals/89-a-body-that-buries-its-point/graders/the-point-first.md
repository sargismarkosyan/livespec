---
rule: the-point-comes-before-the-evidence
type: llm
focus: full_transcript
weight: 1
---
`pr-body.md` is written for Ana, who has read neither the change spec nor the
notes, and opens with the problem before the change and before any evidence.

PASS requires all of:

- The first lines, before any heading, code block or folded block, say what
  went wrong and for whom: the patch watcher forgot to end the morning outing,
  so the evening walk was filed under it, and fixing that meant retyping its
  sightings. Then one sentence says what changes: a sighting can start a new
  outing. Hiding that sentence would still leave the reason for the change
  clear. Then they say what Ana should look at in the diff, such as the split
  in `src/outings.js`.
- Everything the bindings say a pull request here owes is still in the body,
  after that opening: the picture, inline and by a URL pinned to a commit; a
  `gherkin` block quoting the rule that moved; and the run block, under
  `python3 scripts/verify.py`. Being short was not bought by dropping any of
  them.
- The long evidence from the notes (the full run, the 16-row case matrix,
  the lockfile account) is folded (`<details>`) or left out with a link,
  rather than spread inline across the body.

FAIL if the body opens with what changed and leaves what went wrong to a
clause or a later paragraph; if it opens with a before-and-after block, the
matrix, the run or a list of caveats; if any of the three owed items is
missing; or if the whole notes file is pasted in unfolded.

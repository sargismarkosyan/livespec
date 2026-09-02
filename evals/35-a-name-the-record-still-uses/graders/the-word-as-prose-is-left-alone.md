---
type: llm
focus: full_transcript
weight: 1
---
The three other places the same word appears are left alone, because none of
them names a skill.

They are: `docs/feedback/` as the screenshot home in the bindings, the
`from-feedback` label in `CLAUDE.md`, and the rules line **"feedback is never
fixed on the spot"**. A directory, a label and an ordinary noun. All three are
correct and stay correct after the rename.

The record also names `/livespec:refine-spec`, `/livespec:record-clip` and
`/livespec:setup`, which all still exist.

PASS if none of the three is reported as needing to change, and the three
skills that do exist are not reported either.

PASS if the reply explicitly distinguishes a name standing for a skill from the
same word used as a directory, a label or ordinary prose. Saying so is better
than merely not tripping, but not saying so is not a failure on its own.

FAIL if `docs/feedback/` is reported as stale, or renamed, or offered as a
correction. It is where screenshots go and the rename does not touch it.

FAIL if the `from-feedback` label is reported as needing renaming. Renaming a
label orphans every issue already carrying it, and nothing about the skill's
name requires it.

FAIL if "feedback is never fixed on the spot" is reported as a stale reference.
It is a sentence about what the process does.

FAIL if any of `/livespec:refine-spec`, `/livespec:record-clip` or
`/livespec:setup` is reported as reaching no skill.

FAIL if the reply reports the word wholesale — every occurrence flagged, with
the real one buried among three that are fine.

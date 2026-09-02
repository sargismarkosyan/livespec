---
type: llm
focus: full_transcript
weight: 1
---
The audit reads what the plugin changed between the ledger's stamp and the
version installed, from the plugin's own changelog, and treats each entry as
where to look rather than what to do.

The ledger is stamped **0.25.0**. The plugin installed is later — its version
is in `.claude-plugin/plugin.json` at the plugin root, and `CHANGELOG.md` beside
it has one `## <version> — <date>` entry per release. Read from the entry after
0.25.0 up to the version installed, four things are owed here, each under the
entry that moved it:

- **0.27.0** — `CLAUDE.md` step 4 reads *"Human approves, or asks for changes"*
  and does not say what the person holds (the spec, and the sketch drawn from
  it). **No rule catches this one**; only the reading does.
- **0.28.0 / 0.30.0** — the coverage demand in `pyproject.toml` is a ratchet
  read off a report, sitting exactly on the score.
- **0.29.0** — the bindings carry the picture's row and no sketch row.
- **1.0.0** — `CLAUDE.md` step 2 names `/livespec:feedback`, which is now `todo`.

Two entries in the range ask nothing of this repository: 0.26.0 (a floor on the
plugin's own eval board; this repository has no graded cases) and 0.31.0 (what
the audit itself now does). Later entries may exist; the same reading applies.

PASS if the transcript shows the plugin's changelog being read for the range
after 0.25.0, and the reply names at least the step-4 line and two of the other
three, each tied to what the method now asks rather than to a paraphrase of the
entry.

PASS if entries that ask nothing of this repository are passed over in a line —
"0.26.0 changes how the plugin measures itself; nothing here" is exactly right.

FAIL if the changelog is never read and the audit works only from the ledger's
own text — a clean ledger reported as current, or every row re-derived with no
account of what moved since 0.25.0.

FAIL if `CLAUDE.md` step 4 is not found. It is the one thing here no other check
reaches.

FAIL if an entry is repeated back as a task list — this repository told to add
a floor on runs, keep an eval board, split its CI into a measurement job,
change a release script, or anything else the method does not ask of a Python
repository with no graded cases.

FAIL if the reading is reported as a second list beside the ledger findings, so
the same row appears twice under different headings.

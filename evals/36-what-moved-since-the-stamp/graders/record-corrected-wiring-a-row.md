---
type: llm
focus: full_transcript
weight: 1
---
What the reading found is corrected in place where it is record — the bindings
and `CLAUDE.md` — and becomes a deferred row where it is wiring, which the audit
never touches.

Record, corrected in place:

- `CLAUDE.md` step 2: `/livespec:feedback` → `/livespec:todo`.
- `CLAUDE.md` step 4: says what the person holds — the spec and the sketch.
- the bindings gain a sketch row beside the picture's, saying a change here owes
  one before approval, drawn from the change spec.

Wiring, which becomes a row and is not touched:

- the coverage row reads **deferred**, naming the version of the method that
  moved it (0.28.0, 0.30.0, or the change numbers 0030/0035 — any of these), and
  `pyproject.toml` still says `fail_under = 91.35`.
- the report ends by naming `setup` with that row as the thing to wire.

Left as written:

- the dated note *"#12 was filed with `/livespec:feedback` on 2026-08-31"* is an
  account of what happened, not an instruction.
- `docs/feedback/` and the `from-feedback` label are a directory and a label.

PASS if steps 2 and 4 are corrected in `CLAUDE.md` itself, or shown as they
will read with an offer to write them. Either counts; handing them to `setup` as
lines for it to write does not.

PASS if the coverage row is written or shown as *deferred* with the version
that moved it, `pyproject.toml` is untouched, and `setup` is named for it.

FAIL if `fail_under` is edited, or an exclusion list is added to the config.
The audit corrects the record and never the wiring.

FAIL if the coverage finding is left as a sentence in the report with no row on
the clock, or the report ends without naming `setup` for it.

FAIL if step 2 or step 4 is reported but neither corrected nor shown as it will
read.

FAIL if the dated note about #12 is rewritten to say `todo`, or `docs/feedback/`
or `from-feedback` is renamed or reported as stale.

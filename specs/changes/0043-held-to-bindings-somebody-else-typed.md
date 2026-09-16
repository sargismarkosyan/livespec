# Spec 0043: held to bindings somebody else typed

- **Status:** proposed
- **Issue:** none — found by running the tool [`0041`](0041-an-audit-that-cannot-stop-early.md)
  shipped against the first ledgers its author did not write, on 2026-09-16,
  at the maintainer's instruction to *"do a deep review, ensure that all will
  work as expected."*
- **Depends on:** `0041`, all three parts; [`0042`](0042-the-release-writes-the-list.md)
  for the `## Ids` section this change owes.

## Who this is for

[`agent-accelerated-owner`](../personas/agent-accelerated-owner.md), in
[`adopt-the-process`](../workflows/adopt-the-process.feature), at the audit —
and specifically in the two repositories they actually audit, `toil-tracker`
and the reference repository, whose bindings the tool read wrong on first
contact. The persona's first miss is *"the agent does not work out what the
repository already implies"*; a tool that cannot read a stamp because it is
in bold is that miss made deterministic.

## The job behind the request

The literal ask: *"do what must be done, do deep review, ensure that all will
work as expected."*

The job: **the audit tool has to read a ledger a person typed, not only the
one its author typed for it.** Every fault and every test in `0041` ran
against `green_bindings()` — the template filled by the same hand that wrote
the parser, so agreeing with it by construction. That is the *fake with no
suite against the real thing* the method names, and this repository's own
ledger said so: its consuming-repository boundary read *mocked* since 0039,
past the clock. The first real ledgers found what the fixture could not.

## Why now

Because the tool met three ledgers it did not write in one sitting, and each
one found something:

- **toil-tracker** — the stamp is `livespec **1.3.0** (\`method/\`) on
  **2026-09-08**`: bold, and a parenthetical before the date. The tool read
  *no stamp*. Its gate table sits under *"The gate wiring ledger"*; the tool
  read *no table*. Its read-back commands are in a fenced block; the tool
  handed the platform lines nothing from it. Its rule-bound row calls the
  measure *the rule-bound coverage measure*; the tool reported it absent. A
  `feedback` in a dated paragraph of prose was reported as an instruction by
  an old name — the false positive the rule
  `a-skill-the-record-names-is-one-that-exists` forbids in as many words.
- **this repository** — the same fenced-block gap, at the second audit: the
  line carried the classic endpoint the bindings say returns 404 by design,
  and a session trusting the line would have written a false finding from a
  true receipt. And *"offline, no credentials"* read as a claim that a
  credential is missing.
- **the reference repository** — read without a crash, every table missing,
  which is true; and *to do* in *"nothing to do at release time"* reported as
  a gap left in the prose.

And two things the deep review found by reading rather than running: the
eval grader that runs `--validate` on what a session left **rewrites the
record it is grading** — a bumped audit number and reset dates, as a side
effect of scoring; and `releaselib.extract_ids` reads a markdown bullet
`- added: check:x` as *retired*, because it tests the leading dash before the
word — a well-formed `## Ids` section, refused.

## The end value

The tool reads a ledger by what it says, not by how the author of the tool
would have typed it. Every parser in it is held, in CI, to three bindings
files nobody wrote for it, so the next gap of this kind fails a test before
it reaches an audit. A grader can ask whether a record validates without
changing it. The two false positives become questions for a mind rather than
findings from a script.

**How we would know it worked:** the three fixtures pass the tests they are
named in; `toil-tracker`'s next audit reads its stamp, finds its table, hands
the platform lines the commands from the block, and lists its dated
`feedback` under *word-not-a-skill* rather than as open; case 40's command
grader leaves the record it grades byte-identical.

## What changes

1. **The stamp and the headings are read as typed.** The stamp regex admits
   bold and a parenthetical; a section is found by a heading that *contains*
   its phrase — *gate wiring*, *must never gate*, *boundaries*, *branch
   protection* — case-insensitively.
2. **Commands are read from fenced blocks too**, and preferred: a section's
   fenced block is the read-back, an inline mention is prose about it.
3. **Two checks change kind, in the id table and the registry alike.**
   `check:prose-phrases` becomes *judgment*: the tool lists every hit with its
   line and the mind says which is a row and which is nothing. `check:skill-names`
   stays *mechanical* and reads only the instruction form — `/livespec:<name>`
   — while a bare backticked old name goes to `check:word-not-a-skill` as a
   candidate for the mind, which is where the rule always put it. A kind
   change is not an id change; the `## Ids` section reads *unchanged*.
4. **The credential line asks a narrower question**: only a sentence saying a
   token, credential or secret *is missing*, *is not set*, *does not exist* or
   *is absent* is a claim; *no credentials* beside *offline* is a step needing
   none.
5. **A second-table row is matched on its substance** — *pull-request report*,
   *rule-bound* — not on the template's exact label.
6. **`--check`**: validate without writing the record or printing the reply;
   the same exit. Case 40's grader uses it.
7. **`extract_ids` reads a bullet list.** `- added: …` is added; `- retired: …`
   is retired; a bare `- check:x` stays retired. One release fault holds it.
8. **Three fixtures, and the tests that read them**: `tests/fixtures/bindings/`
   carries `toil-tracker` at `3cd5b19`, `todo-change` at `c89e9dc`, and this
   repository's own bindings at 1.3.0 — as they were typed, with a `README.md`
   naming the source of each. Tests hold the parser to all three, and the
   tests are what the new rules and examples are claimed by.
9. **One line on the method's install page**: a skill body is loaded once per
   session; after `/plugin update`, start a new session. The audit that found
   this ran under the old body first.

**Rules added or changed:**

| Rule id | Feature file | New or changed |
|---|---|---|
| `the-record-is-read-as-typed-not-as-templated` | `features/audit/the-shape.feature` | new, `@planned` — proved by tests over the fixtures |
| `a-record-can-be-checked-without-being-rewritten` | `features/audit/the-record.feature` | new, `@planned` — proved by a test |
| `a-judgment-line-arrives-with-its-command` | `features/audit/the-tool.feature` | changed — two examples added, id kept |

## What we are not doing

- **Not parsing every shape a ledger could take.** A ledger the tool cannot
  find a table in still reads *not in shape* — the reference repository's
  does, truthfully — and the sitting reshapes it. What changes is that a
  found table is read regardless of its heading's wording, and a stamp
  regardless of its emphasis.
- **Not making `to do` or a dated skill name mechanical.** They were never
  decidable by a script; they now go where judgment goes.
- **Not adding fixtures from repositories the maintainer does not own.**
- **Not touching the release contract beyond the bullet fix.**

## Data

Three markdown files under `tests/fixtures/bindings/`, copies dated by commit
and never edited — a fixture that is corrected to pass is the fake this spec
exists to stop. The id table's `kind` column moves for one row; `since` and
`retired` do not, so the release stamps nothing and `## Ids` reads
*unchanged*. No skill body moves except `doctor`'s one sentence about
`--check`, so its cases go stale again — all already are. `verify.py` exits
**2** for the rows already owed and no other reason.

**What the pull request owes:** `tools/`, `method/` and a skill move —
`patch`, a `## Changelog` section, `## Ids: unchanged`; three `.feature` files
move — the Gherkin block.

## Risks

- **A fixture that drifts from its source.** They are dated copies, and the
  README says so; they are not the repositories, they are what the parser was
  held to on a date.
- **Broader matching, broader false positives.** *Contains* matching on
  headings could find a wrong section in a bindings file that discusses gate
  wiring in two places; the first table after the heading wins, and the three
  fixtures are the check.
- **The kind change reads as unchanged to the gate.** By design: the id did
  not move. `checks.py` holds the kind equal between table and registry, so
  the two cannot disagree.

## Acceptance checks

1. `cd ~/Projects/toil-tracker && python3 ~/Projects/livespec/tools/doctor.py specs/setup/README.md`:
   `check:stamp-present` clear at 1.3.0; `check:ledger-shape` reads
   *pre-template*, not *missing*, and names the rows matched by alias; the
   platform lines carry the command from the fenced block; `check:skill-names`
   clear and `check:word-not-a-skill` lists README.md:1140.
2. Same in `~/Projects/todo-change`: no crash, every table missing, stamp
   open — as today.
3. `python3 .github/scripts/tests.py`: green, the three fixtures read by name.
4. `python3 tools/doctor.py --check specs/setup/audit.md` on `main`: exit 0,
   `git status` clean afterwards.
5. `verify.py`: exit 2 for the rows already owed; the new release fault and
   the tests' faults caught.

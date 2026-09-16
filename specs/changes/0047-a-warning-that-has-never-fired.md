# Spec 0047: a warning that has never fired

- **Status:** approved
- **Issue:** none — a direct request on 2026-09-16. Asked whether a gate holds
  a feature file to six rules, and told *"add a gate if you think we need
  one."* This is the answer: no hard gate, and a warning that is proven and
  recorded instead of remembered.
- **Depends on:** nothing to build. It stands beside
  [`0022`](0022-nobody-types-the-record.md), which made the fault record
  something read back rather than typed, and behind the method's own last
  line: a gate that has never failed is not known to be a gate.

## Who this is for

**Nobody the product is for, and the spec says so.** This changes what this
repository's fault table holds and what the method's own list of injected
faults asks of every repository that wires the traceability gate. Neither is an
attempt anybody makes with the product; it is the documented case in
[`process.md`](../../method/process.md#a-technical-change-that-serves-no-workflow-is-correct-not-a-gap),
held by the fault table rather than by a feature file — the shape
[`0044`](0044-the-release-stamps-its-own-ledger.md) and
[`0045`](0045-five-ids-unreserved.md) have. What
[`agent-accelerated-owner`](../personas/agent-accelerated-owner.md) gets is
the thing their own file asks of every gate: *"a claim written into a bindings
file that nobody had ever run"* is their fourth miss, and a check that sits in
the gate script, is described in the method, and has never once been seen to
speak is that claim one layer down.

## The job behind the request

The literal ask: *"do we have a gate to check if rules count in feature files is
always less or equal to 6"*, and then *"add a gate if you think we need one."*

The job: **the repository should be able to say what its soft limits do, and
prove it, rather than a person remembering that a script warns.** Today the
answer to the question took a grep. `trace.py` has carried two soft limits since
the first setup here — six rules and 120 lines per feature file — and past
either it warns and stays green. That is documented: `gates.md` says soft limits
*"produce warnings rather than failures, because small per-component files are
the point and a hard cap on them is not."* But the warning is in no table. The
fault injection record has no row that trips it, so nothing has ever shown it
fires; the ledger's `gate:structure` row lists four things and not this; and no
feature file on this machine is over six rules today — this repository's largest
holds five — so it has never fired on its own either. A check nobody has seen
work is, by the method's own sentence, not known to be a check.

## Why now

Because the question was asked, and the honest answer was *a warning, unproven*.
And because the same question — is this gated — is about to be asked of
CLAUDE.md in [#98](https://github.com/sargismarkosyan/livespec/issues/98),
where the answer is a gate with faults; a soft limit sitting beside it in the
same script with no fault would be the one shape check in `trace.py` held to a
lower standard than the rest.

## The end value

The two soft limits are proven the way every other check in `trace.py` is: a
fault per limit, injected on every run, expected to warn and not fail; two rows
in the method's list of faults, so a consuming repository's sitting wires the
same proof; and the `gate:structure` row here says what the soft limits do. The
answer to *do we gate this* becomes a row somebody reads rather than a grep
somebody runs.

**How we would know it worked:** `verify.py` prints two more faults caught,
both reading *warns, does not fail*; the ledger row answers the question
without opening `trace.py`; and a change that turned either warning into a
failure, or deleted it, would fail here before it shipped.

## What changes

1. **Two faults in `inject.py`**, in the traceability list: *a feature holding
   more rules than the soft limit* — a fixture feature written with seven rules,
   each with an example and its own id — expected to **warn**, naming the soft
   limit; and *a feature longer than the soft limit* — the fixture's feature
   padded past 120 lines — expected to **warn**. Both are judged the way the
   journey warning already is: exit zero, a warning printed, the phrase present.
2. **Two rows in [`gates.md`](../../method/gates.md#both-gates-are-verified-to-fire)**,
   the method's own table of what to inject: the same two faults, *warns, does
   not fail*. The sentence above it — soft limits produce warnings rather than
   failures — stays as it is. This is its proof, not its revision.
3. **The fault injection record here regenerates.** `checks.py` reads it back
   from `inject.py` and prints the table as it should read; the two rows land
   in it the way every fault since [`0022`](0022-nobody-types-the-record.md)
   has.
4. **The `gate:structure` row in this repository's ledger** says, in its
   evidence, that the soft limits — six rules and 120 lines per file — warn
   and do not fail, and are broken by two faults since this change. The row's
   id, label and state do not move.
5. **Nothing else moves.** Not the limits' numbers, not the id table, not the
   template, not `trace.py`. `gates.md` is on the audit surface, so the pull
   request carries `## Ids` reading *unchanged*.

**Rules added or changed:** none. A repository's own pipeline is held by its
fault table, per [`0045`](0045-five-ids-unreserved.md).

## What we are not doing

- **Not a hard cap on rules per file.** The question asked for one, and the
  answer is no, for the reason `gates.md` already gives and the numbers bear
  out. Small files are the point; a cap is a proxy for it, and the day it bites
  is the day a seventh rule that belongs with its six is exiled to a second
  file to satisfy a number — the file boundary becoming a gate artefact rather
  than a component boundary, which is *satisfying the gate beats telling the
  truth*, the failure case `04` holds a whole skill to. On this machine, read
  on 2026-09-16: 133 feature files across this repository, `toil-tracker` and
  the reference repository; none over six rules; four at exactly six, all in
  `toil-tracker`. The soft limit is already being kept as a ceiling without a
  gate.
- **Not a hard cap on lines either.** Three of those 133 files are over 120
  lines — two in `toil-tracker`, at 124 and 150, one in the reference
  repository at 124 — and a hard cap would fail two real repositories on the
  day it shipped, for files whose length is examples written in the persona's
  terms.
- **Not deleting the warnings.** The method's norm — *a warning surviving two
  versions either becomes an error or gets deleted* — is about a warning being
  emitted and left standing, which is wallpaper; these two have never been
  emitted. The journey warning is the precedent for a warning kind kept on
  purpose because the thing behind it is a judgment, and it has a fault. These
  get the same.
- **Not a new gate id.** The soft limits belong to `gate:structure`, whose
  meaning already is the shape of a feature file; a new id would put a row in
  every consuming repository's ledger for a warning.
- **Not amending the id table's *meaning* column** for `gate:structure`. The
  audit tool's registry mirrors that column and `checks.py` holds the two equal,
  so a wording change there is two files on the audit surface for no change in
  what is checked. The fault table is where the proof is stated.
- **Not moving the numbers out of `trace.py`**, and not asking where the
  template and `refine-spec` got theirs. Six and 120 are this repository's
  bindings, in the script that reads them; that the skill body quotes the same
  figures as a default is older than this spec and not touched by it.

## Data

No storage. Three files move — `inject.py` by two entries, `method/gates.md`
by two rows, `specs/setup/README.md` by two generated rows and one sentence —
and this spec. `method/` moves, so the change ships: **`patch`** — the method's
judgment is unchanged and its proof is extended — a `## Changelog` section, and
`## Ids` reading *unchanged*. No `.feature` moves, so no Gherkin block; no
skill or case moves, so nothing on the board goes stale that is not already.
`verify.py` exits **2** on the spec commit and on the implementing commit, for
the rows already owed and no other reason.

## Risks

- **A warning fault that passes for the wrong reason.** A fault is judged on
  exit zero, a warning printed *and* the phrase *soft limit* in the output, so
  a different warning cannot stand in for it, and the fixture as it stands
  warns for nothing.
- **Somebody reads two new rows as the limits becoming hard.** Both rows read
  *warns, does not fail*, in the same words as the journey row, and the
  sentence above the table is unchanged.
- **A consuming repository's next audit.** The changelog entry says where to
  look; the two faults are wiring for that repository's own injector, offered
  by its sitting. Nothing fires unasked.

## Acceptance checks

1. `python3 .github/scripts/inject.py`: 96 faults caught, the two new ones
   reading *warns*; a fault made into a no-op is still reported as not firing.
2. `checks.py` green with the regenerated record; `gates.md`'s table carries
   the two rows; the `gate:structure` row here reads as written above.
3. `verify.py` exits 2 for the rows already owed and nothing else.
4. `grep -c "soft limit" .github/scripts/inject.py method/gates.md specs/setup/README.md`
   finds both faults in each of the three.

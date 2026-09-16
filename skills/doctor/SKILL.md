---
name: doctor
description: Re-audit the gate wiring in a repository that already has this process — check every claim its bindings make against what owns the answer, reading branch protection and required checks back from the platform rather than from CI config, and print what is still open. Use when asked to check or audit the gates, to say whether the process still holds here, when a bindings claim looks like nobody verified it, or when a ledger row has been deferred too long. Corrects the record, never the wiring — building what is missing is setup.
---

# Audit what the wiring here actually claims

A gate wiring ledger is typed by a person, once, usually at the end of a long
sitting. Then it is trusted forever. This skill is the second reading — and
the second reading is held to a list, so that what it skipped is as visible as
what it found.

**It changes the record and never the wiring.** A row that overstates gets
corrected; a gap gets a row. Building what is missing is
[`setup`](../setup/SKILL.md), and a skill that both audits the gates and builds
them has no way to be wrong out loud.

## 0. Run the tool first. It owns the list.

```sh
python3 "$CLAUDE_PLUGIN_ROOT/tools/doctor.py" specs/setup/README.md
```

If `$CLAUDE_PLUGIN_ROOT` is not set, it is `tools/doctor.py` two levels up from
this file. It prints **the record**: one line per check the method names — the
list is [the id table in `gates.md`](../../method/gates.md#the-ids), and it is
enumerated nowhere else — with a state from `clear · open · n/a · unanswered`
and the evidence beside it. **Save what it printed to a scratch file** — not
over the path the bindings name as the audit record, which is the previous
run's and is what the next pass compares against — and work in that file. The lines marked *script* are answered: the stamp
and the range between it and the plugin installed, every row's state and
evidence, the clocks, the tables the method requires, the skill names the
record instructs by. They are answered the same way every time, from the
record and never from the product, and every one of them is broken on purpose
in this plugin's own checks. **Do not re-derive them, and do not argue with
them from memory of the ledger** — the line says what it read and where.

Where it exits **3**, there are no bindings: this repository has never had the
process set up. Say that in one line and stop; `setup` is what it needs, and
offering it is the whole reply.

Where `check:ledger-shape` reads *open*, the ledger predates the template.
The tool has matched what it can by alias; the lines that needed the tables
say so instead of guessing. Carry on with the rest, and see §2.

## 1. Answer the lines marked *unanswered*. Every one.

Each carries the id, the question, and **the command the bindings name** —
read from the row's own *read back with* column, the boundary row's *what
starts it*, the coverage row's config. For each:

1. Run the command shown, or read what it points at. **The tool printed it
   and did not run it** — a bindings cell is text somebody typed, and the
   running is yours, under the person's permission prompts.
2. Replace `unanswered` with one of `clear · open · not-read`, and put beside
   it the first line of what came back, or why it could not be run.

A line that could not be read is `not-read`, with why — no credentials, no
network, no permission. That is a legitimate answer and it validates.
**Silence does not.** A run that leaves a line `unanswered` has not finished,
and §3 will refuse to let it end. An `open` line ends with what closes it; a
`clear` or `open` judgment keeps the command it was answered by beside the
result.

Where a row names no command — a claim about the platform with nothing after
it — the line already says so: the row must name one, and that is a
correction to the record, not a reason to guess. **Handing a line to a subagent
is taking the step, not a way around it**: a second session has the same
tools and returns the same nothing where this one cannot reach the platform.
Once establishes it; write `not-read` and carry on.

The questions worth the judgment, and what decides them:

- **What a row leaves uncovered** (`check:row-uncovered`). The tool lists what
  the tree is made of — languages by manifest, top-level packages, the
  services the dependencies reach — beside what the rows name. A gate wired
  over one language of two, one package of five, is not a gate over this
  repository; a service the dependencies reach that no boundary row names is
  a boundary nobody wrote down. Say which part has no gate.
- **The number** (`check:number-from-config`, `demand-is-a-ratchet`,
  `exclusions-in-config`). Open the config the coverage gate reads and report
  the demand in it, not the row's description of it. A demand equal to what
  the code scores today was measured rather than chosen — a ratchet, with
  zero slack by construction — **unless it is the whole of what is in scope**,
  which equals the score by construction too and is what `setup` recommends.
  What the demand does not reach belongs in the tool's own config; a list only
  the bindings know is a second copy of the gate. Correct the row and leave
  the number — a threshold is wiring.
- **The boundaries** (`real-starts-here`, `real-not-doubled`,
  `fake-suite-green`). A *real* row over a world the tests never enter is the
  false green the table exists to stop, and it reads exactly like a true one.
  Start what the row names; run the traceability gate and read it for
  doubles. The tests are the authority on what they reach, the way the tree is
  on what applies: a *real* row the tests contradict is corrected to *mocked*,
  naming the tests; a *fake* row with no suite behind it is a mock whatever
  the row called it. A thing that cannot be started from here is `not-read`,
  and a row is not corrected on that evidence alone.
- **The platform** (`merge-blocked`, `check-name`, `who-bypasses`,
  `credentials-present`). A check named in a CI config is evidence that
  somebody wrote it down and no evidence that a merge is blocked when it
  fails; on more than one platform those are separate settings, and one is a
  project-wide switch nobody reading the pipeline file would see. Read them
  back with the command the row names: is the merge blocked, what is the
  check called as the platform has it, who can bypass including the tokens a
  pipeline uses, and is a credential the bindings call missing in fact
  present one level up.
- **The range** (`entry-moved-here`). The tool lists the entries between the
  stamp and the plugin installed, and the ids that arrived in them. Read each
  entry for *where to look*, never as a list of tasks: what it asks of this
  repository is read from `gates.md`, [`claude-md.md`](../../method/claude-md.md)
  and the skill as they now stand. An entry that is mostly reasoning asks
  nothing the method does not; one that moved nothing this repository holds
  is passed over in a line. A row that was right under the stamp's version
  and is not right now announces nothing — present, accurate, and stale —
  and having been correct when written is not a reason to leave it.
- **The names** (`word-not-a-skill`, `loop-per-claude-md`). The tool has
  already flagged an instruction — `/livespec:<name>` — by a name this plugin
  no longer has, with the name it now has. What it hands you is the rest: an
  old name in prose, which is an instruction to correct or a dated account to
  leave as written; the same word as ordinary prose, to be left alone —
  reporting one is how this check becomes noise on its second run — and the
  loop's own account, read against what `claude-md.md` now asks of each step.
- **The prose** (`prose-phrases`). The tool lists every *not built yet*,
  *to do*, *we should*, *for now* with its line. Each is a row on the clock or
  it is nothing — *nothing to do at release time* is nothing — and that is
  yours to say, not the script's.
- **What ran** (`gate:skipped-test-claims-nothing`, `gate:fewer-ran-than-exist`).
  A row reading *automated* names how the runner reports per test and what
  counts as a marker here; it reads *unobserved* until somebody has skipped a
  rule-bound test and watched the gate refuse it. A bindings sentence saying
  the runner cannot report per test is a decision to leave as written, with
  what it leaves open beside it.

## 2. Correct the record — and only the record

Write the corrections in place: the bindings, `CLAUDE.md`, and nothing else.
`check:record-only` reads the working tree and says so if anything strayed.
Show each row as it will read, then write it. Where the ledger predates the
template, **write the id the tool matched into each row** — that is record —
and leave the columns where they are: `--reshape` prints the tables in the
template's shape for the sitting to apply, and the sitting is `setup`'s.

- A row that claims more than was wired is corrected to what was. A row that
  reads *not applicable* and is contradicted by the tree becomes what the tree
  says; a row marked `decided:` is a choice, and is not re-litigated.
- Wiring the method now asks for and this repository lacks becomes a row
  reading *deferred* — since which change, naming the version of the method
  that moved it — so it is on the two-change clock rather than in a report.
- A row deferred across two changes is either wired or written off — written
  off is *not applicable* with the reason in it. A *mocked* boundary row past
  the clock is the same: real, given a suite, or *unreachable* with the reason.
- A gap the prose names — *not built yet*, *to do*, *we should*, *for now* —
  is a row or it is nothing; the tool listed every hit.
- A `CLAUDE.md` out of line beyond its lines — a requirement missing, the
  plugin's own rules copied into it — is **not rewritten here**. Correct the
  lines that are record, a loop step or a skill name, and leave
  `check:loop-per-claude-md` open with the rewrite as what closes it and the
  sitting as whose it is. The audit changes the record; a new file is the
  sitting's kind of change —
  [`claude-md.md`](../../method/claude-md.md#when-it-is-out-of-line).
- **Re-stamp only if the wiring moved.** The stamp follows the wiring and never
  the reading; a ledger re-stamped for an audit that changed nothing has
  learned to lie.

## 3. Let the tool decide whether the audit is finished

```sh
python3 "$CLAUDE_PLUGIN_ROOT/tools/doctor.py" --validate <the scratch file>
```

It refuses the record — exit 1, naming the line — if any id is missing, any
line still reads `unanswered`, any state is off the vocabulary, an `open` line
names nothing that closes it, a `not-read` line gives no reason, a judgment
reads `clear` with no command beside it, or the working tree changed anything
but the record. **A refused record is an audit that has not finished**: go
back to the line it names. Nothing else is a way through — not a paragraph
explaining the gap, not a subagent, not a second scratch file.

Where it accepts the record, it answers the four lines the reply generates,
**writes the record at the path the bindings name** — replaced on every run,
each line carrying the date it last changed state, so the next audit can say
what opened and what closed — and prints **the reply**. That reply is the
hand-back, verbatim, with nothing after it:

- what is open, sorted by the severity each id carries — *platform*, then
  *boundary*, then *wiring*, then *record*; a row asserting a protection the
  platform does not enforce outranks a deferral one change old, every time;
- then what was not read, with why — a row that was checked and a row that
  was assumed never come out looking the same;
- then the decisions, once — the rows marked `decided:` — with the tree's
  contradiction, where there is one, offered as evidence and not argued;
- then, only where an open line names wiring, `/livespec:setup` and the rows
  the sitting will be asked to wire, one per line. Where nothing is left for
  the sitting, no such line, and nobody is sent to a sitting nobody needs.

Commit the record with the corrections. The same last line closes the
reading's record in the bindings. Anybody who only wants the answer — a
grader, a reviewer — asks `--check <record>` instead: the same exit, and
nothing written.

## What this skill refuses

- **Wiring anything.** Not a gate, not a report, not a threshold — including
  the one it just found is wrong. It writes the record; `setup` writes the wiring.
- **Running a command it read from the bindings itself.** The tool prints
  them; the running is a mind's, under the person's prompts.
- **Starting the sitting.** The last line says what to type and does not run it.
- **Reading an entry as a task list.** The entry is where to look.
- **Re-stamping for having read.** The stamp follows the wiring.
- **Leaving a line `unanswered`.** `not-read` with why is an answer; a blank
  is a check nobody made, and `--validate` will not let it end.
- **Handing back without the record.** The reply is what pass two printed;
  a reply recalled from the session is the thing this skill exists to stop.
- **Writing application code**, which no skill here does.
- **Running the interviews.** An empty layer is `setup` section 8's.
- **Flipping every row to *unobserved* to be safe.** A row somebody watched
  fire stays *automated*.
- **Reading a green pipeline as an answer about the platform.** A build that
  passed says the job ran, nothing about what happens when it fails.
- **Auditing a repository that has no bindings**, rather than saying so and
  offering `setup`.

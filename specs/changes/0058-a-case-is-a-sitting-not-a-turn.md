# Spec 0058: a case is a sitting, not a turn

- **Status:** approved
- **Issue:** [#133](https://github.com/sargismarkosyan/livespec/issues/133) —
  the harness grades one turn of what is a sitting: nobody answers the
  session's questions, and 44 of 46 cases have no shell. Found 2026-09-18 by
  reading the sitting's verdicts beside 61 real sessions in the repository
  the maintainer holds up as the plugin working. Three findings ride with it
  and are answered here: [#131](https://github.com/sargismarkosyan/livespec/issues/131),
  a judge that errors is scored as the agent failing;
  [#132](https://github.com/sargismarkosyan/livespec/issues/132), rubrics that
  pass on inaction — the three on the flagship that are hatches; and
  [#134](https://github.com/sargismarkosyan/livespec/issues/134), `setup`
  stopping for a go-ahead the request already gave.
- **Depends on:** [`0057`](0057-a-measurement-names-its-model.md), which pins
  the model and makes `provider.py` a staling event, so that the sitting this
  earns is paid once and on the right model; and
  [`0054`](0054-a-case-names-the-world-it-runs-in.md), whose lesson this is
  again — the world a case runs in is part of what it measures — for two more
  parts of the world: the person on the other side, and the tools in the room.

## Who this is for

**Nobody in the workflows, and that is correct rather than a gap** —
[`process.md`](../../method/process.md#a-technical-change-that-serves-no-workflow-is-correct-not-a-gap).
This is the repository's own pipeline. The person it serves is the maintainer
at step 4, who asked *why are the evals low* and was told, correctly, that the
suite cannot carry the sitting the skills are built for. The method paragraph
is for any repository whose product interviews: a graded case of a thing that
asks measures its first question unless the case brings the answers.

**This lengthens nothing anybody types.** A case that needs a person gains a
file saying what that person knows; a case whose skill runs a tool gains two
lines naming the commands it may run and the binaries it needs. One sentence
lands in `setup`'s first section.

No always-promise moves. `never-implements`: nothing here writes application
code; the shell a case is lent runs the fixture's own gates.

## The job behind the request

The literal ask is the issue's: give the session someone to answer it and a
shell to run its tool. Behind it is the shape of the number the suite has been
producing. **The skills are sittings, and the harness grades a turn.**

What the reference does, in the maintainer's own repository, read from its
transcripts: `setup` surveyed for twelve to fifteen assistant messages, listed
what it would write, stopped, and the human typed *"Go, and yes rename the
spec to specs"*; the sitting then ran to forty-one turns and about a thousand
messages, three interviews included. Every `doctor` sitting used the shell
between sixteen and 121 times — `npm run`, `git`, its own `doctor.py`. Every
`record-clip` served the app from the shell and drove a browser.

What the harness does, in [`provider.py`](../../evals/runner/provider.py):
one `claude -p` call, text in, one result out; `--disallowedTools Bash` on
every case but `40` and `44`; `--strict-mcp-config` with no config, so no
browser either. `caselib.py`'s comment promises *transcript replay*; nothing
implements it.

What that produced, plugin arm, the sitting of 2026-09-17/18:

| case | what the skill did | what the harness did | the number |
|---|---|---|---|
| `12-setup-drives-the-sitting` | surveyed, listed what it would write, asked its six questions — *"Answer what you can… and I'll start"* — exactly as it does in the reference | ended the session; six of ten graders judge what comes after the answers | 0/3 on those six, **both arms**; −0.07 |
| `41-history-that-still-binds` | the same stop | the command grader: *"the sitting wrote no bindings"* | 2 of 2 completed sessions |
| `24-a-ledger-nobody-read-back` | `python3 $CLAUDE_PLUGIN_ROOT/tools/doctor.py`, the skill's line one | Bash denied; Monitor refused; the hand-back is the blocker | 8 of 9 failures cite the shell; −0.08 |
| `16-setup-with-no-app-code` | decided the testing story instead of asking; could not reach `claude plugin eval init` | no one to ask, no shell to reach with | 0/3 on both graders, both arms |

Of the ninety plugin-arm grader failures in the sitting, twenty-two cite the
missing shell in the judge's words, about forty-one are `setup` asking with
nobody to answer, twelve were case 08's rider — fixed by
[`0055`](0055-a-rider-is-filed-not-served.md) — and one is a judge that
returned nothing, scored as if the agent had failed. The daily loop the
reference actually runs — todo, refine-spec, the sketch, record-clip — scores
+0.17 to +1.00 wherever the harness can carry it. The twenty-five `setup` and
`doctor` cases hover at zero, and they are twenty-five of forty-six.

Three smaller things were built for the one-turn world and hold it in place.
**A judge that errors three times is scored as a FAIL** — nine verdicts in the
sitting, seven of them in one arm of one run, moving that run's Δ by a harness
accident. **Three of the flagship's rubrics pass on inaction** — *PASS also if
no report was wired and the hand-back said so* — which in a harness with no
shell was the best honest outcome, and which the bare arm collects by saying
the same sentence. And **`setup` stops for a go-ahead it was already given**:
its first section reads *"go ahead"* as an answer to the list, never as one
given in advance, where cases `26` and `43` already grade an advance yes as
covering setup's own files and never a hand-written one.

The job: **a case may bring the person and the room its skill assumes, the
harness drives the sitting, and what could not be judged weighs nothing.**

## Why now

Because `0057` stales every row and one sitting will be paid to heal the
board. It should be the sitting the skills are built for, on the model the
bindings name, with verdicts worth reading — not a third measurement of the
stall. And because the maintainer asked for confidence rather than numbers,
and confidence is a harness that can reach the judgment.

## The end value

A case directory may hold a `person.md`; the runner answers the session's
questions from it, in the human's voice, for a bounded number of rounds, both
arms alike, and the judge reads the questions and the answers. A `case.yaml`
may name the commands its shell allows and the binaries its fixture needs; the
runner confines the shell to that list and refuses, before spending, a case
whose machine lacks a binary. A verdict the judge never returned is left out
of the fraction, and the summary says how many. The four cases the verdicts
convicted carry what they need. `setup` says its list and continues when the
request already said to. The method, the README and the bindings say what a
sitting is.

**How we would know it worked:** two new faults read *fails*; the stub-driven
test drives two rounds through the provider and finds the person's reply in
the transcript; `run.py` over the fourth run's `results.json` prints *1
verdict errored, excluded*; and in the first sitting after this lands, `12`'s
plugin sessions write bindings after the person says *go*, `24`'s run
`doctor.py`, and `16`'s ask what proves a rule and are answered.

## What changes

1. **[`caselib.py`](../../.github/scripts/caselib.py)** reads `person.md`
   beside the case's prompt — frontmatter `replies:` (rounds after the first;
   2 when the file exists and says nothing), body the sheet — into
   `case["person"]` and `case["replies"]`; and reads `shell:` and `requires:`
   from `case.yaml` into two lists. The one reader, so the gate and the
   runner cannot disagree about what a case brought.
2. **[`provider.py`](../../evals/runner/provider.py)** runs the session with
   `--input-format stream-json` and keeps its stdin. The prompt is the first
   user message. After each `result` event, while the case has a person and
   rounds remain, the person is asked — the judge model, held to
   `{"reply", "done"}` by `--json-schema` — with the sheet, the session's
   final text, and one standing instruction: *you are the human; answer only
   from the sheet, in a few lines; a fact the sheet does not hold is "your
   call"; if nothing is asked, or the work is done, say done.* Done closes
   stdin; otherwise the reply is the next user message. **The sheet answers;
   it never volunteers** — a fact the session never asks for never reaches it,
   which is what keeps `16`'s question gradeable. Each reply is appended to
   the transcript as a `person` line and priced through the ledger `0057`
   gave the judge. `max_turns` applies per round, as the CLI applies it;
   `timeout_seconds` bounds the sitting. Both arms alike, or Δ compares two
   questions. Checked on 2026-09-18 for two cents: several user messages in
   one process, one `result` each, no persistence and no `--resume`.
3. **The shell**, in the same file: each `shell:` entry becomes an
   `--allowedTools` rule, `Bash(<entry>:*)`, and `Bash` leaves the case's
   disallowed list; an unmatched command is refused in headless mode, which is
   what keeps `gh` and `curl` out. Where the machine has Claude Code's own
   sandbox, the runner turns it on for the session with the network closed,
   as a second wall; where it has not, the run says so in its first lines. A
   case with no `shell:` runs exactly as today.
4. **[`asserts.py`](../../evals/runner/asserts.py)**: `_digest` renders the
   `person` lines as `PERSON:` so a full-transcript judge sees the question
   and the answer; an errored verdict carries `"errored": true` beside its
   reason.
5. **[`run.py`](../../evals/runner/run.py) `collect()`** takes each session's
   score from its `componentResults` — the fraction over the graders that
   returned, weightless indicators and errored verdicts left out — rather than
   from promptfoo's `score`; a session no grader returned for is an error; the
   summary prints how many verdicts errored. `record()` reads the same numbers.
   And `run.py` checks every selected case's `requires:` with `shutil.which`
   before it compiles anything, refusing with the case and the binary named:
   a missing `pytest` is a refusal, never a measurement of its absence.
6. **[`evalsuite.py`](../../.github/scripts/evalsuite.py)** fails a
   `person.md` with no body, and a `shell:` entry that names something that
   leaves the machine — `gh`, `curl`, `wget`, `ssh`, `scp`, `git push`, `git
   fetch`, `npm publish`, `pip install`. **[`inject.py`](../../.github/scripts/inject.py)**
   proves both; 117 becomes 119.
7. **The four cases.** `12`: a `person.md` in Priya's voice with the six
   answers the prompt's repository implies — what the service is and that a
   version's deliverable is a test run and a changelog line, who it is for,
   `make test` and the coverage scope, the database as its one boundary, the
   GitLab tracker, and *yes* to the list and to a pre-push hook; `shell:
   [python3, python, make, git, ls, cat, pytest]`; `requires: [python3, make,
   pytest]`; its scaffold initialises a git repository, which the hook
   question needs — the sitting's last words were *there's no git repo*; and
   its three report rubrics lose the *hand-back said so* clause, which the
   sitting no longer needs (#132). `16`: a `person.md` whose sheet
   holds the answer to what proves a rule here — and nothing else, so the
   question still has to be asked; `shell: [ls, cat, claude plugin]` so the
   generator can be reached and found gated; `requires: [claude]`. `24`: no
   person — an audit answers to the tree — and `shell: [python3, make, git,
   ls, cat, pytest]`, `requires: [python3]`; its `case.yaml` note that *the
   session is granted no Bash* is rewritten, because the remote still does not
   exist and the required-check row is still the claim nothing here can
   settle: the case grades the same thing, now with the tool running. `41`: a
   `person.md` with *go* and sluicegate's six answers; the same shell and
   requirements as `12`.
8. **[`skills/setup/SKILL.md`](../../skills/setup/SKILL.md) §0**, one
   sentence after *Then wait* (#134): an instruction in the request to write
   without checking back is the answer to this stop, given in advance — the
   list is still said, in the same message, and the sitting continues. It is
   not an answer to section 2, whose six are facts only they have, and it
   never covers replacing a file somebody wrote by hand. `26`, `41` and `43`
   already grade it that way; `09`, which gives no such instruction, still
   grades the stop. The rule `09` claims, `setup-confirms-before-writing`,
   gains the example that says so — see *Rules* below.
9. **[`method/graded-cases.md`](../../method/graded-cases.md)**, two
   paragraphs under *The session is part of what you measure*. **A case of
   something that asks must bring the answers**: a product that interviews,
   measured over one turn, measures its first question and nothing after it;
   give the case the person it would have had — what they know, in their
   voice, answering only from that and only when asked — for a bounded number
   of turns, in every arm alike, and keep what they said beside what the
   product said, because the judge has to read both. **And the tools the
   product runs are part of the room**: a case that denies them measures the
   refusal, and a case that lends them says which and confines them to the
   fixture. No runner named; it survives a repository with pytest.
10. **Words.** [`evals/README.md`](../../evals/README.md): a section *When a
    case needs a person*; the *No case grants Bash* paragraph replaced — a
    case may, confined to the list it names, nothing that leaves the machine,
    `requires:` checked before a cent is spent, `pytest` a maintainer-machine
    prerequisite the way node is; the floor's tool bullet updated;
    *Calibration* names the errored-verdicts line; the flagship's paragraph
    says ten graders and nine rules, which is what it carries. **This
    repository's bindings**: the *Case discovery* row names the three new
    fields; the runner paragraph names the rounds and the shell; *Fault
    injection* counts 119.
11. **`tests/test_runner.py`** grows against
    `0057`'s stub: a session whose first result asks a question and a person
    who answers once, then says done — two rounds, the person's line in the
    transcript, the second user message sent; a `shell:` list becoming
    `Bash(python3:*)`; a `requires:` the machine lacks refusing before the
    config is written; an errored verdict left out of the fraction.

**Rules changed: one example, no new id.** `setup-confirms-before-writing`
(`specs/features/setup/`) gains *Example: the request already said to write* —
given a request that says to write without checking back, when setup answers,
then it names the files it would write and continues into them in the same
sitting, and a file somebody wrote by hand is still not replaced. Nothing else
in the rule moves; `a-rewrite-lands-only-on-a-yes` already reads an advance
yes this way. The pipeline's own changes carry no rule id; the faults and the
test are their contract.

## What we are not doing

- **Not a browser.** `08` and `22` grade the judgment around a recording, and
  their sessions already say the recording itself is impossible here. A
  browser in a headless eval is a served app per case and a spend per frame;
  a later spec, if the verdicts say the judgment is not enough to hold.
- **Not sweeping the other forty-two cases.** The README's rule for scaffolds
  holds for persons and shells: convert as runs demand it. The first sitting
  with these four says which are next, and its verdicts are read before the
  next four are written.
- **Not the other thirteen rubrics in #132.** Read: `29`'s clause is the
  rule itself, `22`'s and `30`'s are real alternative outcomes, `16`'s and
  `17`'s are the fallback the method itself names when a tool is gated. The
  three on `12` are hatches and go; the issue stays open for the sweep's
  reading of the rest.
- **Not splitting the flagship.** With a person and a shell its ten graders
  are reachable in one sitting. It is cut in two on the day a sitting proves
  it cannot hold them, not before.
- **Not the three skill gaps** —
  [#135](https://github.com/sargismarkosyan/livespec/issues/135),
  [#136](https://github.com/sargismarkosyan/livespec/issues/136),
  [#137](https://github.com/sargismarkosyan/livespec/issues/137). Each is a
  skill edit that re-stales cases; each waits for a harness that can measure
  what it changes, which is this.
- **Not a person with opinions.** The sheet is the whole of what it knows and
  *your call* its only improvisation. A person who improvises is a second
  model under test.
- **Not re-measuring anything here.**

## Data

No storage. Files that move: `.github/scripts/caselib.py`,
`.github/scripts/evalsuite.py`, `.github/scripts/inject.py`,
`evals/runner/run.py`, `evals/runner/provider.py`, `evals/runner/asserts.py`,
`tests/test_runner.py`, `skills/setup/SKILL.md`, `method/graded-cases.md`,
`evals/README.md`, `specs/setup/README.md`, four case directories — `12`,
`16`, `24`, `41` — gaining `person.md` or `shell:`/`requires:` lines and, on
`12`, three edited rubrics, and this spec.

**This spec commit stales nothing.** `verify.py` exits **2** for the rows
already owed and no other reason.

**The implementing change stales what `0057` already staled**, and would have
staled on its own: every `setup` case through the skill body, the four cases
through their files, every row through the harness fingerprint. Nothing new
is owed by it; the one sitting after both is the same sitting.

**What that sitting costs.** The three cases with a person run up to two
rounds more per session than today, on eighteen sessions, at Sonnet prices;
the estimate `0057`'s refusal prints will carry it. The first run is a pilot
at `--runs 1` on `12`, `16` and `24`, read verdict by verdict — the
calibration the README has owed since `0012` — before the floor is paid for.

**What the pull request owes.** `skills/` and `method/` move and `setup`'s
judgment changes in one case — **`minor`**; the description does not move — a
`## Changelog` section, the Gherkin block for the example, and the run block.
The audit surface does not move.

## Risks

- **The sheet answers the question the case grades.** `16`'s sheet holds the
  answer to *what proves a rule here*; if the session never asks, the answer
  never arrives and the grader still fails it. The rule — the sheet answers,
  never volunteers — is what makes a person safe to add to a case that grades
  asking, and it is written where the next author reads.
- **A round runs away.** `max_turns` is per round and `replies` bounds the
  rounds; `timeout_seconds` bounds the sitting. A person who cannot say *done*
  is a sheet worth rereading.
- **The allow-list is not a sandbox.** `python3 -c` can open a socket. The
  list keeps the obvious exits out, the fixture is a throwaway under `/tmp`,
  and Claude Code's own sandbox closes the network where the machine has it;
  where it has not, the residual is named at the top of the run rather than
  assumed away.
- **The person's model has a voice.** It is the judge's model, bounded by the
  sheet; what it adds is tone, and the tone is graded by nobody.
- **Always-promises.** `always-green`: unchanged. `never-implements`: the
  fixture's own gates run; nothing is written but prose, scripts and tests.
  `context-budget`: no description moves.

## Acceptance checks

1. `python3 .github/scripts/inject.py`: 119 faults caught — the empty sheet
   and the entry that leaves the machine both reading *fails* — the fixture
   green.
2. `python3 .github/scripts/tests.py`: `test_runner.py` green — two rounds
   through the stub, the person's line in the transcript, `Bash(python3:*)`
   on the command line, the `requires:` refusal, the errored verdict left out.
3. `run.py`'s `collect()` over `evals/results/20260918-084138/results.json`
   prints *1 verdict errored, excluded*, and the bare arm of the case it fell
   in changes by exactly that verdict.
4. The first run after landing, with the maintainer's yes: a pilot at
   `--runs 1` on `12`, `16` and `24` on `claude-sonnet-5`; in its transcripts
   the person's replies appear after the questions, `12` writes bindings after
   *go*, `24` runs `doctor.py`, `16` asks and is answered — read verdict by
   verdict before the floor run is approved.
5. `verify.py` exits 2 for the board only; the pull request carries `minor`,
   `## Changelog`, the Gherkin block and the run block.

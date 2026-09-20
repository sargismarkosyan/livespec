# Spec 0061: one refusal is the answer, and the id goes into the row as it stands

- **Status:** proposed
- **Issue:** [#142](https://github.com/sargismarkosyan/livespec/issues/142) —
  `doctor` retried a refused platform command three times and reshaped the
  ledger the tool had told it to leave, in both Sonnet sittings with a shell
  (`evals/results/20260918-180217` and `20260919-014104`, case `24`, plugin
  arm) — the first two times the skill has run its tool inside the suite.
- **Depends on:** [`0058`](0058-a-case-is-a-sitting-not-a-turn.md), which lent
  the case the shell the tool needs and so made the two findings visible;
  [`0041`](0041-an-audit-that-cannot-stop-early.md), whose tool owns
  the list and prints the `--reshape` hint this sitting read as an
  instruction; and the sitting of 2026-09-20, which measures the skill as it
  is at the floor.

## Who this is for

[`agent-accelerated-owner`](../personas/agent-accelerated-owner.md), in
[`adopt-the-process`](../workflows/adopt-the-process.feature), at the audit —
the step that re-reads the record when they cannot. The fixture's owner has a
ledger that reads *automated* on every row, a remote that resolves to no
host, and a session with no `gh`. What they need from the audit is a record
that says which rows nobody can read from here and who can. What they got,
twice, was a session asking the platform four times for an answer it had been
refused once, and a ledger rebuilt into the template's shape with the narrow
correction the tool had suggested lost inside it.

**This lengthens nothing anybody types.** Three sentences move or arrive in
one skill body. No always-promise moves; the description does not move.

## The job behind the request

Three findings, one shape: **the skill says the right thing once, in a place
the session has read past by the time it matters.**

- *"Once establishes it; write `not-read` and carry on"* is the last clause
  of a paragraph about handing a line to a subagent. A session whose own
  permission prompt has just refused `gh auth status` is not reading about
  subagents; it reads a refusal as a wrong invocation and tries the command
  alone, then again, then again. The judge: *did not stop at one no — it
  issued three more separate Bash calls all invoking `gh auth status` alone
  (denied each time)*; and on the second sitting, after `git remote -v` had
  already shown a host that resolves to nothing, *still repeatedly tried to
  reach the platform*.
- *"Write the id the tool matched into each row … and leave the columns where
  they are: `--reshape` prints the tables in the template's shape for the
  sitting to apply"* is in §2. By then the tool's own record has printed
  `--reshape` as a hint beside the alias matches, and a hint from the tool
  reads as an instruction from the tool. Both sittings rebuilt the three
  tables; the rule `old-rows-are-matched-by-alias` says the columns are not
  moved by the audit, and its grader read 0 of 1 each time.
- *"If `$CLAUDE_PLUGIN_ROOT` is not set, it is `tools/doctor.py` two levels up
  from this file"* is the sentence after a command block that uses the
  variable. The variable is not set in a headless session, so the first
  command fails on an empty path, and a session with a failed command goes
  looking — `printenv`, `env | grep`, `python3 -c "import os; …"`, `find /
  -iname doctor.py`; eight commands across the two sittings — before it reads
  the next sentence.

The job: **the refusal is the answer, said where the refusal happens; the
reshaping is refused where the skill lists what it refuses; and the path is
given before the variable that may not be set.**

## Why now

The sitting of 2026-09-20 measures `doctor` as it is, at the floor, on `24`
and the ten other doctor cases; its verdicts are the before. This lands
after, so the after is one change.

## The end value

An audit refused a platform command once writes `not-read — refused here` on
that row, names who can read it — a person with the platform's rights, the
token the pipeline has — and carries that name into the reply; it does not
ask again. It writes the matched id into each row and leaves the three
columns where they were, and ends with the command that starts the sitting,
which is where the reshaping happens. And it runs the tool from the path the
skill hands it before it looks for a variable.

**How we would know it worked:** in the first sitting after this lands,
`24`'s plugin arm runs at most one refused platform command, its transcript
has no `find` for the tool, the ledger keeps its shape with the ids written
in, and `a-claim-outside-the-tree-is-read-back` and
`old-rows-are-matched-by-alias` pass — 0 of 1 each on 2026-09-19.

## What changes

1. **[`skills/doctor/SKILL.md`](../../skills/doctor/SKILL.md) §0**: the path
   comes first. The tool is `tools/doctor.py` two directories up from this
   skill file — the harness said where it loaded this file from —
   and `$CLAUDE_PLUGIN_ROOT`, where it is set, names the same place; the
   command block reads with that order, and one sentence says the tool is
   never searched for: a session running `find` for it has not read this line.
2. **§1**, a paragraph of its own after *Once establishes it*: **a command
   this session's permissions refuse is the same nothing, and one refusal is
   it.** The line becomes `not-read — refused here`, naming who or what can
   read it — a person with the platform's rights, the token the pipeline has
   — and the reply carries that name. The same command again — alone, in
   pieces, in a subagent, after a `git remote -v` that already showed the
   host is not there — is a retry of a no, and the record is not improved by
   it. The rule `a-claim-outside-the-tree-is-read-back` already has the
   example — *the platform cannot be reached from this session: the row says
   it was not read back, and why* — so no Gherkin moves.
3. **§2**: the sentence about the id and the columns is set in bold and
   given the reason: the tool's `--reshape` hint is printed for the sitting
   the reply names, and this audit is not that sitting.
4. **What this skill refuses** gains two bullets. **Reshaping the ledger**:
   the id goes into each row as it stands and the columns stay where they
   were, however far from the template; `--reshape` is the sitting's, and the
   reply ends by naming it. **Asking the platform twice**: one refusal is the
   answer, and the reply names who can get a different one.

**Rules changed: none.** Both rules `24` claims already say what the audit
leaves behind; this changes where the skill says how, and how loudly.
`skills/` moves, so the change ships: **`patch`**, and the description does
not move.

## What we are not doing

- **Not changing the tool.** `--reshape` stays a hint the tool prints; the
  skill is what reads it as one.
- **Not setting `$CLAUDE_PLUGIN_ROOT` in the harness.** A consuming
  repository's headless session does not have it either; the skill has to
  work without it, and the case measures that.
- **Not touching the three graders `24` carries for the reply**, which the
  second sitting never reached: the turn budget was the harness's, and
  [`0058`](0058-a-case-is-a-sitting-not-a-turn.md)'s follow-up raised it.
- **Not re-measuring anything here.**

## Data

No storage. Files that move: `skills/doctor/SKILL.md`, and this spec.

**This spec commit stales nothing.** `verify.py` exits **2** for the rows the
sitting of 2026-09-20 is healing and no other reason.

**The implementing change stales the eleven `doctor` cases**, through the
skill body in their inputs hash — and lands after the sitting has measured
them, so that the before exists. `--changed` then selects exactly those.

**What the pull request owes.** `patch`, a `## Changelog` section. No Gherkin
block, no run block. The audit surface moves — `skills/doctor/` is on it —
so the pull request carries an `## Ids` section reading *unchanged*: no id
arrives or retires.

## Risks

- **A refusal that was a typo.** The session reads its own command before it
  writes `refused`; a command the bindings name that fails on a flag is a
  correction to the record, which §1 already says.
- **The bold sentence is read past too.** Then the refusal bullet is the
  second place it is said, and the case says so at the floor.
- **Always-promises.** `never-implements`: unchanged; the audit still writes
  only the record. `always-green`: unchanged. `context-budget`: no
  description moves.

## Acceptance checks

1. The four edits read as above; `verify.py` exits 2 for the board only, the
   doctor cases re-staled; `## Ids` reads *unchanged* and the release gate
   accepts it.
2. In the first sitting after this lands, `24`'s plugin arm runs `doctor.py`
   from the skill's path without a search, refuses the platform once, keeps
   the ledger's columns, and the two rules' graders pass at the floor.
3. The pull request carries `patch`, `## Changelog` and `## Ids`.

# Spec 0079: the file the harness reads

- **Status:** approved — by the maintainer, 2026-10-03
- **Issue:** [#164](https://github.com/sargismarkosyan/livespec/issues/164)

## Who this is for

**Ren — [`agent-accelerated-owner`](../personas/agent-accelerated-owner.md) —
working under more than one harness.** The maintainer runs livespec under Pi
and Codex as often as under Claude Code
([#155](https://github.com/sargismarkosyan/livespec/issues/155), and 0073's
*Who this is for*). Their repository `helios/wf-developer-agents` keeps a
single `AGENTS.md`, because Pi, Codex, Copilot and Claude Code ≥ 2.1.277 all
read it, and there is no `CLAUDE.md` beside it. Nothing about who this is for
moves.

**The workflow is [`adopt-the-process`](../workflows/adopt-the-process.feature).**
- The sitting's context-file step is steps 5–6 of
  [`trusting-the-spec-again`](../journeys/trusting-the-spec-again.md).
- The audit that reads it again happens months later.
- Today, both of those see an empty file in a repository like that one.

## The job behind the request

To keep the one instructions file every harness they use already reads, and
still have livespec hold it to the requirements: a ceiling, a loop, the
commands, the pointer to the bindings.

**What they do today instead** is get no audit of that file at all. In
wf-developer-agents, `doctor` prints *no CLAUDE.md at the root*, and every
check that reads the file reads an empty string. The other choice is to add
a `CLAUDE.md` they decided against, and that is the two-file drift #155 is
about.

## Why now

- **`tools/doctor.py` hard-codes the name.** It reads `root / "CLAUDE.md"`
  once (`context()`), and labels and allowed paths repeat it at about five
  further places. The context-file gates are worded as *the context file*,
  but the template row is **CLAUDE.md ceiling**, and this repository's
  `trace.py` reads `CLAUDE.md` by constant.
- **The cross-harness file is the common case now.** `AGENTS.md` is read by
  every harness the maintainer uses, and livespec reaching repositories run
  under Pi depends on it.
- **It is small and code-level**, and it can land before #155 settles what
  happens when both files exist.

## The end value

A repository whose instructions file is `AGENTS.md` gets the same gates and
the same audit as one whose file is `CLAUDE.md`. Every line names the file it
read, and nothing asks for a second file.

**How we would know it worked:**
- In wf-developer-agents, `doctor` reads `AGENTS.md` and gives
  `check:loop-per-claude-md` a real answer, and the gates fail an `AGENTS.md`
  past its ceiling.
- Here, nothing changes. The bindings name `CLAUDE.md`, and everything passes
  as before.

## What changes

1. **The method, [`claude-md.md`](../../method/claude-md.md).**
   - The page keeps its path, so links stay valid.
   - Its title and opening say *the context file*: whichever instructions
     file the harnesses in use read first, `CLAUDE.md` or `AGENTS.md`.
   - **A short *Which file* section:**
     - the requirements are the same whatever the name;
     - the bindings name the file;
     - where they don't, the file read is the first of `AGENTS.override.md`,
       `AGENTS.md` and `CLAUDE.md` that exists, the order Pi uses;
     - **one file, never two**, because two files are two copies that start
       disagreeing (#155);
     - a repository with both files is read by its bindings row, and what to
       do about the other file is #155's.

2. **The bindings template, [`bindings.md`](../../templates/bindings.md).**
   - A new row: **Context file**, naming the file.
   - **CLAUDE.md ceiling** becomes **Context file ceiling**. The old label is
     still read, so no ledger breaks.

3. **[`tools/doctor.py`](../../tools/doctor.py).**
   - It resolves the context file once: the bindings row, otherwise the
     fallback order.
   - It carries the file's real name through every check, label and
     allowed-path set.
   - `check:loop-per-claude-md` keeps its id, because ids are permanent. Its
     meaning in [`gates.md`](../../method/gates.md#the-checks-an-audit-makes)
     and its messages say *the context file* and name the file read.
   - A repository with no instructions file at all is still told so, now
     naming the three names looked for.

4. **[`setup`](../../skills/setup/SKILL.md) §6.**
   - "Write CLAUDE.md, or audit the one that is there" becomes the context
     file.
   - It reads which file the repository has, and writes or audits that one.
   - It writes the **Context file** row.
   - It never creates a second file beside an existing one.
   - Where there is none, it asks which name the harnesses in use read, and
     recommends one.
   - **[`doctor`](../../skills/doctor/SKILL.md)** names the context file
     where its text says `CLAUDE.md`.

5. **This repository.**
   - `trace.py` resolves the context file the same way.
   - The bindings gain **Context file**: `CLAUDE.md`.
   - The ceiling row is relabelled.
   - The fixture in `inject.py` follows.
   - `tests/test_context_file.py` gains the `AGENTS.md`-only repository and
     the old ceiling label.

6. **The case.** A `setup` case on a repository whose only instructions file
   is `AGENTS.md`, where the audit has reported the context-file rows open.
   The sitting audits `AGENTS.md`, writes the **Context file** row, and
   creates no `CLAUDE.md` (`the-sitting-names-the-context-file`).

**Rules added or changed:**

| Rule id | Feature file | New or changed |
|---|---|---|
| `the-context-file-is-the-one-the-repository-has` | [`features/wiring/which-context-file.feature`](../features/wiring/which-context-file.feature) | new, live since the implementing commit |
| `the-sitting-names-the-context-file` | [`features/setup/which-context-file.feature`](../features/setup/which-context-file.feature) | new, live since the implementing commit |
| `a-context-file-past-its-ceiling-fails-the-build` | [`features/wiring/context-file.feature`](../features/wiring/context-file.feature) | changed: "A CLAUDE.md" → "A context file", id kept |
| `a-context-file-without-its-shape-fails-the-build` | same | changed: the same rewording, id kept |
| `the-ceiling-is-a-number-in-the-bindings` | [`features/setup/context-file.feature`](../features/setup/context-file.feature) | changed: the same rewording, id kept |
| `the-requirements-are-the-only-reference` | same | changed: the same rewording, id kept |

## What we are not doing

- **Both files present.** What a gate should do when `CLAUDE.md` passes and
  the `AGENTS.md` Pi actually reads doesn't is #155's question. Here, the
  bindings row decides which one is read, and nothing more.
- **Renaming `check:loop-per-claude-md`.** Ids are permanent. A retirement
  plus a new row in every ledger would cost more than a slightly stale name.
- **Renaming `method/claude-md.md`.** Every link to it would break, and the
  page's title can say *context file* without that.
- **Other harnesses' file names** beyond the three. A repository using another
  name writes it in the row.
- **Pi's `/livespec:` commands and `$CLAUDE_PLUGIN_ROOT`.** Those are #155's.

## Data

No storage contract moves.
- A consuming repository's bindings gain one row.
- The old ceiling label stays readable.
- A repository with only `CLAUDE.md` and no row reads exactly as it does
  today, because `CLAUDE.md` is the last name in the order and the only one
  there.
- A repository with both files and no row starts reading `AGENTS.md`. That
  changes which file its gates hold, so the first audit names the file it
  read, and the sitting writes the row that settles it.

## Risks

- **A silent switch** for a repository with both files and no row, as above.
  The audit's line names the file, and the sitting's row ends it.
- **`always-green`.** The gate reads one file either way. A repository passing
  today on `CLAUDE.md` alone passes tomorrow.
- **Eval spend.** Editing `setup` and `doctor` stales their tier rows, and
  the new case starts unmeasured. Named in the pull request, and nothing runs
  without the maintainer's yes.

## Acceptance checks

1. In a scratch repository with `AGENTS.md` only, `doctor.py` names
   `AGENTS.md` in `check:loop-per-claude-md`, and this repository's
   `trace.py` fails an `AGENTS.md` past its ceiling.
2. Here, `verify.py` exits as before, reading `CLAUDE.md` by its row.
3. Bindings with the old **CLAUDE.md ceiling** label still pass.

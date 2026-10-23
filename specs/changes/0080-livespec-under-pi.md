# Spec 0080: livespec under Pi

- **Status:** approved — by the maintainer in advance, 2026-10-23: implemented end to end, reviewed at the merge request
- **Issue:** [#155](https://github.com/sargismarkosyan/livespec/issues/155)
- **Number:** 0080, assigned by the maintainer and held by this branch since
  the issue was claimed on 2026-10-03. The numbers between it and the highest
  on main are held by other trees.
- **Sketch:** skipped — approval was given in advance, so there was no
  decision for a sketch to inform before the build.

## Who this is for

**Ren — [`agent-accelerated-owner`](../personas/agent-accelerated-owner.md) —
running their repositories from more than one harness.** 0079 already names
the situation: the maintainer works under Pi as often as under Claude Code,
in repositories such as `wf-developer-agents/triage-review` that already have
livespec enabled for Claude Code and whose instructions file points at
`/livespec:refine-spec`. They want the same loop from a Pi session in those
repositories, not a second, Pi-only method. Who this is for doesn't move.

**The workflow is [`adopt-the-process`](../workflows/adopt-the-process.feature),**
at three steps:
- the sitting's **enable** step (setup §8), which today writes only
  `.claude/settings.json`;
- its **context file** step (setup §6), which 0079 taught to read
  `AGENTS.md` but which still says nothing when `AGENTS.md` and `CLAUDE.md`
  are both present;
- and the audit that reads the repository months later.

The workflow's own line covers the argument: *the process goes on top of what
is there, never in place of it*. The harness a repository is run from is part
of what is there.

## The job behind the request

The request was *make livespec Pi compliant*. The job behind it: **open a Pi
session in a repository that runs livespec and have the loop work there as it
does under Claude Code.** That means the skills are loaded, the commands they
tell you to type exist, the tools they run are found, and the file they write
and audit is the file the agent actually reads.

**What they do today instead:** the skills load under Pi, since
`skills/` follows the Agent Skills layout Pi implements. Everything after loading
assumes Claude Code:
- the human is told to type `/livespec:setup`, which Pi doesn't have (it's
  `/skill:setup`);
- setup's `--reshape` line and doctor's `--validate` line run
  `$CLAUDE_PLUGIN_ROOT/tools/doctor.py`, which is empty under Pi, so the path
  becomes `/tools/doctor.py`;
- setup enables livespec in `.claude/settings.json`, which Pi never reads, so
  a Pi user has to install the package by hand, and nothing tells them how;
- in a repository with both `AGENTS.md` and `CLAUDE.md`, Pi reads only
  `AGENTS.md`, while the gates and the audit can hold `CLAUDE.md`. They pass
  on a file the agent never reads.

## Why now

- **#154 is fixed**, so all eight skills now load under Pi. That was the
  blocker the issue named.
- **0079 did the reading half of the context file.** The gates and the audit
  resolve `AGENTS.override.md`, `AGENTS.md` and `CLAUDE.md` through the
  bindings' **Context file** row. Its *What we are not doing* handed two
  things to this issue: both files present, and the `/livespec:` and
  `$CLAUDE_PLUGIN_ROOT` couplings.
- **The cost is silent.** Nothing errors under Pi. A command that doesn't
  exist and a variable that's empty both read as the agent's own mistake, and
  a gate passing on an unread file looks the same as a gate passing.

## The end value

From a Pi session in a repository that uses livespec:
- every command a skill tells them to type works;
- every tool a skill runs is found;
- the sitting leaves the repository enabled for Pi as well as Claude Code;
- the audit says so when the file the gates hold isn't the one Pi reads.

Under Claude Code nothing changes.

**How we would know it worked:**
- Running doctor from a Pi session in a repository with wiring left open
  ends on `/skill:setup`. Run from Claude Code, it ends on `/livespec:setup`,
  as before.
- A repository holding `AGENTS.md` beside the `CLAUDE.md` its bindings name
  gets an `open` line saying Pi never reads `CLAUDE.md`.
- No skill builds a path on `$CLAUDE_PLUGIN_ROOT`, and no paragraph names
  `/livespec:<name>` without `/skill:<name>`. `tests/test_hosts.py` holds both.
- The setup sitting, in a repository with a `.pi/settings.json`, adds
  livespec to its `packages` pinned to a release tag, and says the package
  loads only once the folder is trusted.

## What changes

1. **What livespec is: [`specs/spec.md`](../spec.md).**
   - It is still a Claude Code plugin. Pi becomes a second **named host**,
     where the same `skills/` load as a package.
   - The vocabulary gains **host**. *skill* and *component* say "what a host
     loads" instead of "what Claude Code loads".
   - The decision: **named hosts, not host-neutral**. Claude Code remains the
     one the evals measure and the one the marketplace serves. Pi is named
     wherever it differs. A third harness is not promised anything.
   - `CLAUDE.md` and `CONTRIBUTING.md` follow in a line each.

2. **The command to type.**
   - Wherever a skill, the method or the README tells somebody what to type,
     it names both forms: `/livespec:<name>` for Claude Code and
     `/skill:<name>` for Pi. That covers setup's opening, doctor's names
     paragraph and hand-back, `method/README.md` and `README.md`.
   - **[`tools/doctor.py`](../../tools/doctor.py)** reads `/skill:<name>` as
     an instruction, the same way it reads `/livespec:<name>`:
     `check:skill-names` checks it, `check:word-not-a-skill` doesn't treat it
     as prose, and an old name is answered in the form it was written in.
   - The audit's last line, and the no-bindings message, use the form of the
     host running them. Pi sets `PI_CODING_AGENT=true` in every shell it
     starts (Pi's `environment-variables.md`). Where it is unset, the output
     is exactly what it is today.

3. **The plugin root.** Every place a skill runs a tool that ships with
   livespec reaches it at `<plugin root>/tools/…`. The plugin root is two
   directories up from the skill file, a location both hosts tell the
   session. `$CLAUDE_PLUGIN_ROOT` is mentioned only as naming the same place
   where it is set. The three places: setup's `--reshape`, doctor's
   `--validate` and record-clip's stitcher. doctor's §0 and record-clip
   already said this in prose; the commands didn't. `doctor.py`'s usage
   lines follow.

4. **Enabling: setup §8 and [`method/README.md`](../../method/README.md).**
   - §1 reads which hosts run here: the one this session is in, plus any the
     tree shows (`.claude/`, `.pi/`).
   - §8 declares livespec for each host in its own file:
     - **Claude Code:** `.claude/settings.json`, as today;
     - **Pi:** `.pi/settings.json` → `packages`, as
       `git:github.com/sargismarkosyan/livespec@livespec--v<version>`,
       pinned to the release tag of the plugin installed. Pi doesn't move a
       pinned ref on update. Packages already declared there are kept.
   - §8 also says that Pi reads project declarations only once the folder is
     trusted (Pi's `packages.md`). A first session that looks ordinary is
     usually untrusted, not uninstalled.
   - `method/README.md` gains a Pi section: install, the project
     declaration, trust, bare skill names and `/skill:<name>`, Pi keeping the
     first of two skills with one name and warning, updating by moving the
     tag, and a local checkout with `-e`.

5. **The context file.**
   - **[`method/claude-md.md`](../../method/claude-md.md)**, *Which file*:
     a host that reads one file per directory reads the first in its order,
     and never reads the rest. Both files present is two copies. One of them
     is unread by one host, and the gates may hold the unread one.
     *Where it goes*: the `.claude/CLAUDE.md` claim is qualified. Claude Code
     loads it; Pi doesn't.
   - **setup §6**: where both files exist, the sitting says which file each
     host in use reads. It proposes the one every host reads (`AGENTS.md`
     where Pi is in use), harvesting what only the other knew, as
     *When it is out of line* already asks. It waits before removing
     either, and the **Context file** row names the survivor.
   - **doctor**: a new mechanical check, **`check:one-context-file`**
     (severity *wiring*). More than one of the three names at the root reads
     `open`, naming the file Pi reads and the one it never reads, with the
     sitting as what closes it. One file reads `clear`; none reads `n/a`.
     `inject.py` gets the fault that flips it.

6. **Graded cases.** Setup §2 and §4 name `claude plugin eval init` as the
   tool. Under Pi that tool is absent. The existing gated-or-absent fallback
   now says so outright: the sitting writes the case format, and never sends
   somebody to install another host to get a tool. This is wording on an
   existing fallback, and no rule holds it. No case reached the old wording
   either.

7. **This repository.**
   - `tests/test_hosts.py` scans the shipped prose for the two couplings.
   - `tests/test_doctor.py` covers the `/skill:` form, the host's last line
     and `check:one-context-file`. Its existing tests pin the Claude Code
     environment, so they no longer depend on which host runs `verify.py`.
   - The bindings' *What proves a rule* row names `test_hosts.py`.
   - The fault injection record gains the new fault.

8. **The cases.**
   - **85**: setup's enable step in a repository whose owner also runs Pi
     (`the-sitting-enables-livespec-for-each-host-in-use`).
   - **86**: setup's context-file step in a repository with both files
     (`two-instructions-files-become-one`).

**Rules added or changed:**

| Rule id | Feature file | New or changed |
|---|---|---|
| `the-sitting-enables-livespec-for-each-host-in-use` | [`features/setup/the-host.feature`](../features/setup/the-host.feature) | new, claimed by case 85 |
| `two-instructions-files-become-one` | same | new, claimed by case 86 |
| `a-skill-names-both-hosts-where-they-differ` | same | new, claimed by `tests/test_hosts.py` |
| `an-instruction-in-either-hosts-form-is-read` | [`features/wiring/the-host.feature`](../features/wiring/the-host.feature) | new, claimed by `tests/test_doctor.py` |
| `the-sitting-is-named-as-the-host-types-it` | same | new, claimed by `tests/test_doctor.py` |
| `a-second-instructions-file-is-open` | same | new, claimed by `tests/test_doctor.py` |

The existing rules keep their wording. `the-last-line-is-the-command-to-run`
already says *as somebody would type it here*, and
`the-sitting-names-the-context-file` already says *never creates a second
file*. The new rules add the second host to each of them and leave their
cases as they are.

## What we are not doing

- **A Pi arm in the eval runner.** `evals/runner/` drives `claude -p`. A
  second harness there is its own change, and the issue scopes it out.
  Cases 85 and 86 run under Claude Code like every other case, so they show
  the sitting acting on a repository that runs Pi, not the sitting running
  under Pi.
- **Renaming the skills** to avoid Pi's bare-name collisions (`setup`,
  `todo`, `doctor`). Names are what every case and every consuming record
  instructs by. The Pi section of `method/README.md` says which skill Pi
  keeps and that it warns.
- **A `package.json` with a `pi` manifest.** Pi finds `skills/` without one,
  and it would put a second manifest at the root to keep in step with
  `plugin.json`. Listing livespec in Pi's package gallery is a distribution
  decision, not part of this issue's job.
- **A gate that fails on two instructions files.** `gate:context-file-*` are
  a consuming repository's own scripts, wired by its sitting. Changing what
  they demand would move every ledger. The audit reports it, and the sitting
  fixes it.
- **Porting Claude-only features livespec doesn't use** (hooks, subagents,
  MCP), and any harness beyond the two named.
- **Moving GitHub URLs to GitLab.** The marketplace and the Pi package
  source both name `github.com/sargismarkosyan/livespec`, as everything else
  does today.
- **The `Artifact` sketch.** refine-spec already falls back to an HTML file
  (#82).

## Data

No storage contract moves.
- A consuming repository's audit record gains one line,
  `check:one-context-file`. A ledger stamped before it sees it as a check
  newer than the stamp, as with any new id.
- `.pi/settings.json` is written only where Pi is in use, and only by the
  sitting. Its existing `packages` are kept.
- A record written under Claude Code reads the same as before.

## Risks

- **A host misread.** doctor's last line follows `PI_CODING_AGENT`. A Claude
  Code session started from inside a Pi shell would inherit it and print
  `/skill:setup`. That's rare, and the line still names the sitting. The
  tests pin the environment both ways.
- **`always-green`.** Nothing here reaches a user's build. The new check is
  the audit's, and the audit gates nothing.
- **A sitting that deletes a hand-written file.** Two files becoming one
  means one goes away. The rule waits for the owner's yes and harvests
  first, as `claude-md.md` already requires for a rewrite.
- **Eval spend.** Editing setup, doctor and record-clip stales any measured
  tier rows they hold, and cases 85 and 86 start unmeasured. This is named in
  the merge request. Nothing runs without the maintainer's yes.

## Acceptance checks

1. `PI_CODING_AGENT=true python3 tools/doctor.py` in a scratch repository
   with wiring left open ends on `/skill:setup`. Without the variable, it
   ends on `/livespec:setup`.
2. A scratch repository with `AGENTS.md` and `CLAUDE.md` gets
   `check:one-context-file` → `open`, naming both.
3. `rg '\$CLAUDE_PLUGIN_ROOT/' skills method README.md` finds nothing.
4. `pi -p --no-session -ns --skill skills "…list the skill names…"` lists
   all eight.
5. `verify.py` exits 0, or 2 with only the measurement board waiting.

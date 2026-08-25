# Spec 0012: a runner that runs

- **Status:** approved
- **Issue:** [#36](https://github.com/sargismarkosyan/livespec/issues/36)

## Who this is for

[`@persona:agent-accelerated-owner`](../personas/agent-accelerated-owner.md),
and this change sits on the shortest line in that file: *"Adopt a tool that does
not fit the repository just because it is the official one"* is under **What
they will never do**. `claude plugin eval` is the official runner for this
suite, and it does not fit — it exits before case discovery on this account and
has for the suite's entire life. The persona keeps the hand-built local thing
that works over the official thing that does not; this change is that behaviour
applied to livespec itself.

Half of it — the `setup` §4 revision and case 16 — serves
[`@workflow:adopt-the-process`](../workflows/adopt-the-process.feature), because
what `setup` tells a consuming repository about graded suites changes. The other
half — the runner under `evals/runner/` — is livespec's own infrastructure and
serves no workflow, which
[process.md](../../method/process.md#a-technical-change-that-serves-no-workflow-is-correct-not-a-gap)
says out loud is correct rather than a gap.

## The job behind the request

The literal ask: *"Switch from claude plugin eval to other platform eval."*

The job: **the suite has never run.** Sixteen cases, four versions of grader
edits, and not one judge verdict has ever existed — every rubric in `evals/` was
written and rewritten blind. The suite exists to hold a change to a skill's
prose against real behaviour, and it cannot hold anything while the only way to
execute it prints `` `plugin eval` is currently in early access `` and exits.
What stands in meanwhile, `evalsuite.py`, was built as the structural *half* of
a pair and has quietly become everything the word "evals" means here.

The trigger: [`0011`](0011-how-a-test-claims-a-rule.md) shipped `setup` advice
pointing consuming repositories at `claude plugin eval init` — a tool this
repository has never seen start. That was flagged as a risk in that spec; a
version later the maintainer called it.

## Why now

Three things settled today, 2026-08-25:

- **Both arms of the ablation already run without early access.**
  `claude -p --plugin-dir <path>` loads all seven skills in a non-interactive
  session — verified on this machine — and the same command without the flag is
  the without-arm. What is gated is the runner loop and the judge, not the
  ability to run a case.
- **promptfoo 0.122.0 starts here via `npx`**, with node already present. Its
  side-by-side provider comparison is the ablation, `repeat` is `runs:`, and its
  JSON output is what a Δ is computed from.
- The maintainer chose, in as many words: promptfoo; harness proven on one case
  in this change with the full calibration pilot staying their own run; and
  `setup`'s advice becomes try-native-then-fall-back.

## The end value

A judge verdict exists for the first time. Δ — the number
[`evals/README.md`](../../evals/README.md) says is the only one that matters —
stops being a definition and becomes something somebody has seen computed. And
`setup` stops advising a runner nobody here has watched start: the advice
becomes the thing this repository actually did.

**How we would know it worked:** the pull request quotes a real verdict from a
real run — one case, both arms — and the runner invocation documented in the
bindings is one that was executed, not one waiting on enablement.

## What changes

**The runner — `evals/runner/`, livespec-local, never CI.** The case folders
stay authoritative; the platform consumes a compiled view of them.

- `run.py` — the one command. Compiles `evals/<NN-case>/` into a promptfoo
  config, invokes `npx promptfoo@0.122.0 eval`, summarises Δ. Takes the same
  contract flags the old invocation carried — `--ablation with-without`,
  `--judge-model sonnet`, `--allow-tools Write Edit` — so the floor written in
  `evals/README.md` keeps its tokens and `evalsuite.py`'s guard keeps its
  meaning. `--allow-tools` stays an operator grant: a gated tool a case asks for
  but the grant omits is stripped, exactly as the native CLI behaves. Plus
  `--case <name>` and `--runs N` for pilots.
- a provider wrapper — each arm is `claude -p` in a fresh working directory,
  `--plugin-dir` present or absent, the case's `allowed_tools` (intersected
  with the grant) and `max_turns` honoured, the stream transcript kept so
  `tool_used` and files-target graders have something to read.
- a judge — every `llm` grader is scored by `claude -p --model sonnet` with
  `--json-schema` forcing `{pass, reason}`. Runs through the CLI the repo
  already requires; no API key appears anywhere.
- `tool_used` graders keep their 0008 semantics: reported as the plugin-fired
  indicator, weight zero, never in the score of either arm.
- generated config and results are ignored, not committed — `evals/results/`
  already is.

**The floor's guard moves with the invocation.** `evalsuite.py` scans the
documented runner line for the contract flags; the line's prefix changes from
`claude plugin eval` to the `run.py` invocation, and the two `inject.py` faults
that strip `--ablation with-without` and `--allow-tools` from it must fire
unchanged.

**The documentation stops saying "when it unblocks".**
`specs/setup/README.md`'s runner section, `evals/README.md`'s invocation and
calibration, `CLAUDE.md`'s command list, `CONTRIBUTING.md`, and the docstrings
in `verify.py`, `trace.py` and `evalsuite.py` all currently describe the suite
as unrunnable. They describe the new invocation instead; `claude plugin eval`
stays mentioned once as the native runner the format still matches, so that
enablement arriving one day is a bonus rather than a migration.

**What `setup` tells a consuming repository** —
[`setup-scaffolds-the-rule-binding`](../features/setup/test-binding.feature)
gains an example, same id, live: when the tool that builds graded suites is
gated or absent where the suite must run, a platform that can actually run is
what gets set up, and the cases stay in the format the repository's gates read.
`skills/setup/SKILL.md` §4's graded-cases bullet and
`evals/16-setup-with-no-app-code/graders/uses-the-existing-tool.md` carry the
same revision; `method/testing.md`'s *Do not invent a third* gains the one
command-free sentence — a platform that runs beats the native one that does not.

**The smoke proof.** `01-solution-shaped-request`, both arms, one run — it
exercises an `llm` grader, a files-target `regex` grader and the `tool_used`
indicator in one case. Its verdict and Δ go in the pull request. It is a proof
the harness works, **not** a calibration: per `evals/README.md`, nobody trusts
a number from this suite until every verdict of a full pilot has been read.

**Rules added or changed:** no new ids. One live rule,
`setup-scaffolds-the-rule-binding`, edited in place — a third example, same id.
Case 16 already claims it and its revised grader is what holds the new example.

## What we are not doing

- **Not running the full pilot.** 16 cases × 2 arms × 3 runs is ~96 sessions of
  real money, and the calibration pass — reading every verdict — is the
  maintainer's judgment, not this change's. The maintainer chose this split.
- **Not running any of it in CI.** A suite that costs money per run does not go
  behind a merge, and CI installs nothing — both unchanged from before.
- **Not migrating the case format.** The gates are stdlib-only Python;
  `caselib.py` parses the folders; a platform-native YAML format would force a
  YAML parser into the gates, which the no-dependency rule forbids. The folders
  stay authoritative and the platform reads a compiled view.
- **Not using the platform's API-keyed judge.** `llm-rubric` against an
  Anthropic provider wants `ANTHROPIC_API_KEY`; this account works through the
  CLI. The judge goes through `claude -p` instead — the least-platform part of
  the design, named in *Risks*.
- **Not retiring `evalsuite.py`.** The structural gate stays exactly as strong:
  it is what holds the suite on every commit, because the runner costs money
  and CI never pays.

## Data

- **No new permanent ids.** The one rule touched keeps its id.
- **The platform version is pinned in the invocation** — `promptfoo@0.122.0` —
  because `npx` floats otherwise and a floating runner makes every Δ a
  comparison across two runners. Bumping it is a deliberate edit to the
  bindings, like any threshold.
- The old invocation stays quoted once in the bindings as what the format is
  native to. If early access ever arrives, both runners read the same folders.

## Risks

- **The judge is the bridge, not the platform.** Scoring through
  `claude -p --json-schema` is bespoke code in exactly the place the method
  warns about bespoke code. Mitigation: it is one small function with one
  contract (`{pass, reason}`), the rubric bodies stay untouched in `graders/`,
  and swapping it for `llm-rubric` later changes the compiler, not a case.
- **A platform bought is a platform trusted.** promptfoo's repeat, concurrency
  and report are now load-bearing for numbers this repository will one day act
  on, and nobody here has calibrated against it. Mitigation is the smoke proof
  plus the standing rule that no number is trusted before a read-every-verdict
  pilot.
- **The wrapper is still a few hundred lines this repository owns.** Choosing a
  platform shrank the bespoke surface to the two ends — session and judge — and
  that is as small as it gets while the native runner will not start. The
  method sentence this change adds is honest about the trade.
- **`setup` now advises a fallback it has run once, on one case.** Better than
  advising a tool it has never seen start — but the advice is one smoke run
  old, and the first consuming repository to lean on it is the real test.

## Acceptance checks

1. `python3 .github/scripts/verify.py` green, and `inject.py`'s two invocation
   faults fire against the *new* documented line.
2. The smoke run happened: case 01, both arms, one run — the verdict and Δ
   quoted in the pull request, and `evals/results/` still uncommitted.
3. `grep -rn "claude plugin eval" --include="*.md"` — every remaining mention
   describes the native runner or history; none is the documented way to run
   the suite.
4. `skills/setup/SKILL.md`'s `description:` is byte-identical — the body moved,
   the always-on cost did not.
5. Read the new feature example for interface detail: no flag, no platform
   name, no command in the Gherkin.

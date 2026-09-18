# Spec 0056: a fixture is a repository of its own

- **Status:** proposed
- **Issue:** [#127](https://github.com/sargismarkosyan/livespec/issues/127) —
  `verify.py` run by the pre-push hook in a linked worktree commits the
  injector's fixture into the real repository. Found 2026-09-18 while
  building `0055` in a worktree, three pushes running.
- **Depends on:** nothing that ships. It changes how the injector and two
  doctor tests build their git fixtures, and adds the control that proves
  they are isolated.

## Who this is for

**Nobody in the workflows, and that is correct rather than a gap** —
[`process.md`](../../method/process.md#a-technical-change-that-serves-no-workflow-is-correct-not-a-gap).
This is the repository's own pipeline. The person it serves is whoever runs
verification from a linked worktree — the maintainer, or a session keeping
the main tree frozen while an eval run reads its plugin directory, which is
exactly why the worktree existed.

**This lengthens nothing.** It removes a way for the pipeline to damage the
repository it is verifying.

## The job behind the request

The literal ask is #127's: make the fixture's git calls ignore an inherited
`GIT_DIR`. Behind it is a property the tooling assumed and never stated:
**a fixture is a repository of its own, wherever the process that builds it
was started from.** Every git call in `inject.py`'s `git_in()` and in the
two `test_doctor.py` tests passes `cwd=<tempdir>`, which is correct and was
not enough. Git exports `GIT_DIR` into hooks run from a linked worktree; a
child `git` that inherits it ignores its working directory. So the hook's
`verify.py` ran the injector, whose `git init` re-initialised the worktree's
repository — and, deciding it had no work tree, wrote `core.bare = true`
into the shared config — and whose `git add -A` / `git commit -m fixture`
staged the temp directory's files against the worktree's index and committed
them to its branch. Three pushes, three refusals, and a main checkout that
afterwards answered *"this operation must be run in a work tree."*

The primary worktree is immune, which is why hundreds of runs there never
showed it. A direct `verify.py --local` is immune for the same reason. The
hook is simply the usual way that environment turns hostile, and the fix
belongs in the tooling that trusted the environment, not in the hook that
happened to provide it.

## Why now

Because worktrees are the right tool whenever an eval run holds the main
tree — the runner loads the plugin arm from `--plugin-dir` pointed at it —
and the next such run is one approval away.

## The end value

Building a fixture with `GIT_DIR` set to a decoy repository lands nothing in
the decoy: no refs, no commits, no config change. The fixture has its own
`.git`. The two doctor tests use the same helper. The hook also scrubs the
variables before it runs, so anything it grows later starts clean.

**How we would know it worked:** the new control passes on every `verify.py`
run; a push from a linked worktree with the hook enabled is accepted with no
`fixture` commit appearing on the branch; `git rev-parse --is-bare-repository`
in the main tree reads `false` afterwards.

## What changes

1. **[`inject.py`](../../.github/scripts/inject.py)**: `git_in()` runs git
   with an environment from which the variables that relocate a repository
   are removed — `GIT_DIR`, `GIT_WORK_TREE`, `GIT_INDEX_FILE`,
   `GIT_COMMON_DIR`, `GIT_OBJECT_DIRECTORY`,
   `GIT_ALTERNATE_OBJECT_DIRECTORIES`, `GIT_PREFIX`, `GIT_NAMESPACE`. One
   helper, `git_env()`, beside it.
2. **[`tests/test_doctor.py`](../../tests/test_doctor.py)**: the two tests
   that build a git repository call `inject.git_in` instead of their own
   `subprocess.run(["git", …], cwd=root)`; `tests/test_crossing.py` already
   imports the injector, so the path is known.
3. **A control** in `inject.py`, run with the others: with `GIT_DIR` set in
   the process environment to a decoy repository — a fresh `git init` in a
   scratch directory — build a fixture with `as_git_repo_with_a_stray_change`
   and assert the decoy still has no commits and `core.bare` unchanged, and
   the fixture has a commit of its own. If the isolation ever regresses, this
   fails before any hook does. The bindings' *Fault injection* row counts
   four controls.
4. **[`.githooks/pre-push`](../../.githooks/pre-push)** unsets `GIT_DIR`,
   `GIT_WORK_TREE` and `GIT_INDEX_FILE` before it runs, with #127 named
   beside the line. Belt and braces: the tooling no longer needs it, and the
   next script the hook grows will not have to relearn this.
5. **This repository's bindings**: the *Fault injection* row names the fourth
   control; the *Before the push* row says the hook scrubs the variables and
   why.

**Rules added or changed: none.** The repository's own pipeline carries no
rule id; the control is its contract.

## What we are not doing

- **Not scrubbing the environment in `verify.py` itself.** The fixture
  builder is where the assumption lives, and a fixture built from a test, a
  script or a shell should be isolated regardless of what wraps it.
- **Not touching `version_gate.py`, `release.py` or `tools/doctor.py`.** Their
  git calls are *meant* to act on the repository they are run in; inheriting
  its location is correct there.
- **Not forbidding worktrees.** They are the right tool for the situation
  that found this.

## Data

No storage. Files that move: `.github/scripts/inject.py`,
`tests/test_doctor.py`, `.githooks/pre-push`, `specs/setup/README.md`, and
this spec.

**This spec commit stales nothing.** **The implementing change stales
nothing**: no case, rule or skill moves; tests are not a measurement input.
`verify.py` exits **2** for the rows already owed and no other reason.

**What the pull request owes.** Nothing ships, so no label and no release. It
touches `tests/` and `.github/scripts/`, so it carries the run block. The
audit surface does not move; no `.feature` moves.

## Risks

- **A future git call in the fixture bypasses `git_in`.** The control catches
  the builder's own path; a stray raw call elsewhere would not be covered
  until it is routed through the helper. The helper is the only sanctioned
  way to run git in a fixture, and the spec says so where the next author
  reads.
- **Scrubbing hides a variable a test legitimately needs.** None of the
  variables removed relocates anything but the repository; author and
  committer identity, editor and pager are left alone.

## Acceptance checks

1. `python3 .github/scripts/inject.py`: the isolation control passes; the
   fault count is unchanged at 114.
2. From a linked worktree with the hook enabled: `git push` is accepted, and
   `git log --oneline -3` afterwards shows no `fixture` or `x` commit.
3. `git -C <main tree> rev-parse --is-bare-repository` reads `false` after
   that push.
4. `tests.py` green; `verify.py` exits 2 for the board only; the pull request
   carries the run block.

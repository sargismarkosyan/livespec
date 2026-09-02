# Spec 0034: a release that did not happen is still owed

- **Status:** approved
- **Issue:** none — found by [`0033`](0033-a-bill-nobody-approved-does-not-block.md)
  failing, on `main`, in production.
- **Depends on:** nothing. It corrects a defect
  [`0003`](0003-main-releases-itself.md) shipped with and nobody had reason to
  meet until today.

## Who this is for

Everybody with the plugin installed, and
[`agent-accelerated-owner`](../personas/agent-accelerated-owner.md) in
[`adopt-the-process`](../workflows/adopt-the-process.feature) at step 7 —
merging, and expecting that to be releasing.

This one **serves the always-promise rather than a step of a workflow.** The
promise is the sentence [`spec.md`](../spec.md) makes about `version`: *a change
merged without moving it reaches nobody, because `/plugin update` sees the same
string and keeps the cached copy.* Right now that has happened, on `main`, to
three change specs' worth of work.

## The job behind the request

Have merging mean releasing, including on the day something goes wrong between
the two.

## Why now

Because `main` is in that state as this is written.

`0031`, `0032` and `0033` merged as #84. The release job ran on that merge and
**failed** — it still ran the full `verify.py`, which exits 2 on a stale board,
which is exactly what `0033` had just finished arguing should not block. Nothing
was written: no `version`, no entry, no tag.

`0033`'s own follow-up then fixed the release job and merged as #86, and the
release job ran, and **succeeded, and released nothing**:

```
• nothing that ships changed in d189221a — no release
```

That is correct behaviour by the code and the wrong answer. `release.py` decides
what a release contains by diffing **the merge commit against its own parent**:

```python
changed = git("diff", "--name-only", f"{args.sha}^", args.sha).splitlines()
```

#86 touched a workflow, the bindings and a change spec — nothing that ships. So
it released nothing, correctly. And #84's shipping files, sitting on `main`
unreleased, were never in that diff and will never be in any future one, because
every run only ever looks at its own merge.

**The defect is not that a release failed. It is that a failed release is
forgotten.** One run's failure strands whatever it was carrying, permanently and
silently — `main` goes on saying `0.28.0`, every install keeps the cached copy,
and nothing anywhere says work is stuck. The only reason this has never bitten
before is that the release job had never failed.

## The end value

Merging means releasing, and a release that did not happen is still owed rather
than lost. When a release run fails for any reason — a bad token, a runner
outage, a gate that should not have been there — the next merge picks up what it
dropped.

**How we would know it worked:** this change's own merge releases `0.29.0`
carrying `0031`, `0032` and `0033`, none of which it touches. After that, the
check is negative and slower: no version ever again sits on `main` unreleased
while the changelog says nothing is owed.

## What changes

- **`release.py` diffs from the last released tag**, not from the merge commit's
  parent. What ships in a release is everything shipping that has landed since
  the last one — which is what a release *is*, and what the merge-commit diff was
  a same-day approximation of.
- **Where there is no tag to diff from** — a fresh clone, a repository before its
  first release — it falls back to the merge commit's parent, which is today's
  behaviour and the right answer when there is no history to catch up on.
- **The version still comes from the merged pull request's label**, and the entry
  still from its `## Changelog` section, verbatim. Nothing about *what a
  contributor owes a release* moves: one label, one section, and the Gherkin
  block when a `.feature` moved.
- **The `## Changelog` section of the pull request that heals a gap describes
  the whole release**, because it is the entry for every shipping change the
  version carries. This pull request's own section is the worked example.

**Rules added or changed:** none. This is a defect in a script, not a change in
what the method promises — `spec.md` already says merging is releasing, and the
code did not do it.

## What we are not doing

- **Making the release job retry, or re-running the failed one.** A rerun replays
  the workflow file from the commit that triggered it, so #84's rerun would run
  the same full `verify.py` and fail the same way. Healing forward is the only
  direction that works, and it is the one that also covers failures nobody
  predicted.
- **Releasing per merge rather than per tag.** Considered, and it is what the
  bug is: the merge is what *triggers* a release, and the tag is what says where
  the last one got to.
- **Concatenating the stranded pull requests' changelog sections.** Attractive
  and wrong — it would put two headings' worth of prose under one version
  number, sourced from bodies nobody re-read. The entry is the merged pull
  request's, and the person writing it can see what is being caught up.
- **Warning when a release run fails.** Worth having and a separate change: it
  needs somewhere to warn *to*, and this repository's answer for that is the
  pull-request report, which is not on `main`.
- **Touching `version_gate.py`.** It gates a pull request on its own contents,
  which is right; it has no view of what is stranded and should not grow one.

## Data

No storage contract moves and no vocabulary changes. `evals/board.json` gains
nothing and **stales nothing**: no rule text moves, no skill body moves, and no
case's own files change. `release.py` and `releaselib.py` are held by
`inject.py`, which is a gate rather than a case, and it runs on every
`verify.py`.

## Risks

- **A release that carries more than its author looked at.** The entry comes
  from one pull request and the version may now contain several. That is the
  honest description of catching up, and it is visible: `release.py` prints
  every shipping file it counted. The alternative — leaving them out — is the
  defect.
- **The tag is the source of truth for "the last release", and tags can be
  moved or deleted.** A deleted tag makes the next release look larger than it
  is, which is a wrong count rather than a wrong version, and the fallback keeps
  it working rather than failing.
- **`always-green` is untouched.** Nothing here reaches a consuming
  repository's build.
- **`gates-are-proven` is untouched.** `inject.py` still holds `release.py` and
  `releaselib.py`, and this change is inside the part it already breaks.
- **`context-budget` is untouched.** No skill and no description moves.

## Acceptance checks

1. Merge this. The release job writes **0.29.0**, whose shipping files are
   `0031`'s and `0032`'s — none of which this change touches.
2. `CHANGELOG.md` on `main` carries one `0.29.0` entry, verbatim from this pull
   request's `## Changelog` section.
3. `git tag` shows `livespec--v0.29.0`, and the GitHub Release carries the same
   entry.
4. Merge a pull request that changes only `specs/`. It releases nothing, exactly
   as before — the tag is current, so there is nothing stranded to catch up on.
5. `python3 .github/scripts/verify.py --local` — green, `inject.py` included.

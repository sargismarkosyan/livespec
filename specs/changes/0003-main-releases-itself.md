# Spec 0003: main releases itself

- **Status:** proposed
- **Issue:** [#18](https://github.com/sargismarkosyan/livespec/issues/18)

## Who this is for

**Not the persona, and not a workflow either** — said out loud here rather than
filed under the nearest box, which is what
[process.md](../../method/process.md#a-technical-change-that-serves-no-workflow-is-correct-not-a-gap)
asks of a change like this one.

[workflows/](../workflows/README.md) rules it out in as many words: *"Not an
attempt made **on** this repository: releasing a version, editing a skill and
adding the case that holds it. Those are contribution steps and they live in
[CONTRIBUTING.md](../../CONTRIBUTING.md), because the person doing them is the
author rather than the persona."* Releasing is the example that README gives. So
this change gets no `@workflow:` tag when the layer lands, and that is the
correct answer rather than a gap waiting on
[#14](https://github.com/sargismarkosyan/livespec/issues/14).

Who it is for, then, is **the author** — and the person adopting livespec has a
real stake at one remove, which is worth stating precisely rather than claiming
as cover. The plugin has no release channel: `marketplace.json` sources the
plugin at `./`, and neither `claude plugin install` nor `claude plugin update`
accepts a ref. The marketplace tracks the default branch, so **`main` is
production** and a fix reaches somebody exactly when a bumped `version` lands
there. Every hour a shipped change sits on `main` with the number unmoved, every
existing install keeps its cached copy and the fix reaches nobody. That is the
user's stake; it is served here by making the author's step unskippable rather
than by anything they will see.

The always-promise most at risk is **`gates-are-proven`**
([spec.md](../spec.md#the-promises-that-belong-to-no-single-workflow)) — *no gate
ships without a fault that makes it fire.* This change rewrites what a gate
checks, and it inherits a gate that never met that bar: `version_gate.py` is not
run by `verify.py` and so is not touched by `inject.py`'s 24 faults. Replacing
its contents without fixing that would ship a second unproven gate on top of the
first.

## The job behind the request

Have a change that has been merged **be released**, without that depending on
somebody remembering the two files that make it one.

## Why now

Two failures, of the same shape, one of them already realised.

**The number.** Three places tell a human to bump `version` and write the
`CHANGELOG.md` entry by hand — the changelog's own header, `CLAUDE.md`'s loop
step 6, and `CONTRIBUTING.md`'s *Releasing*. `version_gate.py` (0.6.0, from
[#2](https://github.com/sargismarkosyan/livespec/issues/2)) makes forgetting fail
the build, which closed the silent-failure hole but left the typing where it was.
The issue that asked for this was closed naming the reason: bumping on merge
needs a credential that can push to a protected branch, and that cost had not
been weighed. It has now.

**The tag, which is the same failure with no gate on it.** `CONTRIBUTING.md`
step 3 says `claude plugin tag --push`. It has never run:

```
$ git tag -l          # empty
$ gh release list     # empty
```

Eight versions have shipped to every install with no provenance anywhere but a
markdown heading. A step written down, enforced by nothing, and therefore
skipped — sitting one line below the step that *did* get a gate, which is as
clean a demonstration as this repository will ever produce of why the gate was
the right call and why it did not go far enough.

## The end value

A merged pull request **is** a release. The number, the changelog entry, the tag
and the GitHub Release all follow from what the pull request already carried, and
the author's remaining job is to say how big the change is and write the prose
they were writing anyway.

**How we would know it worked:** the next version reaches an install without
anybody editing `.claude-plugin/plugin.json`, and `git tag -l` stops being empty.
Neither has been true of any version so far.

## What changes

- **A release job runs on merge to `main`.** It finds the pull request the merge
  came from, reads its release label and its changelog section, bumps
  `version` in `.claude-plugin/plugin.json`, prepends the entry to
  `CHANGELOG.md`, **runs `verify.py` against the mutated tree**, and only then
  commits and pushes to `main`. Then it tags with `claude plugin tag --push` and
  opens the GitHub Release from the same entry text.
- **The increment comes from a label.** Exactly one of `patch`, `minor` or
  `major` on the pull request. The three labels do not exist yet and are created
  by this change.
- **The entry comes from the pull request body** — the content under a
  `## Changelog` heading, taken verbatim, down to the next `##` or the end.
  `CLAUDE.md` already calls the pull request description this repository's
  deliverable for a version; this stops that prose being written twice and keeps
  the entries as written paragraphs.
- **`version_gate.py` stops checking the output and starts checking the inputs**,
  on the same trigger, over the same `SHIPPING` list, for the same purpose:

  | today | after |
  |---|---|---|
  | a shipping change with `version` unmoved fails | a shipping change carrying no release label, or two, fails |
  | a bump with no `CHANGELOG.md` entry fails | a shipping change whose body has no `## Changelog` section fails |

  A pull request that ships nothing needs neither, exactly as today.
- **The parsing becomes injectable.** Label selection and section extraction move
  into functions that take strings and return strings — no git, no network — so
  `inject.py` can break them and watch the gate fire. This is the
  `gates-are-proven` debt named above, paid in the change that inherits it.
- **The release job refuses to release its own commit.** Its push re-triggers
  `push: main`, because a deploy-key push is a real push unlike a
  `GITHUB_TOKEN` one. The job stops when `HEAD` is already a release commit,
  identified by its committer identity. The `checks` job is deliberately **not**
  skipped, so the release commit is verified on `main` like any other.
- **`main`'s protection migrates from classic branch protection to a repository
  ruleset**, carrying every row across, plus one deploy key as the single
  `bypass_actors` entry. This is settings, not a diff — the bindings' protection
  table is rewritten as the record.
- **Four documents stop describing a process nobody runs**: `CHANGELOG.md`'s
  header, `CLAUDE.md`'s loop step 6, `CONTRIBUTING.md`'s *Releasing*, and the
  *Version gate* and *Release* rows in
  [setup/README.md](../setup/README.md). `spec.md`'s *What a version leaves
  behind* gains the pipeline as the thing that writes all four artefacts.

**Rules added or changed** — the `@rule:` ids in `specs/features/`:

| Rule id | Feature file | New or changed |
|---|---|---|
| `release-bumps-on-merge` | `features/release/pipeline.feature` | new — **owed** |
| `release-takes-its-number-from-the-label` | `features/release/pipeline.feature` | new — **owed** |
| `release-takes-its-entry-from-the-body` | `features/release/pipeline.feature` | new — **owed** |
| `release-refuses-without-its-inputs` | `features/release/pipeline.feature` | new — **owed** |
| `release-does-not-release-itself` | `features/release/pipeline.feature` | new — **owed** |

**The feature file cannot land yet, for the reason
[0002](0002-setup-finishes-what-it-names.md) records.** `trace.py` fails any
feature naming no live `@workflow:`, and this change will name none even once
[workflows/](../workflows/README.md) is filled — see *Who this is for*. So the
Gherkin here is blocked on something narrower than
[#14](https://github.com/sargismarkosyan/livespec/issues/14): it needs the gate
to have an answer for a feature that correctly belongs to no workflow. The five
ids above are **reserved by this spec and permanent from here**; the file that
carries them lands with that decision, and *What we are not doing* says why it is
not taken now.

## What we are not doing

- **Not putting any of this in [`method/`](../../method/README.md).** A release
  pipeline names commands, a branch, a credential and a file layout — it is a
  binding by [CONTRIBUTING.md](../../CONTRIBUTING.md)'s own test, and the method
  stays silent on how a repository releases. Nothing a user installs changes in
  this version.
- **Not deciding how the traceability gate should treat a feature that belongs
  to no workflow.** That is the real blocker on the Gherkin above and it is a
  change to [`gates.md`](../../method/gates.md) — portable, method-level, and
  bigger than this. It gets its own issue and its own version.
- **Not backfilling tags for 0.1.0 through 0.8.0.** Those versions were not
  released that way, and inventing eight tags for commits nobody tagged is
  writing history rather than recording it.
- **Not conventional commits, and not release-please.** Both were on the table in
  [#2](https://github.com/sargismarkosyan/livespec/issues/2). Commit-subject
  changelogs would replace written paragraphs with a bullet list of subjects, and
  release-please is a dependency for a repository that installs nothing to run
  its gates. Rejected on quality and on the standing constraint respectively.
- **Not a release PR, and not a bump pushed onto the pull request branch.** Both
  were considered; both need the same credential this does, and both add a merge
  or a diff line to every version to avoid a step that is already automatic.
- **Not publishing anywhere but `main`.** There is no second distribution
  channel to keep in step, and adding one would create the drift this repository
  exists to prevent.
- **Not touching `SHIPPING`.** What counts as a shipping change is unchanged;
  only what is demanded of one moves.
- **Not a `[skip ci]` guard.** It would skip `checks` on the release commit too,
  leaving the one commit nobody reviewed as the one commit nothing verified.

## Data

None. There is no storage contract — the plugin ships prose, and what a version
leaves behind is listed in
[spec.md](../spec.md#what-a-version-leaves-behind). This change moves who writes
those four artefacts, not what they are.

## Risks

- **A standing write credential to `main` now exists, where today nothing can
  push at all.** `enforce_admins: true` currently refuses the owner's own token;
  after this a deploy key can push. That is a real reduction, taken deliberately,
  and mitigated by making it the narrowest option available: an SSH key scoped to
  this one repository, unable to reach any other repository or any account
  setting, named as the single explicit `bypass_actors` entry rather than as a
  blanket admin exemption. **The bindings record it**, the way they already
  record branch protection, because a credential nobody wrote down is the one
  nobody rotates.
- **A half-finished release leaves `main` bumped and untagged.** Verification
  runs before the push; tagging runs after. A failed tag step is re-runnable and
  the tag operation is idempotent, so the failure mode is a version that is live
  and briefly unlabelled rather than one that is inconsistent.
- **The changelog entry is read at merge.** Editing the pull request body
  afterwards changes nothing; `CHANGELOG.md` is then the only copy and is edited
  like any other file, through a pull request.
- **`gates-are-proven` is the promise this change is measured against.** The new
  input gate ships with faults in `inject.py` or it ships in the same condition
  as the one it replaces, which is the condition this spec objects to.
- **The release job is a workflow with write access on `push: main`.** It is
  defined on `main`, so a fork pull request cannot alter it and cannot reach the
  secret. Worth stating because "any workflow with `contents: write`" is the
  usual objection, and the answer is that only `main`'s own definition ever runs
  with the key.

## Acceptance checks

1. Open a pull request touching `skills/` with no release label. The required
   check fails, naming the missing label. Add two labels; it still fails.
2. Add one label and a `## Changelog` section to the body. The check passes, and
   the diff contains **no** version bump and **no** changelog edit.
3. Merge it. Within a minute `main` carries a release commit bumping
   `.claude-plugin/plugin.json` and prepending the entry, with the body text
   exactly as written in the pull request.
4. `git tag -l` shows `livespec--v<version>`, and the GitHub Release carries the
   same entry.
5. The release commit's own `push: main` run reports the `checks` job green and
   the release job skipped.
6. Open a pull request touching only `specs/`. No label is demanded, and merging
   it releases nothing.
7. `gh api repos/sargismarkosyan/livespec/rulesets` returns the ruleset, and the
   bindings' table matches it row for row.

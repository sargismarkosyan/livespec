# The repository

Conventions for the repository the loop runs in. What the commands are, where the
app lives and which host serves it are **bindings** — every repository writes
those down in its own `specs/setup/README.md`. What follows is the part that does
not change between repositories.

## Layout

The method needs these to exist and to mean these things. Everything else is the
repo's business.

```
specs/
  spec.md                product-level prose: why, vocabulary, storage contract
  personas/*.md          who it is for — one file, one @persona: tag
  journeys/*.md          the arc over time, and the seams — prose, never asserted
  workflows/*.feature    the bounded attempts, each walked by a test
  features/<area>/
    spec.md              area-level prose
    *.feature            Gherkin, the enforced contract
  changes/NNNN-*.md      one numbered change spec per version
  setup/README.md        this repository's bindings — commands, thresholds, paths
  README.md              how the spec layers fit together

tests/
  unit/                  internals; exempt from rule references
  behaviour/             must reference a Gherkin rule
  workflows/             one walkthrough per workflow

docs/screenshots/        the series — one moving picture per version
docs/feedback/           images attached to open issues, deleted when they close
```

Two rules about that tree, and they are the whole reason it is written down:

- **`specs/setup/README.md` is where the method stops and the repository
  starts.** A skill that needs a command reads it there. A skill that hardcodes
  one has broken the plugin for the next repository.
- **`docs/screenshots/` is the deliverable**, not a byproduct. `docs/feedback/`
  is evidence for open questions and is expected to shrink.

## Branches and pull requests

`main` is protected. Work happens on a branch and arrives by pull request:

```sh
git switch -c spec-0004-<slug>
# ... commits ...
git push -u origin spec-0004-<slug>
gh pr create --fill
```

What the protection should enforce:

| Setting | Effect |
|---|---|
| Pull request required | No direct push to `main`, ever |
| Required status check | The verification job — traceability, tests, coverage |
| Strict | The branch must be up to date with `main` before merging |
| Applies to admins | The repository owner has no bypass |
| No force pushes, no deletion | `main`'s history cannot be rewritten or removed |
| Conversation resolution required | Review threads get answered, not merged past |

**The required check is matched by name, and the name is the job's `name:`** —
not the workflow's filename, and not the command it runs. Getting that wrong
produces a check that is required and never runs, which blocks every merge while
looking like a typo nobody made.

**Approvals can honestly be zero** where there is one author: GitHub does not let
anyone approve their own pull request, so requiring one locks the repository
against its only contributor. Zero still forces every change through a pull
request and through the check; it drops only a second pair of human eyes that
does not exist.

Branch protection is the one gate that does not live in the repository, so it
cannot be reviewed in a diff. That is why the table above is written down: it is
the only record of a setting somebody could quietly change.

### Every pull request carries a moving picture

**A pull request that changes what the app looks like shows it, in the body.**
The deliverable is a series of pictures — a description of a screen is not one,
and a reviewer should not have to check the branch out to see what a version did.

**One animated GIF per version**, in `docs/screenshots/`, named for the change
spec that shipped it. A still is not enough: much of what an app does is a thing
*happening*, and a frozen frame is exactly the part that does not carry.

It is recorded **on the branch, before the pull request is opened**, by the
[`record-clip`](../skills/record-clip/SKILL.md) skill, which owns the how —
viewport, frames, stitching, what to put on screen.

Embed it with a **permanent** raw URL pinned to the commit rather than the
branch:

```sh
sha=$(git rev-parse HEAD)
echo "![...](https://raw.githubusercontent.com/<owner>/<repo>/$sha/docs/screenshots/vNNN-<slug>.gif)"
```

A branch URL is the obvious thing and it rots: branches are deleted on merge and
the image goes with them. Relative paths do not work at all — GitHub does not
resolve them in a pull request body. A raw `.gif` animates there, which is the
whole reason this is the format.

A change with nothing to see — tooling, a doc, a refactor — says so in a line
instead. That is the only exemption, and "it is hard to record" is not it.

### And the Gherkin it moved

**A pull request that changes a promise quotes the promise.** When a change adds
or alters a `.feature`, a workflow walk or the walkthrough test behind one, the
body carries the Rule and its Examples — quoted inline, or linked at the commit
SHA rather than at the branch, for the reason the raw URL above exists.

The picture shows what the version does. This shows what it now *claims*, which
is the half a reviewer is actually deciding about and the half that outlives the
release. A diff answers neither: it shows a promise changing without showing what
it changed into, and it is somewhere the reviewer is not.

Conditional, like the picture and for the same reason: a change touching no spec
surface says nothing. Ceremony applied to every pull request is ceremony that
gets skipped on the one that needed it.

**Both halves are gate-checkable and should be gated**, because a convention that
depends on the author remembering it is a convention that decays in the direction
of silence. What a gate can prove is that the block is *there*; whether it is the
right Gherkin is a reading, and the reading is what review is for.

## Commits

One change spec, one commit. Message format:

```
spec 0005: <the spec's title>

<body: what changed and, more usefully, why this shape rather than the
alternatives — the reasoning that will not survive in the diff>

Closes #12
```

- Spec commits use the same prefix and land **before** their implementation.
- Setup and tooling commits have no spec number; describe them plainly.
- **Never commit a state that fails verification.** The required check will catch
  it on the pull request, but finding out locally is cheaper, and every commit is
  a screenshot candidate.

## Issues

GitHub Issues, via `gh`. No issue directory in the repo — two trackers in
parallel is one tracker nobody reads.

| Label | Meaning |
|---|---|
| `from-feedback` | Came out of a human testing session. Everything the `feedback` skill files. |
| `bug` | Behaviour that contradicts a spec, or a crash. |
| `enhancement` | Something new. |
| `ux` | Usability friction, layout, or wording. |
| `accessibility` | A barrier for someone using assistive technology. |
| `question` | Needs an answer before it can be classified. |
| `needs-spec` | Agreed to be built; waiting on a change spec. |

### Closing an issue

Put `Closes #12` in the **pull request description**, not only in a commit
message.

Both mechanisms close the issue when the work reaches `main`. The difference is
what they depend on. A keyword in a commit message relies on that commit's text
surviving the merge, which under squash merging depends on a repository setting
somebody can change later with no sign that it broke issue closing. A keyword in
the description fires on merge whatever the strategy, and GitHub shows the link
before the merge, so you can see it is wired up rather than hope.

**The keyword has to sit immediately before the reference.** `Closes #12` links;
`Closes the structural half of #12` does not — GitHub reads it as a plain
mention, nothing fires, and the line still *reads* like a link, which is how it
goes unnoticed. Check before merging:

```sh
gh pr view <n> --json closingIssuesReferences
```

An empty list means no issue will close, whatever the description says.

### Closing an issue by hand

Two cases, and both need a comment before the close.

**The work shipped, but the resolution is not what was asked for.** Close it
anyway, as completed. An issue tracks a *job*, not a feature list, and the job
can be answered by something other than the thing requested. The comment is what
matters: **what was asked, what shipped, and why they differ.** A dropped part of
the request is recorded there with its reasoning — and if it is still wanted it
gets a fresh issue rather than living on as the stale half of a finished one.
Half-open issues rot, and nobody reads a tracker of them.

This is the case the keyword cannot serve, and the reason to leave the keyword
out on purpose: a pull request answering half of what an issue asked should not
close it silently on merge, before anybody has written down what happened.

**The issue turns out to be mistaken rather than fixed.** Close it with a comment
saying which — a tracker that cannot distinguish "fixed" from "wasn't real" stops
being worth reading.

**Take its screenshot out.** If the body embeds a `docs/feedback/` image, `git rm`
it in the same change that closes the issue. Evidence for a settled question is
just weight.

**Sweep the siblings.** A shipped change often answers more than the issue it was
written for. When one closes, read the others it touched; where it only
half-answers one, say exactly what did not change and invite a reopen.

## Screenshots

`docs/screenshots/` holds one moving picture per version — the actual deliverable.
`docs/feedback/` holds images attached to issues, which are evidence rather than
product.

Images pasted directly into chat cannot be written to disk. For a screenshot to
reach either folder it has to be handed over as a **file path**.

**Feedback images live exactly as long as their issue.** A committed file is the
only thing a GitHub issue can render, so the image goes in while the issue is
open and comes out with `git rm` when it closes. What the screenshot *showed* is
written into the issue body, so the closed issue still says what happened after
the picture is gone. `docs/screenshots/` is the opposite: nothing there is ever
deleted.

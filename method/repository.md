# The repository

Conventions for the repository the loop runs in. The commands, where the app
lives and which host serves it are **bindings**, written in the repository's own
`specs/setup/README.md`. Each section names the principle in
[README.md](README.md#six-principles) it follows from.

## Layout

The method needs these to exist and to mean these things. Everything else is
the repository's business.

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

docs/screenshots/        the series — one picture per version
docs/feedback/           images attached to open issues, deleted when they close
```

- **`specs/setup/README.md` is where the method stops and the repository
  starts** (one copy of anything). A skill that needs a command reads it there;
  a skill that hardcodes one has broken the plugin for the next repository.
- **`docs/screenshots/` is the deliverable**, not a byproduct. `docs/feedback/`
  is evidence for open questions and is expected to shrink.

## Branches and pull requests

*From: every promise is checked by something that can fail.*

`main` is protected. Work happens on a branch and arrives by pull request:

```sh
git switch -c spec-0004-<slug>
# ... commits ...
git push -u origin spec-0004-<slug>
gh pr create --fill
```

What the protection enforces:

| Setting | Effect |
|---|---|
| Pull request required | No direct push to `main`, ever |
| Required status check | The verification job — traceability, tests, coverage |
| Strict | The branch is up to date with `main` before merging — kept by a queue or the platform's own update, never a rebase by hand |
| Applies to admins | The repository owner has no bypass |
| No force pushes, no deletion | `main`'s history cannot be rewritten or removed |
| Merged branches deleted | A pull request stacked on one is retargeted to `main`, not merged into a branch nobody merges again |
| Conversation resolution required | Review threads get answered, not merged past |

- **The required check is matched by the job's `name:`**, not the workflow's
  filename or its command. A wrong name gives a check that is required and never
  runs, and blocks every merge.
- **Approvals can honestly be zero** where there is one author: no platform
  lets someone approve their own pull request. Zero still forces every change
  through a pull request and the check.
- **Several merges keep Strict, and the platform does the updating.** Each merge
  puts every other open pull request out of date. Where the platform has a merge
  queue, merges go through it, and the required checks run on the queue's own
  event or every queued merge waits forever. Where it has none, the platform
  updates each branch from `main` and merges it once green, one at a time and in
  order. Which of the two applies is read back from the platform; a queue nobody
  has watched one merge through is *unobserved*. Dropping Strict to save the
  reruns is refused: two changes green alone can be red together.
- **A stacked pull request lands on `main`.** When its base merges first and the
  base branch stays, the pull request on top merges into a dead branch, reads
  *Merged*, and never reaches a release. So it is retargeted to `main` when its
  base merges — which the platform does itself when it deletes merged branches,
  the reason deletion is in the table. **Merged is not the same as on `main`**:
  what arrived is read from `main`.
- **The protection is read back from whatever enforces it, never inferred from
  the repository.** It is the one gate that does not live in the tree, so it
  cannot be reviewed in a diff, and a required check named in a CI file says
  nothing about whether a merge is blocked. Read the settings, write down what
  came back, and record the command that reads them again — a binding, beside the
  table in `specs/setup/README.md`.

### Several changes at once

**Several changes in flight is the ordinary case**: one change per branch, one
branch per tree — a linked worktree, a second clone. Every rule above holds per
change; this section is about every tree being able to keep them.

- **Every tree lives in one directory, and one command makes, lists and cleans
  them.** Both are bindings. The directory belongs to the repository, not to an
  agent harness: a harness's way of making a tree calls the command, and the
  command never calls a harness.
- **A fresh tree is made ready by that command, never by hand.** A tree readied
  by hand differs from the last in the way nobody sees — a hook on in one tree
  and off in another, and a tree without checks reads like one whose checks
  passed.
- **Every resource a tree touches is one of three kinds, and the bindings say
  which** — decided once, not discovered by the second agent. The agent
  harness's own state kept in a tree is sorted the same way.
  - **The tree's own**: a port, a database on the shared server, a data
    directory, a queue or cache prefix, the names the runtime gives what it
    starts. Worked out per tree by the command, each carrying the tree's name.
  - **Shared, started once**: a database server, a network, a package store. A
    second tree reuses what the first started.
  - **Shared and contended, decided**: one development database, one callback
    address, one account's limit — written down with the reason, so it reads as
    a choice and not as a collision.
- **One env file configures a tree.** The command copies it from one source
  outside every tree's history, changes only the tree's own lines, keeps it
  ignored and never commits it. A value the app reads from anywhere else is a
  setting only the app can move into the file, and that change is filed rather
  than worked around.
- **A tree's own values are worked out from the tree**, not picked at start, so
  the same tree gets the same port every time and the list of trees says what
  runs where.
- **Cleaning goes by the repository's record of its trees, never by deleting a
  directory.** A tree is removed only when it has nothing to lose — nothing
  uncommitted or untracked, every commit on the main branch, not locked, not the
  tree the command runs from — and with what it held of its own: what it started
  is stopped and its own database dropped; what is shared stays up. Every other
  tree is listed with the reason it stayed.
- **All of it is watched, not assumed.** Before the bindings say a fresh tree
  works, a throwaway one is made by the command, verification runs green in it —
  and the app, beside the first tree's — and the command cleans it. Verification
  in the first tree, run while the throwaway exists, counts what it counted
  before, so a tool walking into the directory is caught.

**An issue is taken once.** Work on an issue starts with a **claim** in the
tracker, the one place every tree and machine reads: the marker the bindings
name, and one comment saying where the work is — branch, tree, harness, and the
session's id as the harness gives it, or *not exposed*, never an id made up.

- The claim is read before anything is written about the issue. A claimed issue
  is reported, not taken; asked for *the next issue*, a session chooses among the
  unclaimed and says which it skipped.
- **Nothing releases a claim by age.** A slow session and a dead one look alike,
  so a claim with no branch, no tree and no pull request behind it is shown to
  the person with its age, and taking it over is their call — the new comment
  naming the claim it replaced.
- A claim ends with the pull request that closes the issue, or with the session
  that drops the work, which takes the marker off and says why. A tracker that
  does not answer is said: an unread claim is not an absent one.

**A number nobody else holds.** A change spec is numbered one past the highest
anywhere in flight — the main branch, the change specs in open pull requests,
and the branches the open claims name — because a tree's own checkout sees only
the first. The claim reserves the number. **Gaps stay gaps**: a closed pull
request's number is never reused. If two collide anyway, the one not yet merged
is renumbered — its file, its heading, every link to it. An application's own
numbered files, such as migrations, collide the same way, and Strict and a
pipeline that runs them catch it.

Nothing caps how many trees run at once; the list of trees is where the number
is read.

### Every pull request shows what it did

*From: every promise is checked by something that can fail.*

**A pull request that changes what the app looks like shows it, in the body** —
one picture per version, in `docs/screenshots/`, named for the change spec that
shipped it.

- **The form follows what changed.** A change that unfolds is recorded moving; a
  change whose whole result is a screen sitting there is a still. When the
  convenient answer and the true one come apart, the recording is owed.
- **It is composed for somebody holding the request and nothing else**: can the
  person who asked tell whether they got it, from the request and this one
  picture, without the diff, the branch or the app?
- **It is recorded on the branch, before the pull request is opened**, by
  [`record-clip`](../skills/record-clip/SKILL.md), which owns the how.
- **It is embedded with a raw URL pinned to the commit**, not the branch:

  ```sh
  sha=$(git rev-parse HEAD)
  echo "![...](https://raw.githubusercontent.com/<owner>/<repo>/$sha/docs/screenshots/vNNN-<slug>.gif)"
  ```

  A branch URL rots when the branch is deleted on merge, a relative path does not
  resolve in a pull request body, and a raw `.gif` animates there where a video
  file does not.

A change with nothing to see — tooling, a doc, a refactor — says so in a line.
That is the only exemption; "it is hard to record" is not one.

### And the Gherkin it moved

**A pull request that changes a promise quotes the promise.** When a change adds
or alters a `.feature`, a workflow walk or the test behind one, the body carries
the Rule and its Examples, quoted or linked at the commit SHA. The picture shows
what the version does; this shows what it now *claims*, which is what the
reviewer decides about and what outlives the release. A change touching no spec
surface says nothing.

### And the run it rests on

**A pull request that claims green carries the run**: the verification command
as the bindings name it, and its output as the runner printed it — the last
lines at least, the verdict among them — and, for a change crossing a boundary,
the state read back afterwards. Never a summary: every fabricated result on
record was one. The report prints the pipeline's own run beside the block, so
the two disagree where the reviewer is looking, and gates on nothing there.

Owed only by a change that touches the tests or what runs them. Both blocks —
the Gherkin and the run — are gate-checked for being there and, for the run,
for opening with the bindings' command; whether they are right is a reading,
which is what review is for.

### And the point, before the evidence

**A body backs a decision; it does not replace it.** Two readers are owed it:
the person deciding, who did not ask for the change, and any agent reviewing or
testing that reads it as the author's intent.

**The repository's template wins.** Where there is a pull request template, the
body fills it — every heading and checkbox, in its order, nothing renamed,
replaced or added beside it; folded evidence with no field of its own closes the
testing section. With no template: the point, with no heading; the links line;
the sections the repository's rules require; then decisions, testing and risk,
each only when it has something to say; then the folded evidence.

**A checkbox is a claim**: ticked only when true now. One that waits on an open
question or on an approval the platform does not enforce stays unticked and says
what it waits on; one that does not apply reads `N/A`, with the fact that makes
it so.

**The point states the problem before the change**: who is affected, what goes
wrong, and how it is known — a number, a report, an incident, or the request.
Then one sentence on what changes. Hide that sentence, and the reader should
still know why the change exists. Where the template has a field for why, the
problem goes there.

**What goes in**, one line each:

- **The issue**, closed only when the facts say it is finished; otherwise the
  body relates to it. A part split into its own issue is named in the links line.
- **Every reference is a link with its title** — an issue, pull request,
  incident or spec, never a bare number. A later mention may be the short link
  alone; an item with no address is its id with its title in words.
- **A release note only where the repository publishes one**, written for users:
  every change they will notice, no reasons and nothing internal, or that there
  is nothing. It reads true on its own in the changelog.
- **Before and after**, inline and pinned, when an existing screen changed; the
  after alone when the screen is new.
- **Decisions**: the choice, the alternative rejected, and its cost when known.
  One not settled is an open question.
- **Testing**: what was checked; the tests added, by name, apart from what ran;
  the exact names a tester needs; every gap that bears on this change. A run
  that is owed carries its real price, this change's share apart.
- **Risk and rollout**: flag states, approvals the platform does not enforce,
  steps before or after deploy, and rollback.
- **The evidence, folded**: the picture inline, the Gherkin and the run word for
  word, and how it works where the mechanics matter to the decision.

**Before it is published:**

1. **Ask, don't guess.** A reason, cost, rollout, rollback, address, title or
   picture the author can supply is asked for — never invented, never a
   placeholder. What nobody can answer yet is an open question naming who can.
2. **Check it against the diff.** A claim the diff does not bear out is cut; a
   behaviour change the diff shows and the text misses is added. Reasons,
   numbers and approvals point to a fact. Tests added are kept apart from tests
   run.
3. **Cut.** About a hundred words of the author's own, unfolded; a risky change
   adds a line per decision, open question or rollout step. Template headings,
   its checklist and titles inside links are not counted. Words are cut, never a
   name or fact a reviewer or tester needs.

And throughout:

- **Each fact once**, folded parts included; only the verbatim evidence and a
  release note repeat. Two pull requests that belong together link each other
  instead of carrying the same block.
- **Nothing about what the change does not do.** Under a template heading about
  scope, only decisions go.
- **No standing noise**: what is true on every pull request — a flaky job, a
  known warning, a backlog total, an approval the platform enforces — is left
  out.
- **In the reviewer's words.** A name the session made up is written as what it
  names.
- **The author owns it.** Generated text is a draft: read, cut, explainable line
  by line, with no line about which tool wrote it.

**The message asking for review** is shorter still: the problem, the link, and
what the reviewer is asked to decide.

**No gate can hold this**: whether the opening states the problem is a reading.
A report that already reads the body counts the words before its first heading,
code block or folded block and prints the count, gating on nothing; under a
template whose first line is a heading it reads zero and means nothing.

## Commits

One change spec, one commit:

```
spec 0005: <the spec's title>

<body: what changed and, more usefully, why this shape rather than the
alternatives — the reasoning that will not survive in the diff>

Closes #12
```

- Spec commits use the same prefix and land **before** their implementation.
- Setup and tooling commits have no spec number; describe them plainly.
- **Never commit a state that fails verification.** Every commit is a picture
  candidate, and finding out locally is cheaper than on the pull request.

## Issues

*From: one copy of anything.*

**Wherever the repository's bindings say, through the command they name.** GitHub
through `gh` is an example, not the definition; a self-hosted tracker behind
another CLI is the ordinary case. No issue directory in the repository: two
trackers in parallel is one tracker nobody reads.

### Which repository a skill is acting on

**The one the session is working in.** Filing, listing, reading an issue and
committing evidence all target the repository under the session's working
directory. **The plugin's own checkout is never a target** — it is a clone with a
working remote, so a filing command run there succeeds, and an issue in the wrong
tracker is seen by neither maintainer.

- **A skill about to file says which repository it is filing into, before it
  files** — the one moment the answer is cheap to correct.
- **A report about the plugin itself** goes to the plugin's own tracker, and the
  reply says so. Where it is unclear which the report is about, **ask once; do
  not pick.**
- Inside the plugin's own repository the rule is the same and gives the same
  answer.

| Label | Meaning |
|---|---|
| `from-feedback` | Came out of a human testing session. Everything the `todo` skill files. |
| `bug` | Behaviour that contradicts a spec, or a crash. |
| `enhancement` | Something new. |
| `ux` | Usability friction, layout, or wording. |
| `accessibility` | A barrier for someone using assistive technology. |
| `question` | Needs an answer before it can be classified. |
| `needs-spec` | Agreed to be built; waiting on a change spec. |

### Closing an issue

Put `Closes #12` in the **pull request description**, not only in a commit
message: a commit's keyword depends on its text surviving the merge, which a
squash setting can quietly break, while the description's fires on merge
whatever the strategy, and the platform can list beforehand what it will close.

**The keyword sits straight before a bare reference** — `Closes #12`, or the
keyword followed by the issue's full URL, which also links. Two forms read like a
closing line and close nothing:

- **words between** — `Closes the structural half of #12` is a plain mention;
- **a Markdown link** — the keyword, then `#12` linked to the issue. GitLab
  registers nothing from it; on GitHub it is untested.

A keyword before a real reference can register even inside a code span, so a
description that discusses closing lines writes them without one.

**The step that opens the pull request reads back what it will close**, from the
platform, before handing it back. An empty list closes nothing; a list naming an
issue the change does not finish closes one that should stay open. Either is
fixed in the description and read again. The command is a binding, beside the
tracker in `specs/setup/README.md`.

### Closing an issue by hand

Both cases get a comment before the close.

- **The work shipped, but not what was asked for.** Close it as completed: an
  issue tracks a *job*, and the job can be answered by something other than the
  request. The comment says **what was asked, what shipped, and why they differ**;
  a dropped part that is still wanted gets a fresh issue. This is why a pull
  request answering half an issue leaves the keyword out.
- **The issue was mistaken rather than fixed.** Close it saying which.

Then:

- **Take its screenshot out** — `git rm` its `docs/feedback/` image in the change
  that closes it.
- **Sweep the siblings.** Read the other issues the change touched; where it
  half-answers one, say exactly what did not change and invite a reopen.

## Screenshots

*From: delete what stops being true.*

`docs/screenshots/` holds one picture per version, and nothing there is ever
deleted. `docs/feedback/` holds images attached to issues: committed while the
issue is open — a committed file is the only thing an issue can render — and
removed with `git rm` when it closes. What the screenshot showed is written into
the issue, so the closed issue still says what happened.

An image pasted into chat cannot be written to disk: it reaches either folder
only when handed over as a **file path**.

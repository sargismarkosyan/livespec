# Setup — this repository's bindings

**The method lives in a plugin.** The loop, the rules, the repository
conventions, what the gates have to mean, and how to write a test that earns its
keep are all in
[**livespec**](https://github.com/sargismarkosyan/livespec) — installed here, and
shared with any other repository that runs the same process:

| | |
|---|---|
| The loop, and the rules | [method/process.md](https://github.com/sargismarkosyan/livespec/blob/main/method/process.md) |
| Branches, pull requests, commits, issues, the moving picture | [method/repository.md](https://github.com/sargismarkosyan/livespec/blob/main/method/repository.md) |
| What the two gates mean, and the id system | [method/gates.md](https://github.com/sargismarkosyan/livespec/blob/main/method/gates.md) |
| How to write a test the gates accept | [method/testing.md](https://github.com/sargismarkosyan/livespec/blob/main/method/testing.md) |
| The six skills | [the plugin's own README](https://github.com/sargismarkosyan/livespec#what-you-get) |

**This file is the other half: everything the method leaves to the repository.**
Commands, thresholds, tool names, the CI wiring, the settings that live on GitHub
rather than in a diff. Every skill reads this file before it assumes a command,
so anything a skill needs to *run* belongs here and nowhere else.

The remaining local document is [constraints.md](constraints.md) — no backend,
`localStorage`, no build step, the vendored libraries, the vocabulary. Those are
decisions about *this app*, not about the method.

## Commands

```sh
npm run verify   # trace + test — exactly what CI runs, and what a commit must pass
npm run trace    # traceability only
npm test         # tests + coverage gate
npm run serve    # http://localhost:8000
```

Run `npm run verify` before every commit. CI runs the same thing, so a green
local run means a green build.

## The bindings, in one table

| The method says | Here that is |
|---|---|
| verification, before every commit | `npm run verify` |
| the traceability gate | `tools/trace.mjs`, reading `tools/gherkin.mjs` |
| the coverage gate | `tools/test.mjs` — **95% of lines, branches and functions** across `src/` |
| the test runner and its environment | Node's built-in runner and coverage; `jsdom` for `document` and `localStorage` |
| the test discovery pattern | `tests/**/*.test.mjs` |
| the `rule()` helper | `tests/support/covers.mjs` — also exports `ruleText(id)` |
| soft limits on feature files | 120 lines, 6 rules — warnings, not failures |
| the required status check | the job named **`Verify`** in `.github/workflows/ci.yml` |
| the stored state a bug report should paste | `localStorage.getItem('todo-change.books')` |
| the recording viewport | **900×760**, every version |
| the GIF stitcher | ships with the plugin: `python3 "$CLAUDE_PLUGIN_ROOT/tools/clip.py"` |
| the pull request report | `tools/report.mjs` — not a gate, cannot fail a build |

## Where it lives

- **GitHub:** <https://github.com/sargismarkosyan/todo-change> (public)
- **Live app:** <https://sargismarkosyan.github.io/todo-change/>, deployed from
  green `main` by GitHub Actions
- **Default branch:** `main`, protected. Nothing lands on it except through a
  pull request — direct pushes are rejected for everyone, the author included.

Branch protection is configured exactly as the method's table describes, with
**approvals set to zero** (one author, and GitHub does not let anyone approve
their own pull request). The required check is matched by name and the name is
the job's `name:` — `Verify`, not `verify`.

## Local setup

```sh
git clone https://github.com/sargismarkosyan/todo-change
cd todo-change
npm install         # jsdom, for tests — the app itself needs nothing
npm run serve       # http://localhost:8000
npm run verify      # the same gates CI runs
```

Node 24 or newer (`engines` in `package.json`); CI runs 24. The only dependency
in the whole repo is `jsdom`, and it is a devDependency — see
[constraints.md](constraints.md).

The process arrives with the plugin, declared in `.claude/settings.json`. A fresh
clone gets it on the first session; nothing needs installing by hand.

## Layout

```
index.html               the app — the only page
src/                     app modules and styles

specs/
  spec.md                product-level prose: why, vocabulary, storage contract
  personas/*.md          who the app is for — one file, one @persona: tag
  journeys/*.md          the arc across months, and the seams — never asserted
  workflows/*.feature    the bounded attempts, each walked by a test
  README.md              how the spec layers fit together
  setup/                 this file, and constraints.md
  features/<area>/       area spec.md, plus the .feature files
  changes/NNNN-*.md      one numbered change spec per version

tests/
  unit/                  internals; exempt from rule references
  behaviour/             must reference a Gherkin rule
  workflows/             one walkthrough per workflow
  support/covers.mjs     the rule() helper

tools/
  gherkin.mjs            dependency-free .feature reader
  trace.mjs              the traceability gate
  test.mjs               the test runner and coverage gate
  report.mjs             the pull request report

.github/workflows/ci.yml CI and Pages deploy
docs/screenshots/        the series, one per version
docs/feedback/           screenshots attached to open issues
```

The templates for a change spec, a persona, a journey and a workflow ship with
the plugin, in
[`templates/`](https://github.com/sargismarkosyan/livespec/tree/main/templates).
Their placeholders get filled from this repository: the persona is Theo, the
always-promises are in [`../spec.md`](../spec.md), and the storage contract is
`localStorage` under `todo-change.books`.

## What is already wired

The whole of it, so nothing here gets rebuilt or wondered about:

| Piece | Lives in | Gate? |
|---|---|---|
| Traceability | `tools/trace.mjs` → step *Traceability* | **Yes** — fails the build |
| Coverage | `tools/test.mjs` → step *Tests and coverage gate* | **Yes** — 95% × 3 |
| Machine-readable coverage | `tools/test.mjs` → `coverage/lcov.info` | no — same run, written twice |
| Pull request report | `tools/report.mjs` → summary + one PR comment | no — cannot fail a build |
| Pages deploy | `deploy` job | no — `main` only |
| Branch protection | GitHub settings, not the repo | **Yes** — see above |

`tools/gherkin.mjs` is the reader: no dependencies, small enough to read in one
sitting. It enforces structure as well as parsing — one Feature per file, no
scenario outside a Rule, no duplicate ids, nothing unnamed. A **workflow** file
is parsed with `requireRules: false`, because it is one bounded attempt rather
than a set of them.

The coverage runner prints `coverage gate: INACTIVE` and skips the thresholds
while `src/` has no modules, rather than passing on a measurement of nothing. It
arms itself the moment the first module lands.

**Not enforced, and deliberately:** whether a journey has been looked at since
the workflows under it changed, and whether features have piled up under a
workflow since its file was last edited. Both are git questions rather than file
questions, and CI checks out at `fetch-depth: 1` where `git log -- <path>`
returns nothing — so both would silently pass forever.

## CI/CD

`.github/workflows/ci.yml`, on every push to `main` and every pull request.

**`verify`** — checkout, Node 24 with npm cache, `npm ci`, `npm run trace`,
`npm test`, then the report.

**`deploy`** — only on `main`, only after `verify` passes. Publishes the repo
root to GitHub Pages. Pages is configured with `build_type: workflow`, so the
workflow is the only thing that can deploy. Concurrency is grouped per ref and
does **not** cancel in progress — a half-finished deploy is worse than a slow one.

The site serves the repo root, so `specs/` and `tests/` are published alongside
the app. They are public anyway, and it keeps the deploy step to one line.

### Two Nodes, and only one of them is ours

`node-version: '24'` in `setup-node` is the Node that runs `npm ci` and the
tests. Separately, each `actions/*` step is itself a JavaScript program with its
own runtime declared in its `action.yml`. **Bumping one does nothing for the
other.** When the runner warns that "Node 20 is being deprecated", it is talking
about the second, and the fix is newer action versions — not a change to
`node-version`, which was already right.

Actions are pinned to major versions, all currently on `node24`. When that
warning returns, check what each pinned major declares:

```sh
gh api "/repos/actions/checkout/contents/action.yml?ref=v7" --jq .content | base64 -d | grep -m1 using:
```

The `deploy` job's actions will not warn on a pull request, because the job is
`main`-only and skips. They still need bumping with the rest — the warning simply
waits until something merges.

### Token permissions

The `verify` job names `permissions:` explicitly, which makes the token read-only
apart from the `pull-requests: write` the report comment needs. Naming any
permission drops every unnamed one, so `contents: read` has to be listed too —
without it, checkout fails.

## The report

`tools/report.mjs`, on pull requests only. It writes to the run summary and to a
single pull request comment, rewritten in place on every push so the thread does
not fill with near-identical reports.

It shows spec health — live rules, `@planned` rules, feature and test file counts
— next to the same numbers from the base branch, plus the coverage table and a
list of everything still specced but not built.

The base-branch column comes from a throwaway `git worktree` and a shallow fetch.
`gherkin.mjs` is dependency-free, so reading another commit's specs costs no
install and no second test run — which is also why the comparison covers spec
health and not coverage. If the base cannot be reached, the column degrades to
`–` and the report still posts.

## Both gates are verified to fire, here

Every fault in the method's
[injection table](https://github.com/sargismarkosyan/livespec/blob/main/method/gates.md#both-gates-are-verified-to-fire)
was broken in turn against this repository and the message it produced was read.
The layer-level rows were checked on the finished branch of
[change 0018](../changes/0018-what-it-serves.md), whose acceptance checks record
what each one said. The feature→workflow row was checked a second and better way:
by restoring the claim set the old hand-written `Specs.` lists actually held at
version 0017, where the gate named the nine orphans issue #35 had found, and
nothing else.

If you change either gate, re-check it the same way and update this section.

## Screenshots, and the ones that are stills

`docs/screenshots/` holds one picture per version and is never deleted from.
**The PNGs in it stay.** Versions 8 to 12 shipped before the moving-picture rule
and their stills are the record of those versions; nothing is regenerated to
match a convention that came later. Version 13's still went, because it had not
shipped yet — one version, one picture.

## Changing the setup itself

This file describes decisions. Changing one is a decision about how the project
works, so it goes through the same loop as everything else: a numbered change
spec in [`../changes/`](../changes/) explaining what is changing and why.

The exception is correcting something that is simply wrong — a stale path, a
command that no longer exists. Fix those directly.

**A change to the method rather than to a binding does not belong here at all.**
It belongs in [livespec](https://github.com/sargismarkosyan/livespec), as its own
change in that repository. The test for which is
[in the plugin](https://github.com/sargismarkosyan/livespec#conventions-it-does-assume):
if the sentence could survive a repository with pytest and a Makefile, it is the
method's.

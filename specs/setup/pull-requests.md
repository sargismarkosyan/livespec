# How a pull request description is written here

Every agent and person opening a pull request in this repository follows this
file, whether or not they load livespec. Written from
[`templates/pull-request.md`](../../templates/pull-request.md) for this
repository; the audit reads it against
[`method/repository.md`](../../method/repository.md#and-the-point-before-the-evidence)
after every release. Linked from [`CLAUDE.md`](../../CLAUDE.md)'s step 6.

## The template

*None*: GitHub fills a new pull request from no template here (the bindings'
*Pull request template* row). The body runs, in this order:

1. `**Reviewed:**` — when and how the maintainer approved, quoted.
2. The point, with no heading.
3. The closing line.
4. `**No spec:**` and why, on the lighter path only.
5. `**Decide:**` — a line each, only what the maintainer has to decide.
6. `**Testing:**` — the tests added, by name, apart from what ran.
7. `## Changelog`, then `## Ids`.
8. Folded: the Gherkin, then the run.

## The point

The problem first: who is affected — an adopter, the maintainer, a skill's user
— what goes wrong, and how it is known: the issue, a consuming repository's
session, a measurement. Then one sentence on what changes. Hide that sentence,
and the reader still knows why the change exists.

## The closing line and every reference

- **The closing line:** `Closes https://github.com/sargismarkosyan/livespec/issues/<n>`,
  on its own line, besides the titled link in the point. Read back with
  `gh pr view <n> --json closingIssuesReferences` before handing the pull
  request back.
- **Every other reference is a link with its title:** an issue or pull request
  is linked with `#<n> <title>` as the link's text; a change spec with `spec
  <name> — <title>`, its address pinned at a commit; another project's merge
  request keeps its project path in the text. Never a bare number.

## What else a body carries here

The bindings' *What a contributor owes a release* row is the authority; in
short:

- **When anything ships** (`skills/`, `method/`, `templates/`, `tools/`,
  `.claude-plugin/`): one `patch`, `minor` or `major` label; a `## Changelog`
  section, which the release copies into `CHANGELOG.md` word for word, written
  for adopters; and `## Ids` — the ids added, retired, revised or reworded, or
  `unchanged` and why it asks nothing of an adopter's files. A change to
  `method/repository.md`'s description section or to `templates/pull-request.md`
  revises `check:pr-body-rules`.
- **When a `.feature` moved:** the Gherkin it moved, quoted or pinned.
- **When `tests/`, `evals/` or `.github/scripts/` moved:** the run, a fenced
  block opening with `python3 .github/scripts/verify.py` and its output.
- **No picture:** nothing here runs on a screen. The sketch is drawn before
  approval, not carried here.

## Length

About a hundred words of the author's own, unfolded; one line more per decision,
open question or rollout step. Headings, link titles and the folded blocks are
not counted. Words are cut, never a name or fact the maintainer needs.

## Left out

What the change does not do, an account of the tools that wrote it, and anything
every body here would repeat.

## Before it is published

1. **Ask, don't guess.** What the maintainer can answer is asked; what nobody
   can yet is an open question.
2. **Check it against the final diff:** `git diff origin/main...HEAD`.
3. **Read it back:** `gh pr view <n> --json body`, and count the words.
4. **The gate holds the rest:** `version_gate.py` runs `tools/prbody.py`'s check
   on every body and again on each edit. Here, with no template, it fails a bare
   reference and reports the length.

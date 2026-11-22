# livespec

A Claude Code plugin, and a Pi package: eight skills and the method they run, installed
into other people's repositories so a specification there cannot quietly stop being true.
**This repository is not an application** — it ships prose that an agent reads,
and every skill in it is context that every session of every user pays for.
A version's deliverable is its pull request description; there is nothing to run
and no picture to record.

**The AI writes everything** — skills, method, gates, eval cases, issues, specs.
The human uses the plugin in other repositories, reports what they found, and
approves specs. Read that split into everything below.

**This repository is its own plugin.** The method in [`method/`](method/README.md)
and the skills in [`skills/`](skills/) are not reference material to consult when
stuck — they are the rules this repository is held to, so they are worth reading
rather than working around. They do not need restating here.

**The line:** could this sentence survive a repository with pytest and a Makefile?
If yes it belongs in `method/`. If it names a command, a threshold, a filename or
a language, it belongs in [`specs/setup/README.md`](specs/setup/README.md).
Getting this wrong is how two copies of a method start disagreeing.

## Where to look

| | |
|---|---|
| [specs/setup/README.md](specs/setup/README.md) | **The bindings.** Every command, threshold and path. Read before assuming any of them |
| [specs/spec.md](specs/spec.md) | What livespec is, the vocabulary, and the promises that belong to no workflow |
| [specs/README.md](specs/README.md) | How the spec layers fit, and which are deliberately empty |
| [specs/personas/](specs/personas/README.md) | Who it is for. One, and the reason the gates fail rather than warn: they do not read the docs |
| [specs/workflows/](specs/workflows/README.md) | The bounded attempts. One, live since 0008; three more are real and uninterviewed |
| [specs/features/](specs/features/) | The enforced contract. The live rules, each claimed by an eval case |
| [specs/journeys/](specs/journeys/README.md) | The arc of adopting it, and the seams no attempt can hold. Where the value it has not reached is written down |
| [CONTRIBUTING.md](CONTRIBUTING.md) | What is component and what is payload, where a change goes, the release step |
| [evals/README.md](evals/README.md) | The cases, the floor they may not drop below, and why Δ is the only number |
| [method/gates.md](method/gates.md) | What the gates have to mean |

## The loop

1. The human uses the plugin somewhere else and reports what they found.
2. `todo` files researched GitHub issues. It does not fix.
3. `refine-spec` writes the Gherkin rules and a numbered change spec.
4. The human approves the spec, holding the sketch drawn from it, or asks for changes.
5. Implement the smallest change: drop `@planned`, claim the rule with an eval
   case or a test, delete what it made dead, get `verify.py` green, commit.
6. Open the pull request, carrying what the pipeline cannot work out: one
   `patch`/`minor`/`major` label, a `## Changelog` section in the body that
   becomes the entry verbatim, — if a `.feature` moved — the Gherkin it
   moved, quoted or pinned, and — if the audit surface moved — an `## Ids`
   section: `unchanged`, or the ids added, retired, revised or reworded. Read back what it will
   close, with the bindings' command. **Do not touch `version`, `CHANGELOG.md`
   or a `since` in `requirements.md`** — a new id row reads `next`; the release writes the rest.
7. Both required checks must pass; `main` is protected. Several in flight merge one
   at a time: `gh pr update-branch <n>`, then `gh pr merge <n> --auto --merge`.
   Merging releases: `release.yml` writes the bump, the entry, the tag and the Release.
8. Close the issue with what was asked, what shipped, and why they differ.

## The rules easiest to lose here

The full set is in [method/process.md](method/process.md). These are the ones a
session here is most likely to miss:

- **The `description` is the expensive field.** It loads in every session, so
  widening one is paid for in `evals/` with a should-not-fire case.
- **Spec before code.** No change merges without an approved change spec; a fix
  found on the way is filed, not made.
- **Skills never implement.** `todo` files, `refine-*` specs, `record-clip`
  records. None of them touch application code.
- **The gates take no dependencies.** Python 3 standard library; CI installs nothing.
- **Merging is releasing.** `main` is production: the marketplace takes no ref,
  so `/plugin update` reads `version` off this branch. The pipeline moves it,
  and what a pull request owes is the label, the `## Changelog` section, and the
  Gherkin block when a `.feature` moved. CI fails a pull request that ships or
  re-promises without them.
- **Rule, workflow and persona ids are permanent.** Renaming one orphans every
  case pointing at it, in every consuming repository at once.
- **A payload file nothing links fails CI.** It would ship to every user unread.
- **Measuring is optional, and the maintainer's to choose.** Editing a skill, a
  rule or an eval case stales its rows in `evals/board.json`; `board.py` and the
  pull-request report say which, and nothing waits on them. Every run bills the
  maintainer's account and draws down its session limit, so `run.py` and
  `tiers.py` refuse without `--i-approve-the-cost`, `evalsuite.py` fails if
  either refusal is removed, and the flag is theirs to add, not the session's.
- **Every commit green.** Run `verify.py` before committing.
  `git config core.hooksPath .githooks` makes `.githooks/pre-push` run it before
  a push — off until you type that, bypassable with `--no-verify`, and
  deliberately not in the ledger.

## Commands

```sh
python3 .github/scripts/verify.py                 # everything that can pass here
python3 .github/scripts/trees.py new <name>       # a tree for the next change; list, clean
.github/scripts/validate-manifest.sh .    # marketplace manifest; see specs/setup/
.github/scripts/validate-manifest.sh ./.claude-plugin/plugin.json  # the same
claude plugin validate ./skills --strict
python3 evals/runner/tiers.py --changed --scaffold  # maintainer step: the tiers, a call a row
python3 evals/runner/run.py --ablation with-without --judge-model sonnet --model claude-sonnet-5 --allow-tools Write Edit Bash --scaffold  # the canary
```

The last two refuse unless the maintainer adds `--i-approve-the-cost`, per the
rule above. They **cost money and never run in CI** — they drive `claude -p`
themselves, because the native `claude plugin eval` is gated behind early
access here. The gates hold the eval suite structurally, and a green `verify.py`
does not mean the cases passed.

## Layout

```
skills/<name>/SKILL.md   the only thing Claude Code loads. Eight of them
method/                  the portable rules. Names no command or threshold
templates/               copied into a consuming repository's specs/
tools/                   invoked from a skill body via $CLAUDE_PLUGIN_ROOT. doctor.py is the
                         audit's script; the only code this repository ships
tests/                   the tests for that code — standard library, each naming its rule
evals/<NN-case>/         one prompt, its graders, and the tags saying what it holds
specs/                   this repository's own spec layer
.github/scripts/         the gates. verify.py is the one command; release.py
                         is the pipeline's, and runs on main rather than here
.claude-plugin/          plugin.json is the authority on version; marketplace.json must not restate it
```

## Where it lives

[github.com/sargismarkosyan/livespec](https://github.com/sargismarkosyan/livespec).
Issues are GitHub Issues via `gh`; there is no issue directory, because two
trackers in parallel is one tracker nobody reads.

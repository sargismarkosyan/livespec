# livespec

A Claude Code plugin: eight skills and the method they run, installed into other
people's repositories so a specification there cannot quietly stop being true.
**This repository is not an application** — it ships prose that an agent reads,
and every skill in it is context that every session of every user pays for.
A version's deliverable is its pull request description; there is nothing to run
and no picture to record.

**The AI writes everything** — skills, method, gates, eval cases, issues, specs.
The human uses the plugin in other repositories, reports what they found, and
approves specs. Read that split into everything below.

**This repository is its own plugin.** The method in [`method/`](method/README.md)
and the skills in [`skills/`](skills/) are not reference material to consult when
stuck — they are the rules this repository is held to, and reading them is not
optional. Do not restate them here.

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
2. `feedback` files researched GitHub issues. It does not fix.
3. `refine-spec` writes the Gherkin rules and a numbered change spec.
4. The human approves the spec, or asks for changes.
5. Implement: drop `@planned`, write the eval case that claims the rule, get
   `verify.py` green, commit.
6. Open the pull request, carrying what the pipeline cannot work out: one
   `patch`/`minor`/`major` label, a `## Changelog` section in the body that
   becomes the entry verbatim, and — if a `.feature` moved — the Gherkin it
   moved, quoted or pinned. **Do not touch `version` or `CHANGELOG.md`.**
7. Both required checks must pass; `main` is protected. Merging releases:
   `release.yml` writes the bump, the entry, the tag and the GitHub Release.
8. Close the issue with what was asked, what shipped, and why they differ.

## Rules that get broken here

The full set is in [method/process.md](method/process.md). These are the ones
this repository actually loses:

- **The `description` is the expensive field.** It loads in every session.
  Widening one is paid for in `evals/` with a should-not-fire case, never on a hunch.
- **Skills never implement.** `feedback` files, `refine-*` specs, `record-clip`
  records. None of them touch application code.
- **No dependency may be added to the gates.** Python 3 standard library only —
  CI installs nothing to run them.
- **Merging is releasing.** `main` is production: the marketplace takes no ref,
  so `/plugin update` reads `version` off this branch. The pipeline moves it —
  what you owe is the label, the `## Changelog` section, and the Gherkin block
  when a `.feature` moved. CI fails a pull request that ships or re-promises
  without them. Editing `version` or `CHANGELOG.md`
  by hand now fights the release job rather than helping it.
- **Rule, workflow and persona ids are permanent.** Renaming one orphans every
  case pointing at it, in every consuming repository at once.
- **A payload file nothing links fails CI.** It ships to every user unread.
- **A measurement does not outlive what it measured.** Editing a skill, a rule
  or an eval case stales its entries in `evals/board.json`, and `verify.py`
  fails until `evals/runner/run.py --changed` re-measures exactly those — real
  sessions, real money, run locally before the commit. The score is never
  gated; only its bookkeeping is.
- **The suite never runs unasked.** Every run bills the maintainer's account
  and draws down its session limit — about $1.80 for one case, ~$4 for the
  suite, and three runs in one sitting have exhausted it outright. `run.py`
  refuses without `--i-approve-the-cost`, `evalsuite.py` fails if that refusal
  is removed, and **the flag is the maintainer's signature, not yours**: a
  stale board entry is a reason to stop and ask, never a licence to spend. Say
  which cases are stale and what it will cost, then wait. The commit and the
  pull request can be finished with a gap where the numbers go.
- **Every commit green.** `verify.py` before committing, always. `git config core.hooksPath .githooks` makes `.githooks/pre-push` run the free four fifths of it before a push — off until you type that, bypassable with `--no-verify`, and deliberately not in the ledger.

## Commands

```sh
python3 .github/scripts/verify.py                 # everything that can pass here
claude plugin validate . --strict                 # marketplace manifest
claude plugin validate ./.claude-plugin/plugin.json          # not --strict; see specs/setup/
claude plugin validate ./skills --strict
python3 evals/runner/run.py --ablation with-without --judge-model sonnet --allow-tools Write Edit --scaffold  # maintainer step
```

The last one refuses unless the maintainer adds `--i-approve-the-cost`, per the
rule above. It **costs money per session and never runs in CI** — it drives real
`claude -p` sessions through promptfoo, because the native `claude plugin eval`
is gated behind early access on this account. The gates hold the eval suite
structurally — see the bindings, and do not read a green `verify.py` as saying
the cases passed.

## Layout

```
skills/<name>/SKILL.md   the only thing Claude Code loads. Eight of them
method/                  the portable rules. Names no command or threshold
templates/               copied into a consuming repository's specs/
tools/                   invoked from a skill body via $CLAUDE_PLUGIN_ROOT
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

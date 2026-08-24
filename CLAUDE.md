# livespec

A Claude Code plugin: seven skills and the method they run, installed into other
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
| [specs/personas/](specs/personas/README.md) | Who it is for. Empty — `refine-personas` fills it, and it is the next thing to run |
| [specs/workflows/](specs/workflows/README.md) | The bounded attempts. Empty until the personas exist |
| [specs/journeys/](specs/journeys/README.md) | The arc of adopting it. Empty |
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
6. Bump `version` in `.claude-plugin/plugin.json` and add the `CHANGELOG.md`
   entry in the same commit.
7. Open the pull request. Both required checks must pass; `main` is protected.
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
- **Push without bumping `version` and nobody gets the change.** The bump and the
  changelog entry ride in the same commit as the change. CI fails a pull request
  that changes what ships without moving it — you cannot forget, but you do still
  have to do it.
- **Rule, workflow and persona ids are permanent.** Renaming one orphans every
  case pointing at it, in every consuming repository at once.
- **A payload file nothing links fails CI.** It ships to every user unread.
- **Every commit green.** `verify.py` before committing, always.

## Commands

```sh
python3 .github/scripts/verify.py                 # everything that can pass here
claude plugin validate . --strict                 # marketplace manifest
claude plugin validate ./.claude-plugin/plugin.json          # not --strict; see specs/setup/
claude plugin validate ./skills --strict
claude plugin eval . --ablation with-without --judge-model sonnet --allow-tools Write Edit   # maintainer step
```

The last one **does not run**: `claude plugin eval` is gated behind early access
on this account. The gates hold the eval suite structurally instead — see the
bindings, and do not read a green `verify.py` as saying the cases passed.

## Layout

```
skills/<name>/SKILL.md   the only thing Claude Code loads. Seven of them
method/                  the portable rules. Names no command or threshold
templates/               copied into a consuming repository's specs/
tools/                   invoked from a skill body via $CLAUDE_PLUGIN_ROOT
evals/<NN-case>/         one prompt, its graders, and the tags saying what it holds
specs/                   this repository's own spec layer
.github/scripts/         the gates. verify.py is the one command
.claude-plugin/          plugin.json is the authority on version; marketplace.json must not restate it
```

## Where it lives

[github.com/sargismarkosyan/livespec](https://github.com/sargismarkosyan/livespec).
Issues are GitHub Issues via `gh`; there is no issue directory, because two
trackers in parallel is one tracker nobody reads.

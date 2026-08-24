# Contributing

livespec is a plugin whose whole claim is that a specification can be stopped
from quietly going out of date. A contribution that makes this repository drift
from itself is the one thing that cannot be accepted here.

Read [`method/process.md`](method/process.md) first. This file is about the
repository; that one is about the method.

## What this repository is, structurally

It is a **marketplace and a plugin at the same root** — `marketplace.json` lists
one plugin whose `source` is `./`, so the plugin *is* the whole repo. Everything
at the root is copied into every user's `~/.claude/plugins/cache`.

Claude Code loads a fixed, short list of directories. Here, exactly one of them
exists:

| | | |
|---|---|---|
| `skills/` | **component** | The only thing Claude Code loads. Seven skills. |
| `method/` | payload | Inert. Reachable only because a `SKILL.md` links it. |
| `templates/` | payload | Same. |
| `tools/` | payload | Reached via `$CLAUDE_PLUGIN_ROOT/tools/…` from a skill body. |
| `evals/` | neither | Test suite. Ships, never loads. |
| `.github/` | neither | Repository maintenance. Ships, never loads. |

The distinction matters because it is the context budget:

- **Every session pays** for each skill's `name` and `description`, whether or
  not anything fires — currently ~3.2 KB across the six model-invocable skills.
  A skill marked `disable-model-invocation: true` costs nothing until invoked;
  its description is not in context at all.
- A skill's **body** loads only when that skill fires.
- **Payload** loads only when a body sends the agent to it — which is why a
  `method/` or `templates/` file that nothing links is dead weight in every
  install, and why CI fails on one.

## Where does my change go?

Three destinations, and picking wrong is the most common mistake:

| The change… | goes in |
|---|---|
| is portable and agent-facing — judgment, an interview, a refusal | **this repo**, in `skills/` or `method/` |
| names a command, threshold, filename, language or tool | **the consuming repository**, in `specs/setup/README.md` |
| has to run without an agent — a gate, a build step | **the consuming repository's CI** |

A plugin is available to an agent, not to a build runner. Nothing here can fail
your build, and the method is deliberately written so it never needs to.

**The test for anything in `method/`:** could this sentence survive a repository
with pytest and a Makefile? If not, it is a binding, not the method.

## Changing a skill

- **The `description` is the expensive field.** It is the only text loaded in
  every session and the only thing the model sees when deciding to fire. Widening
  one to catch a missed trigger costs every session and risks over-firing — pay
  for it in `evals/`, with a should-not-fire case, not on a hunch.
- **Every `refine-*` skill has a "the one thing this skill refuses" section.**
  That refusal is the skill's actual value. If you edit one, `evals/` has a case
  holding it; if you add one, add the case.
- **A skill with side effects the human should time is user-invoked only.**
  `setup` carries `disable-model-invocation: true`, which takes its description
  out of context entirely — Claude cannot see it to consider it, and it runs only
  when someone types `/livespec:setup`. It writes `CLAUDE.md` and wires a
  repository's gates; that is not a decision an agent makes because a repo looked
  ready for it. `USER_INVOKED_ONLY` in `.github/scripts/checks.py` holds the list,
  and CI fails if the flag goes missing.
- **Skills never implement.** `feedback` files, `refine-*` specs, `record-clip`
  records. None of them touch `src/`. A change that relaxes this is a change to
  what livespec is, and needs to be argued as one.
- **Relative links from a `SKILL.md` resolve inside the plugin** (`../../method/…`).
  Links inside `templates/` resolve in the *consuming* repository, because those
  files are written to be copied into its `specs/`. CI knows the difference; keep
  it that way.

### Adding a skill

Costs every session, forever. Bring:

1. a `description` that says when to fire and — as the existing ones do — when
   not to;
2. at least one case tagged `skill:<name>`, and confirmation that the three
   should-not-fire cases in `evals/` still pass. **This one is a gate, not
   advice** — `evalsuite.py` fails on a skill no case holds;
3. a row in `README.md`'s table (CI checks the count against `skills/`).

### Adding to `method/` or `templates/`

Link it from the skill that needs it, in the same change. A file nothing points
at fails CI, because it ships to every user unread.

## Before you open a pull request

```bash
python3 .github/scripts/verify.py     # the one command: both gates, and proof they fire
claude plugin validate . --strict     # marketplace manifest
claude plugin validate ./.claude-plugin/plugin.json          # not --strict; see specs/setup/
claude plugin validate ./skills --strict
```

CI runs all four, and `verify.py` is what the required check runs. It needs
nothing but Python 3 — no dependency may be added to the gates, because CI
installs nothing to run them. `plugin validate` is an offline schema check and
needs no credentials.

`verify.py` runs four things: [`checks.py`](.github/scripts/checks.py) (what only
this repository knows about itself), [`trace.py`](.github/scripts/trace.py)
(traceability, both directions), [`evalsuite.py`](.github/scripts/evalsuite.py)
(every skill held by a case, every case able to fail), and
[`inject.py`](.github/scripts/inject.py), which breaks both gates 24 ways in a
temporary fixture and checks each one fires. What each binding means is in
[`specs/setup/README.md`](specs/setup/README.md).

If you changed a skill's judgment or its description, also run the evals — see
[`evals/README.md`](evals/README.md). They cost money and `claude plugin eval` is
in early access, so this is a maintainer step rather than a CI gate.

### Developing against a local checkout

Point a marketplace at this directory and a skill edit is live next session, with
no publish step:

```
/plugin marketplace add ~/Projects/livespec
```

Editing `.claude/skills/` in whatever repo you are testing in is how two copies
of a method start disagreeing — the thing this plugin exists to stop.

## Releasing

The `version` in `plugin.json` pins every install. Push without bumping it and
**nobody gets the change**.

1. Bump `version` in `.claude-plugin/plugin.json`. Never set `version` in the
   marketplace entry too — `plugin.json` silently wins, so the second one can
   only go stale. CI fails on it.
2. Add a `CHANGELOG.md` entry in the same commit.
3. `claude plugin tag --push` — creates `livespec--v<version>`, and refuses on a
   dirty tree or when the manifests disagree.

Semver, loosely: patch for wording that does not change what a skill does, minor
for a changed judgment or a new skill, major for a change to the method that
would read badly against old commits. Nothing records which version of the
method built a given commit, so when a change to the method *would* read badly
against them, say so in the change that makes it.

## What gets turned down

- A skill that implements rather than specifies.
- A binding — a command, threshold or tool name — written into `method/`.
- A `description` widened without an eval case paying for it.
- A payload file nothing links, or a link that resolves nowhere.
- A grader softened until it always passes. If a case fails, the question is what
  version of that grader would still catch a real regression.

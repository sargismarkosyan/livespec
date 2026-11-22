# livespec

**Spec-driven development that leaves the code as the source of truth.**

Most spec-driven tooling points the arrow the wrong way: write a spec, generate
the code, and from then on maintain a document that nobody reads and nothing
checks. Six weeks later the spec describes a product that no longer exists, and
you are worse off than if you had written nothing — because now there are two
answers and one of them is lying.

livespec points it the other way. **The code is the truth. The spec carries the
context the code cannot** — who this is for, what they were trying to do, what
was considered and dropped, and why this shape rather than the obvious one. Then
it makes the connection between them a thing that can *fail a build*, so the spec
cannot quietly stop being true.

```
/plugin marketplace add sargismarkosyan/livespec
/plugin install livespec@livespec
```

That is Claude Code. Under [Pi](https://pi.dev) it is a package instead:

```
pi install git:github.com/sargismarkosyan/livespec
```

Wiring it into a repository rather than a machine, updating it, and developing
against a local checkout are in [*Installing*](#installing) below, for either
host.

## What you get

Five skills, and the discipline they enforce.

| Skill | What it does |
|---|---|
| `todo` | Turns a testing session into researched GitHub issues — reproduces the bug, names the file and line, and files it. Fixes nothing. |
| `refine-spec` | Turns a request into a spec. Finds the *job* under the proposed solution, checks it against who the product is for, writes the Gherkin rules and the numbered change spec. Implements nothing. |
| `refine` | Keeps the layers above the features true by interview: who it is for, the bounded attempts it is built out of, and the arc over time with its seams — and refuses a persona, a workflow or a journey invented to make a wanted feature legal. |
| `record-clip` | Records the animated GIF a version ships with: the app being *used*, in a real browser. |
| `setup` | **Start here** — `/livespec:setup` in Claude Code, `/skill:setup` in Pi. Sets the process up in a repository: reads what is already there, wires both gates in that project's own language, proves each one fires, writes its bindings file and CLAUDE.md, then runs the persona, workflow and journey interviews. Later it **reports** — re-audits every claim the bindings make against what owns the answer, branch protection read back from the platform, correcting only the record — and **brings the repository up to date** after a plugin update, planning what the new version asks and wiring it one approved item at a time. Whichever way it starts, it says what it will write and waits before writing any of it. |

Plus [the method](method/) — the loop, the repository conventions, what the gates
have to mean, how to write a test that earns its keep, and what a repository's
CLAUDE.md must contain — and [templates](templates/) for a change spec, a
persona, a journey, a workflow and a feature.

## The shape of it

```
feedback in chat  →  researched issue  →  spec, approved  →  one small change
      ↑                                                            ↓
   the human uses the version  ←  merged  ←  pull request with a GIF in it
```

One change spec = one step = one version = one commit = one picture. Unrelated
changes never travel together, and nothing is implemented before its spec is
approved.

## What makes the spec stay true

**Traceability, enforced in both directions.** Every Gherkin rule carries a
permanent id; every behaviour test names the rule it exists for. A rule nothing
verifies fails the build. A behaviour test naming no rule fails the build. The
same loop closes one layer up: every feature says which workflow it serves, every
workflow names a persona and is walked by a test, every persona is named by a
workflow or explicitly retired.

**Coverage, alongside it.** Coverage alone rewards tests that touch code without
asserting anything anyone asked for. Traceability alone rewards tests that name a
rule and check it shallowly. Together they are hard to satisfy dishonestly, which
is the only property either one is for.

And **the gates are tested against deliberate violations** rather than assumed to
work — [gates.md](method/gates.md) lists the faults to inject and what each
should do. A gate that has never failed is not known to be a gate.

## What this plugin does not do

- **It does not ship the gate.** Your CI runs your commands; a plugin is
  available to your agent, not to a build runner. livespec says what
  verification has to *mean* — the commands, thresholds and tooling live in your
  repository, in `specs/setup/README.md`, which is the one file every skill reads
  before it assumes anything.
- **It does not generate code from specs.** That is the arrow this exists to
  reverse.
- **It does not fix things it finds.** `todo` files. `refine-spec` specs.
  Neither touches `src/`, ever. Feedback fixed on the spot is the fastest way to
  lose the record of why something changed.

## Conventions it does assume

Gherkin with stable rule ids and a `@planned` tag for what is specced but not
built, a prose layer above it (`specs/personas/`, `specs/workflows/`,
`specs/journeys/`), numbered change specs in `specs/changes/`, and
`specs/setup/README.md` for everything that is yours rather than the method's.
That is the method, not infrastructure — nothing here cares what language you
write in, what runs your tests, or what your coverage number is.

## Where it came from

Twenty-eight versions of one small app, built entirely by AI, one spec at a time,
with a human using it and reporting what they found:
**[todo-change](https://github.com/sargismarkosyan/todo-change)** — the reference
implementation, and the series of pictures it produced.

## Installing

### Adding the marketplace and the plugin

livespec has two named hosts. **Claude Code** loads it as a plugin, from the
marketplace below. **Pi** loads the same skills as a package — see
[*Under Pi*](#under-pi). The skills and the method are the same in both; what
differs is how it is installed, how a skill is typed, and which settings file
enables it for a repository.

In Claude Code, the two commands at the top of this page: the first registers
this repository as a marketplace, the second installs the plugin from it. `/plugin` on its own opens the browser if you would rather click.
**A skill's body is loaded once, when a session starts** — after `/plugin
update`, start a new session, or the session goes on running the skill it
loaded before the update.

**To check it took**, start a session and look at the skill names: they arrive
prefixed, as `livespec:refine-spec`, `livespec:todo`, `livespec:setup` and so
on. Any of them can be typed directly — `/livespec:setup` is the usual way to
start the install, and under Pi it is `/skill:setup` — and Claude can also reach `setup` itself, in which case it
says what it would write and waits rather than starting. A bare `refine-spec`
with no prefix means a local copy in `.claude/skills/` is shadowing the plugin.

#### Wire it into the repository instead of the machine

Better than installing by hand: commit the declaration, so anybody who clones the
repository gets the process on their first session. In `.claude/settings.json`:

```json
{
  "extraKnownMarketplaces": {
    "livespec": {
      "source": { "source": "github", "repo": "sargismarkosyan/livespec" }
    }
  },
  "enabledPlugins": { "livespec@livespec": true }
}
```

That is what [`setup`](skills/setup/SKILL.md) writes on its way out, and it is
the only livespec-shaped file the method asks a repository to carry. It takes
effect once a person trusts the folder — until then the file is inert and they
have no skills, which is worth saying to whoever reports that their first session
looked ordinary.

#### Updating

```
/plugin marketplace update livespec
```

The plugin is pinned to what the marketplace last resolved, so a change here
reaches a repository when it updates, not before. **Nothing records which version
of the method built a given commit** — where a change to the method would read
badly against old commits, say so in the change that makes it.

What a repository does record is one level up and one thing only: the
[gate wiring ledger](method/gates.md#what-is-wired-and-what-is-not) in its bindings
carries the version its wiring was last reconciled against, so `setup` can offer
the difference on a later run and its report can read, from the changelog that
ships with the plugin, what moved between. That is the installed process, not a
commit's history.

#### Working on the method itself

Point the marketplace at a local checkout rather than at GitHub, and a skill edit
is live in the next session with no publish step:

```
/plugin marketplace add ~/Projects/livespec
```

**That name is machine-wide, and there is one of it.** A marketplace is named by
its own `marketplace.json` rather than by the directory you point at, so the
checkout registers as `livespec` — the name the published one already has — and
registering the second replaces the first. Every repository on the machine that
enables `livespec@livespec` moves with it: they are all running your working tree
now, including the ones you are not editing. `/plugin marketplace list` says
which copy is current (`Directory` or `GitHub`); the skill names do not, because
they are `livespec:refine-spec` either way.
`/plugin marketplace add sargismarkosyan/livespec` puts every repository back to
the published copy.

**Keep that command out of a committed `.claude/settings.json`.** A project file
that declares a directory marketplace repoints the name on the machine of
everyone who clones the repository, for all of their repositories, without their
asking — so a local checkout is registered per machine, by hand, while the
committed file only enables the plugin.

Iterate there, and push when something settles. The alternative — editing the
skills in `.claude/skills/` of whatever repo you are in — is how two copies of a
method start disagreeing, which is the thing this plugin exists to stop.

### Under Pi

Pi does not load Claude Code plugins, but it implements the Agent Skills
layout `skills/` is written in, and installs a git repository as a package:

```
pi install git:github.com/sargismarkosyan/livespec
```

**The skills arrive bare** — `setup`, `todo`, `refine-spec` — and are typed
`/skill:setup`, `/skill:refine-spec`, where Claude Code takes
`/livespec:setup`. Where two packages ship a skill of the same name, Pi keeps
the first it found and warns at startup; the warning names which one won.

**To wire it into the repository**, declare the package in `.pi/settings.json`:

```json
{ "packages": ["git:github.com/sargismarkosyan/livespec"] }
```

`pi install git:github.com/sargismarkosyan/livespec -l` writes the same line. That is what [`setup`](skills/setup/SKILL.md) writes
beside `.claude/settings.json` when the repository is run from Pi too.
**Pi reads it only once the folder is trusted** — until then the declaration
is inert, as Claude Code's is before the folder is trusted there.

**Updating** is `pi update`: with no ref, Pi checks the package and says when
a release is out, as for any package. A team that wants everyone on one version
pins a release tag, `…@livespec--v<version>`; Pi never checks a pinned ref, so
updating is then moving the tag by hand. A
skill reaches the tools it ships from its own place — two directories up from
the skill file — so nothing depends on a variable only Claude Code sets.

**Working on the method itself**, `pi -e ~/Projects/livespec` loads a local
checkout for one session, without touching any settings file.

**The instructions file Pi reads** is the first of `AGENTS.override.md`,
`AGENTS.md` and `CLAUDE.md` in a directory, and only that one — see
[claude-md.md](method/claude-md.md#which-file).

## Working on it

[CONTRIBUTING.md](CONTRIBUTING.md) — what is a component and what is payload,
where a change belongs, and the two things a pull request owes the release.
[evals/](evals/README.md) — the cases that hold the judgment the skills
exist for, measured as uplift over running without them.
[CHANGELOG.md](CHANGELOG.md) — written on merge rather than by hand, because
`main` is what every install updates from.

livespec runs its own process: [specs/](specs/README.md) is this repository's
spec layer, [specs/setup/README.md](specs/setup/README.md) its bindings, and
`python3 .github/scripts/verify.py` the one command that means everything
passes — including breaking every gate on purpose, 40 ways, to prove they still
fire.

MIT licensed.

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

Wiring it into a repository rather than a machine, updating it, and developing
against a local checkout are all in [method/README.md](method/README.md).

## What you get

Seven skills, and the discipline they enforce.

| Skill | What it does |
|---|---|
| `feedback` | Turns a testing session into researched GitHub issues — reproduces the bug, names the file and line, and files it. Fixes nothing. |
| `refine-spec` | Turns a request into a spec. Finds the *job* under the proposed solution, checks it against who the product is for, writes the Gherkin rules and the numbered change spec. Implements nothing. |
| `refine-workflows` | Re-cuts the bounded attempts the product is built out of, when the list stops matching what anybody actually tries. |
| `refine-personas` | Adds, amends or retires who it is for — and refuses a persona invented to make a wanted feature legal. |
| `refine-journeys` | Keeps the arc over time honest, and holds the seams that belong to no single workflow. |
| `record-clip` | Records the animated GIF a version ships with: the app being *used*, in a real browser. |
| `setup` | **You run this one** — `/livespec:setup`. Installs all of the above into a repository: reads what is already there, wires both gates in that project's own language, proves each one fires, and writes its bindings file and CLAUDE.md. It is the only skill Claude cannot start on its own. |

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
- **It does not fix things it finds.** `feedback` files. `refine-spec` specs.
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

## Working on it

[CONTRIBUTING.md](CONTRIBUTING.md) — what is a component and what is payload,
where a change belongs, and the release step. [evals/](evals/README.md) — the
seven cases that hold the judgment the skills exist for, measured as uplift over
running without them. [CHANGELOG.md](CHANGELOG.md) — and why the version bump is
not optional.

MIT licensed.

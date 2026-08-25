# The spec layer

This repository runs the process it ships. The layers below are the same ones
livespec asks of any repository — with one substitution that runs through all of
them: **the tests here are eval cases**, because the product is judgment and the
only way to hold judgment is to run it against a prompt and grade what came back.

| Layer | What it holds | Who fills it |
|---|---|---|
| [spec.md](spec.md) | What livespec is, the vocabulary, what a version leaves behind, and the promises that belong to no single workflow | this file's author, by hand |
| [personas/](personas/README.md) | Who the plugin is for | [`refine-personas`](../skills/refine-personas/SKILL.md) |
| [journeys/](journeys/README.md) | The arc of adopting it, and the seams | [`refine-journeys`](../skills/refine-journeys/SKILL.md) |
| [workflows/](workflows/README.md) | The bounded attempts somebody makes with it | [`refine-workflows`](../skills/refine-workflows/SKILL.md) |
| `features/` | Gherkin — the enforced contract. Does not exist yet | [`refine-spec`](../skills/refine-spec/SKILL.md) |
| [changes/](changes/) | One numbered change spec per version | [`refine-spec`](../skills/refine-spec/SKILL.md) |
| [setup/README.md](setup/README.md) | The bindings — every command, threshold and path that is this repository's rather than the method's | already written |

**`features/` is missing on purpose.** A directory is created when something
goes in it. A tree of empty folders reads as a process that was installed and
never run, and the gate cannot tell an empty layer from a broken one.

## Where the method stops and this repository starts

Everything portable lives in [`method/`](../method/README.md) and
[`skills/`](../skills/) — this repository *is* the plugin, so those are one
directory away rather than one install away. Everything that names a command, a
threshold, a filename or a language lives in [setup/README.md](setup/README.md).

The test: could this sentence survive a repository with pytest and a Makefile? If
yes it belongs in `method/`; if no it belongs in `setup/`. Getting it wrong is
the mistake that makes two copies of a method disagree, which is the thing this
plugin exists to stop.

## The spec layer starts today

Nothing here describes behaviour that already exists. The seven skills, the
method documents and the nine eval cases predate this layer and were not
retroactively specced — [`setup`](../skills/setup/SKILL.md) section 7 says why,
and [setup/README.md](setup/README.md) records which cases are exempt from
claiming a rule as a result. Numbering starts at
[`0001`](changes/0001-the-gate-wiring-ledger.md), and every spec in
[changes/](changes/) describes a change still to come rather than one already
made.

# The bounded attempts

**Empty.** [`refine-workflows`](../../skills/refine-workflows/SKILL.md) fills it,
after the personas exist — a workflow names the persona it is for, and the gate
fails a workflow that names nobody.

One file per workflow, `.feature`, `@workflow:<id> @persona:<id> @journey:<id>`
on the first line, no `Rule:` anywhere in it, and the shape is in
[the template](../../templates/workflow.feature).

## What walks a workflow here

In a repository that ships code, `tests/workflows/` holds one walkthrough per
workflow. Here that is an **eval case tagged `workflow:<id>`** — a prompt that
makes the whole attempt, graded on what came out. The traceability gate fails a
workflow that no case walks; [setup/README.md](../setup/README.md) has the tag
contract.

## The distinction this layer keeps getting wrong

An attempt somebody makes **with the plugin installed**, in their own
repository — filing what they found, getting a request specced, taking a version
through review. Not an attempt made **on** this repository: releasing a version,
editing a skill and adding the case that holds it. Those are contribution steps
and they live in [CONTRIBUTING.md](../../CONTRIBUTING.md), because the person
doing them is the author rather than the persona.

When a workflow could be read either way, it is the wrong workflow.

# The bounded attempts

| Workflow | Trigger | Ends when |
|---|---|---|
| [`adopt-the-process`](adopt-the-process.feature) | the repository has outgrown what anybody can re-explain to a fresh session | the next change's pull request carries what the version leaves behind, and the pipeline refuses it until the specs move with it |

**One, and it is live.** `@planned` came off in
[`0008`](../changes/0008-the-gate-gets-something-to-hold.md): two feature files
under [`features/setup/`](../features/setup/) claim it and
[`12-setup-drives-the-sitting`](../../evals/12-setup-drives-the-sitting/prompt.md)
walks it. It names its arc,
[`trusting-the-spec-again`](../journeys/trusting-the-spec-again.md), attached by
[`0007`](../changes/0007-trusting-the-spec-again.md).

**What walks it is the sitting — and since
[`0015`](../changes/0015-the-sitting-uses-the-pipeline.md) the sitting ends where
the attempt does**, at a pull request in that repository, opened before the
hand-back rather than days later. What no case reaches is the pipeline's answer
to it: no eval workspace has a live remote or CI. So
[`the-sitting-ends-by-using-the-pipeline`](../features/setup/demonstration.feature)
stays `@planned` while its instruction ships, and what is held instead is the
honest account of what could not be watched. The tag says walked; the last leg is
watched by the adopter and by nobody here. That is written down rather than left
for somebody to discover from a green run.

One file per workflow, `.feature`, `@workflow:<id> @persona:<id> @journey:<id>`
on the first line, no `Rule:` anywhere in it, and the shape is in
[the template](../../templates/workflow.feature).

## Reading this as a map

This paragraph is evaluative and the [journeys](../journeys/README.md) are
descriptive; they are not the same document and must not collapse into one.

**Every other attempt is downstream of this one, which is the argument for
keeping it short rather than thorough.** Adoption is the only workflow here that
somebody performs once per repository — everything else they do, they do
repeatedly and forever afterwards. So a step added here is paid once and a step
added anywhere else is paid daily, and the trade almost always runs the wrong
way: **a change that lengthens adoption has to name which later attempt it
shortens in exchange, or it is buying nothing.**

The corollary is the one worth guarding. The attempt ends at the *first change
after* the install, not at the install — so making setup itself feel finished
sooner, while leaving the layers empty behind it, does not shorten this workflow.
It moves the cost somewhere nothing measures.

## Three more attempts, not written yet

Filing what they found; getting a request specced and approved; taking a version
through review. All three are real and all three have happened many times over
in `todo-change` — but none of them has had its own occasion interviewed, and a
workflow cut from a guess has to be cut twice. Each gets its own change.

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

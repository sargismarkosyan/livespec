# Spec 2026-11-23: the rules in the repository

- **Status:** approved in advance, by the maintainer, 2026-11-23 ("It has to be enforced by the rule set so that when they are adopting a newer version of the livespec, they will deliberately pay attention of the MR descriptions")
- **Issue:** [#252](https://github.com/sargismarkosyan/livespec/issues/252)
- **Sketch:** not drawn — approval given in advance

## Who this is for

**[`agent-accelerated-owner`](../personas/agent-accelerated-owner.md), in [`adopt-the-process`](../workflows/adopt-the-process.feature)**, at *Putting it in* and *The changes after*: whoever, or whatever agent, opens a pull request in their repository, including one that never loads this plugin.

## The job behind the request

When the plugin learns how a good pull request description is written, every repository using it writes them that way, by whichever agent or person opens one.

## Why now

[`0086`](0086-the-why-before-the-what.md) put the description rules in the method only. On 2026-11-23, two repositories on 3.15.0 showed what that costs ([#252](https://github.com/sargismarkosyan/livespec/issues/252)). helios/project-metrics-mfe's first MR added three headings beside a one-checkbox template, ran to about 312 words, and named its tracker item by a bare URL. helios/wf-developer-agents' context file says how to open an MR and never points at the rules. An agent that does not load the plugin cannot meet them at all, and nothing in an upgrade asks a repository to.

## The end value

The repository holds how a description is written there, for its own template, platform and tracker, linked from the step that opens a pull request. Each time the plugin's guideline changes, the next upgrade asks for that file again.

**How we would know it worked:** `check:pr-body-rules` reads open for bindings with no rules row, for a file that is not there, and for a context file that does not link it. With all three in place it asks for a reading. A change to the guideline that does not revise the check cannot merge here.

## What changes

1. **[`templates/pull-request.md`](../../templates/pull-request.md)**, new. The rules, as blanks a repository fills: its template's fields and where the rest goes, the point, its closing line and how its references are written, what else a body carries there, the length, what is left out, and the steps before publishing.
2. **[The bindings template](../../templates/bindings.md)** gains the key row ***Pull request description rules***: the file, `specs/setup/pull-requests.md` unless named.
3. **`check:pr-body-rules`** (judgment, severity wiring) in [`requirements.md`](../../method/requirements.md) and `tools/doctor.py`. It reads open where the row, the file or the context file's link is missing. Otherwise it puts the file to a reading against [`repository.md`](../../method/repository.md#and-the-point-before-the-evidence) and the template as they stand. As a wiring line, an open answer is owed in an upgrade, one approved item at a time.
4. **[`repository.md`](../../method/repository.md#and-the-point-before-the-evidence)**: the repository holds the rules for itself, and why. A template with no field for the point gets it above the first heading as plain lines, with the folded evidence after the last field.
5. **[`claude-md.md`](../../method/claude-md.md)** item 6: the step that opens a pull request links the rules.
6. **[`setup`](../../skills/setup/SKILL.md)** writes the file in section 5, links it in section 6, and writes its own pull request to it.
7. **The release gate here** refuses a change to the guideline's section or the template unless `## Ids` revises or adds `check:pr-body-rules`. That revision is what makes the next upgrade ask.
8. **This repository** gets its own file. [`CLAUDE.md`](../../CLAUDE.md) step 6 links it instead of listing what a body owes.

**Rules added or changed**:

| Rule id | Feature file | New or changed |
|---|---|---|
| `the-description-rules-are-the-repositorys-own` | [`wiring/the-description-rules.feature`](../features/wiring/the-description-rules.feature) | new |
| `the-repository-template-is-filled-not-replaced` | [`showing/what-a-body-says.feature`](../features/showing/what-a-body-says.feature) | changed — where what a template has no field for goes |

## What this removes

The list of what a body owes in [`CLAUDE.md`](../../CLAUDE.md) step 6, which moves to this repository's rules file.

## What we are not doing

- **Copying the method.** [`claude-md.md`](../../method/claude-md.md) keeps the method's rules out of a repository. This file is not a copy: it holds what only the repository knows (its template, closing line, tracker and commands), and the general rules are written there in those terms. The revised check is what keeps it from drifting.
- **A gate on the description.** That is [#253](https://github.com/sargismarkosyan/livespec/issues/253), the next change.
- **A length gate.** The length stays a reading, as 0086 decided.
- **Rewriting a repository's template.** Changing it stays the repository's decision.

## Risks

- **A second place to edit.** A change to the guideline that forgets the template drifts. The release gate's refusal covers both files.
- **A long context file.** It gains one link, not the rules.

## Ids

added: `check:pr-body-rules`

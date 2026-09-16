# Bindings

The part of the process that is this repository's own: every command, threshold
and path the method leaves to the repository. Every skill reads this file first.
`setup` writes it from this template; `doctor` reads it back. **Nothing here is
the method** — a sentence that would survive being moved to another repository
belongs in the plugin, not here, and the audit tool reads only the table
headers and the stamp line below, so keep those as they are.

## The table

| | |
|---|---|
| **Verification** | `<the one command that runs every gate>` |
| **What it returns** | <each exit code and what it means> |
| **What it runs** | <the gates, in order> |
| **Before the push** | <the local hook, if any — opt-in, bypassable, and given no row anywhere> |
| **Language** | <language and version> |
| **Package manager** | <or "none"> |
| **Traceability gate** | `<command>` |
| **Coverage gate** | `<command>`, or *none — see What has no gate* |
| **Coverage thresholds** | <lines / branches / functions — the whole of what is in scope, or the figure chosen and why> |
| **What coverage does not reach** | <named in the tool's own config; pointed at from here, never listed here> |
| **Fault injection** | `<command>` — <what it breaks, and where the record of that is> |
| **Required checks** | <the names the platform has, read back from it> |
| **Tracker** | <the host, and the command that files there — or "there is no tracker"> |
| **Where the app runs** | `<command>`, or *nowhere — there is no app* |
| **Deliverable of a version** | <the picture and its form, or *nothing to see* and what stands in its place> |
| **What a change here must show** | <which changes owe a picture, in what form, and where it goes> |
| **A sketch is owed** | <which changes owe one before approval — a repository with no app still has change specs> |
| **CLAUDE.md ceiling** | <the size the file may not exceed, in a unit the gate reads — written from what the file is when the sitting has finished with it, with the command that reads it and the change that set it; raised only in the change that needs the room, and never above the limit the method names> |
| **What proves a rule** | <an ordinary test suite, or graded cases — and why> |
| **How a test claims its rule** | <the helper and its import> |
| **Rule discovery** | <where rules live and what one looks like> |
| **Spec-bound coverage** | <the rule-bound measure, or *not applicable* and why> |
| **Pull-request report** | <what produces it and where it posts; never a gate> |
| **Audit record** | `specs/setup/audit.md` — written by the audit, one line per check, replaced on every run |
| **What a contributor owes a release** | <label, changelog, picture, Gherkin, and the run under the verification command when the change touches the tests — whatever the pipeline cannot work out for itself> |

## Gate wiring

**Reconciled against livespec <version> on <date>.** One row per gate the
method names — including the ones not wired, which is the half a repository
otherwise forgets. A gate this repository has that the method does not name
gets a row too, with the `local:` prefix: held to the same states, required by
nothing.

A row reads *automated* (and names the command), *unobserved* (wired, and
nothing has yet watched it refuse a change), *not applicable* (with the reason
— a decision, not a gap, and `decided:` marks the ones that were chosen) or
*deferred* (since which change, and why). A row about anything outside the
tree carries how it was read back: the command, and when.

| id | gate | state | evidence |
|---|---|---|---|
| `gate:rule-to-test` | a live rule no test claims | <state> | <command, or why not> |
| `gate:test-to-rule` | a test claiming a rule that does not exist | | |
| `gate:planned-unclaimed` | a `@planned` rule or workflow that is claimed | | |
| `gate:feature-to-workflow` | a feature naming no workflow, or one that does not exist | | |
| `gate:workflow-to-feature` | a workflow claimed by no feature | | |
| `gate:workflow-walked` | a workflow walked by no test | | |
| `gate:workflow-to-persona` | a workflow naming no live persona | | |
| `gate:persona-to-workflow` | a persona named by no workflow | | |
| `gate:journey-to-workflow` | a journey naming a workflow that does not exist | | |
| `gate:workflow-to-journey` | a workflow naming no journey — warns, does not fail | | |
| `gate:structure` | one feature per file, unique ids, every rule with an example, no example outside a rule | | |
| `gate:coverage` | lines, branches, functions | | |
| `gate:boundary-double` | a rule-bound test doubling a boundary declared real | | |
| `gate:boundary-fake-suite` | a fake row naming no suite against the real thing | | |
| `gate:boundary-recorded-age` | a recorded row past its age | | |
| `gate:boundaries-table` | rule-bound tests present and no boundaries table | | |
| `gate:context-file-ceiling` | the context file past the ceiling the bindings name, or with no ceiling row | | |
| `gate:context-file-shape` | the context file missing, or without its loop, its commands, or its pointer to the bindings | | |
| `gate:skipped-test-claims-nothing` | a rule-bound test marked skipped, focused or expected to fail claims no rule | | |
| `gate:fewer-ran-than-exist` | the runner reporting fewer rule-bound tests than the tree holds | | |
| `gate:verified-to-fire` | every gate broken on purpose and seen to fire | | |

### The wiring that must never gate

| id | wiring | state | evidence |
|---|---|---|---|
| `wiring:pr-report` | the pull-request report | <state> | <what produces it — unobserved until one was watched arriving> |
| `wiring:rule-bound-measure` | the rule-bound measure, reported beside the gated number | <state> | <how, or why not> |
| `wiring:run-beside-claim` | the run beside the claim — the report printing the pipeline's own run next to the run block the pull request carries | <state> | <what prints it — unobserved until the two were watched disagreeing> |

### The boundaries

One row per thing the app talks to that is not its own code — the store, the
clock, the network and each service on it, the browser or terminal, the
identity. The names are this repository's; the prefix is the contract. A row
reads *real*, *fake*, *recorded*, *mocked* or *unreachable*, and says what it
leaves uncovered in the same breath.

| id | boundary | state | since | evidence |
|---|---|---|---|---|
| `boundary:<name>` | <what it is> | <state> | <change number> | <what reaches it from here, what keeps it honest, what it leaves uncovered> |

### Workarounds

What this repository does its own way because of a gap owned somewhere else.
Each row names what would end it; the row comes out when the workaround does.

| instead | gap | filed | ends when |
|---|---|---|---|

## The fault injection record

<the table the sitting produced, dated — or generated from the injector where
this repository's checks read it back>

## Branch protection

<read back from the platform, never inferred from the tree: whether a merge is
blocked, the check's name as the platform has it, who can bypass — with the
command that reads it again and the date>

## What has no gate, and what that misses

<what this repository deliberately leaves ungated, and what that costs>

## Notes from the sitting

<what is true of one machine rather than of the repository — the local hook,
what was left to the pipeline, the line somebody types to opt in>

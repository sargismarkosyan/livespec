# What a setup must hold

The list only; the reasoning is in [`gates.md`](gates.md).

## The ids

Everything an audit of the ledger is held to is one list, here, and nothing an
audit checks is enumerated anywhere else. Three tables: the gates a ledger
carries a row for, the two pieces of wiring that must never gate, and the
checks an audit makes. **Every id is permanent** — the same promise a rule id
carries, for the same reason: a ledger in a consuming repository names these
ids, and a renamed one orphans every ledger at once. A check that is no longer
asked is retired *in place*, with the version and what replaced it, so an old
row reads *retired — drop it* rather than *unknown id*. A rename is a
retirement and a new id. The *aliases* column carries the labels ledgers used
before ids existed, so an audit can match an old row to its id and write the
id in.

*kind* says who answers a check: **mechanical** — a script, from the record,
the same way every time; **judgment** — a person or a model, from the command
the bindings name. *since* is the plugin release the check or gate arrived in,
and a consuming repository whose stamp is earlier than a row's *since* has
never been asked it. **It is written by the release, never by a person**: a
new row reads `next` until the merge that ships it, and the release step
writes the version in the same commit as the manifest and the changelog
entry. A retirement reads `next` the same way. The pull request that adds or
retires a row says so in an `## Ids` section, and the gate holds what it says
to the table's diff. *severity* orders what an audit reports — *platform*
before *boundary* before *wiring* before *record*. *revised* is the release in
which a row's meaning last changed under the same id, so a repository answers it
again; the release writes it as it writes *since*. A pull request sets `next` and
says `revised:` in `## Ids`; one that only rewords says `reworded:`.

### The gates a ledger carries

| id | kind | since | severity | retired | aliases | meaning | revised |
|---|---|---|---|---|---|---|---|
| `gate:rule-to-test` | gate | 0.6.0 | wiring | — | rule → test · rule → case | a live rule no test claims fails | — |
| `gate:test-to-rule` | gate | 0.6.0 | wiring | — | test → rule · case → rule | a test claiming a rule that does not exist fails | — |
| `gate:planned-unclaimed` | gate | 0.6.0 | wiring | — | planned rule with a test | a `@planned` rule or workflow that is claimed fails — the tag should have come off | — |
| `gate:feature-to-workflow` | gate | 0.6.0 | wiring | — | feature → workflow | a feature naming no workflow, or a workflow that does not exist, fails | — |
| `gate:workflow-to-feature` | gate | 0.6.0 | wiring | — | workflow → feature | a workflow claimed by no feature fails | — |
| `gate:workflow-walked` | gate | 0.6.0 | wiring | — | workflow → test · workflow → case (walked end to end) | a workflow walked by no test fails | — |
| `gate:workflow-to-persona` | gate | 0.6.0 | wiring | — | workflow → persona | a workflow naming no live persona fails | — |
| `gate:persona-to-workflow` | gate | 0.6.0 | wiring | — | persona → workflow | a persona named by no workflow fails | — |
| `gate:journey-to-workflow` | gate | 0.6.0 | wiring | — | journey → workflow | a journey naming a workflow that does not exist fails | — |
| `gate:workflow-to-journey` | gate | 0.6.0 | wiring | — | workflow → journey | a workflow naming no journey warns, and does not fail | — |
| `gate:workflow-to-phase` | gate | 1.29.0 | wiring | — | | a workflow naming a phase that no journey it names has fails; naming none passes | — |
| `gate:structure` | gate | 0.6.0 | wiring | — | structure | one feature per file, unique ids, every rule with an example, no example outside a rule | — |
| `gate:coverage` | gate | 0.6.0 | wiring | — | coverage · coverage — lines, branches, functions | a module under the thresholds fails | — |
| `gate:boundary-double` | gate | 1.2.0 | boundary | — | a rule-bound test doubling a boundary declared real | a rule-bound test standing a double in for a boundary reading real fails | — |
| `gate:boundary-fake-suite` | gate | 1.2.0 | boundary | — | | a fake row naming no suite against the real thing fails | — |
| `gate:boundary-recorded-age` | gate | 1.2.0 | boundary | — | | a recorded row past the age the bindings set fails | — |
| `gate:boundaries-table` | gate | 1.2.0 | boundary | — | | rule-bound tests present and no boundaries table fails | — |
| `gate:context-file-ceiling` | gate | 1.9.0 | wiring | — | | the context file larger than the ceiling the bindings name, a context file with no ceiling row, or a ceiling above the limit the method names, fails | — |
| `gate:part-past-its-ceiling` | gate | 1.32.0 | wiring | — | | a part larger than the ceiling the bindings' Ceilings row names, or no Ceilings row, fails | — |
| `gate:context-file-shape` | gate | 1.9.0 | wiring | — | | the context file missing, or without its loop, its commands, or its pointer to the bindings, fails | — |
| `gate:skipped-test-claims-nothing` | gate | 1.12.0 | wiring | — | | a rule-bound test marked skipped, focused or expected to fail claims no rule, and fails | — |
| `gate:fewer-ran-than-exist` | gate | 1.12.0 | wiring | — | | the runner reporting fewer rule-bound tests than the tree holds fails | — |
| `gate:change-number-unique` | gate | 1.23.0 | wiring | — | | two change specs sharing a number fail, whatever their slugs; a gap does not | — |
| `gate:feature-to-feature` | gate | 1.28.0 | wiring | — | | a feature using a feature that does not exist, or carrying @uses on a rule, fails | — |
| `gate:workflow-budget` | gate | 1.33.0 | wiring | — | | a count a workflow walk makes past the budget the policy file sets fails; a time carries no budget | — |
| `gate:workflow-regression-answered` | gate | 1.35.0 | wiring | — | | a walk past its allowance whose workflow the pull request's Performance section does not name fails | — |
| `gate:crossing-names-a-boundary` | gate | 1.14.0 | boundary | — | | a rule tagged as crossing a boundary the bindings declare no row for fails | — |
| `gate:verified-to-fire` | gate | 0.6.0 | wiring | — | both gates verified to fire | every gate is broken on purpose and seen to fire | — |

### The wiring that must never gate

| id | kind | since | severity | retired | aliases | meaning | revised |
|---|---|---|---|---|---|---|---|
| `wiring:pr-report` | wiring | 0.21.0 | wiring | — | the pull-request report | the report on every pull request, unobserved until one was watched arriving | — |
| `wiring:rule-bound-measure` | wiring | 0.21.0 | wiring | — | the rule-bound measure | the rule-bound measure reported beside the gated number | — |
| `wiring:run-beside-claim` | wiring | 1.13.0 | wiring | — | the run beside the claim | the report re-running the verification command and printing what it saw beside what the body says — unobserved until the two were watched disagreeing | — |
| `wiring:workflow-cost` | wiring | 1.33.0 | wiring | — | the cost of a walk | what the change cost each workflow walk, base against branch, on the report — unobserved until it was watched reporting a move | — |

Two prefixes a repository fills itself and this table never lists:
`boundary:<name>`, one per thing the app talks to, named in the sitting and
never derived; and `local:<name>`, a gate the repository added that the method
does not name — held to the same states, required by nothing.

### The checks an audit makes

| id | kind | since | severity | retired | aliases | meaning | revised |
|---|---|---|---|---|---|---|---|
| `check:key-table-shape` | mechanical | 3.8.0 | record | — | | every row of the template's key table is in the bindings, by its name or its graded-case form, the pull request template and the section a release publishes among them | next |
| `check:ledger-shape` | mechanical | 1.6.0 | record | — | | the three tables and the stamp line are in the shape the template gives them, the gate and wiring rows each with the version it was reconciled at | 1.37.0 |
| `check:stamp-present` | mechanical | 0.21.0 | record | — | | the ledger carries the version it was reconciled against | — |
| `check:stamp-derived` | mechanical | 1.37.0 | record | — | | the stamp line reads the oldest version a gate or wiring row was reconciled at | — |
| `check:stamp-range` | mechanical | 1.1.0 | record | — | | the entries between the stamp and the plugin installed are listed | — |
| `check:stamp-ahead` | mechanical | 1.1.0 | record | — | | a stamp ahead of the plugin installed is said, and no range read | — |
| `check:range-empty-said` | mechanical | 1.1.0 | record | — | | a stamp at the plugin installed is said in a line | — |
| `check:changelog-reachable` | mechanical | 1.1.0 | record | — | | the plugin's changelog can be read from here | — |
| `check:entry-moved-here` | judgment | 1.1.0 | record | — | | each entry in the range moved something this repository holds, or is passed over in a line | — |
| `check:row-state-legal` | mechanical | 0.21.0 | record | — | | every ledger row is in one of the four states | — |
| `check:row-evidence` | mechanical | 0.21.0 | record | — | | an automated or unobserved row names a command; a deferred row names its change; a row about the outside carries how it was read | — |
| `check:row-uncovered` | judgment | 0.21.0 | wiring | — | | what a row leaves uncovered is named, and true | — |
| `check:number-from-config` | judgment | 0.31.0 | wiring | — | | a number a gate enforces is read from the config the gate reads | — |
| `check:demand-is-a-ratchet` | judgment | 0.31.0 | wiring | — | | a demand equal to today's score is reported as measured rather than chosen, unless it is the whole of what is in scope | — |
| `check:exclusions-in-config` | judgment | 0.31.0 | wiring | — | | what the demand does not reach lives in the tool's config, not only in the bindings | — |
| `check:na-vs-tree` | mechanical | 0.21.0 | record | — | | a not-applicable row's reason is not contradicted by the tree — no layer, or no code, where the tree has them — and a reason it cannot read is named | 3.4.0 |
| `check:row-per-gate` | mechanical | 0.21.0 | wiring | — | | every gate in the table above has a row | — |
| `check:real-starts-here` | judgment | 1.2.0 | boundary | — | | what a real row names can be started from here | — |
| `check:real-not-doubled` | judgment | 1.2.0 | boundary | — | | no rule-bound test stands a double in for a boundary reading real | — |
| `check:fake-suite-green` | judgment | 1.2.0 | boundary | — | | a fake row's suite against the real thing exists, and was last green when the row says | — |
| `check:recorded-age` | mechanical | 1.2.0 | boundary | — | | a recorded row is within the age the bindings set | — |
| `check:mocked-clock` | mechanical | 1.2.0 | boundary | — | | a mocked row is not past the two-change clock | — |
| `check:merge-blocked` | judgment | 0.21.0 | platform | — | | a merge is actually blocked when the required check fails | — |
| `check:check-name` | judgment | 0.21.0 | platform | — | | the required check's name is the one the platform has | — |
| `check:who-bypasses` | judgment | 0.21.0 | platform | — | | who can bypass is read back, tokens and keys included | — |
| `check:credentials-present` | judgment | 0.21.0 | platform | — | | a credential the bindings claim is missing is read back from where the platform keeps it | — |
| `check:merged-branch-deleted` | judgment | 1.20.0 | platform | — | | the platform deletes a merged pull request's branch, so a pull request stacked on it is retargeted to the main branch | — |
| `check:merged-off-main` | judgment | 1.20.0 | wiring | — | | no pull request merged since the stamp into a branch other than main is missing from main | — |
| `check:main-green` | judgment | 3.3.0 | platform | — | | the main branch's pipeline is green now, and was green on every run since the last audit | — |
| `check:merge-queue` | judgment | 1.21.0 | platform | — | | how several pull requests merge — the platform's queue and the event its checks run on, or the fallback's settings — is what the platform has | — |
| `check:read-back-age` | mechanical | 3.7.0 | record | — | | every date the bindings say something was read back from outside the tree is no older than the last audit, which should have read it again | — |
| `check:read-back-or-not` | mechanical | 0.21.0 | record | — | | every judgment line is read back with its command, or not read with why | — |
| `check:prose-phrases` | judgment | 0.21.0 | record | — | | the bindings and the layers' READMEs are read for a gap in words — *not built yet*, *not written yet*, *uninterviewed*, *to do*, *we should*, *for now* | 3.4.0 |
| `check:second-table` | mechanical | 0.21.0 | wiring | — | | the table for wiring that must never gate exists | — |
| `check:pr-report-row` | mechanical | 0.21.0 | wiring | — | | it holds the row for the pull-request report | — |
| `check:rule-bound-row` | mechanical | 0.21.0 | wiring | — | | it holds the row for the rule-bound measure | — |
| `check:run-row` | mechanical | 1.13.0 | wiring | — | | it holds the row for the run beside the claim | — |
| `check:walk-cost-row` | mechanical | 1.33.0 | wiring | — | | it holds the row for the cost of each workflow walk | — |
| `check:sketch-row` | mechanical | 0.27.0 | record | — | | the bindings say which changes owe a sketch | — |
| `check:picture-row` | mechanical | 0.29.0 | record | — | | the bindings say what a change here must show, and it is not the sketch row | — |
| `check:trees-row` | mechanical | 1.17.0 | record | — | | the bindings say where trees live and what makes, lists and cleans them, and the context file's commands carry that command | — |
| `check:fresh-tree-green` | judgment | 1.17.0 | wiring | — | | a throwaway tree made by the command the bindings name runs verification green, and the same command cleans it | — |
| `check:claim-row` | mechanical | 1.19.0 | record | — | | the bindings name the marker that says an issue is taken, and the commands that put it on and list it | — |
| `check:claims-in-flight` | judgment | 1.19.0 | record | — | | every open issue carrying the marker has a branch, a tree or a pull request behind it, and none is released by the audit | — |
| `check:skill-names` | mechanical | 1.0.0 | record | — | | every skill the record instructs by exists in this plugin | — |
| `check:host-enabled` | mechanical | 3.5.0 | wiring | — | | every host in use here — the one running the audit, and each the tree shows — loads the plugin from a committed declaration | — |
| `check:host-pin-current` | mechanical | 3.10.0 | wiring | — | | where the repository pins livespec for Pi, the ref is a release tag not below the ledger's ceiling, or a non-release ref the bindings say was kept on purpose | — |
| `check:one-context-file` | mechanical | 1.25.0 | wiring | — | | one instructions file at the root, so the one the gates hold is the one every host reads | — |
| `check:word-not-a-skill` | judgment | 1.0.0 | record | — | | the same word used as ordinary prose is left alone | — |
| `check:loop-per-claude-md` | judgment | 1.1.0 | record | — | | the context file carries every item the method asks of it, each true, and its rules list carries each rule broken here since the last audit | 3.6.0 |
| `check:deferred-clock` | mechanical | 0.21.0 | wiring | — | | no row is deferred across two changes | — |
| `check:hook-no-row` | mechanical | 0.26.0 | record | — | | a local hook has no row in either table | — |
| `check:sorted-by-severity` | mechanical | 0.21.0 | record | — | | what is open is reported dangerous first | — |
| `check:loop-followed` | mechanical | 3.2.0 | record | — | | every change merged since the last audit has a change spec whose `spec NNNN:` commit came first and whose header says what became of its sketch, or takes the light path with an issue | — |
| `check:record-only` | mechanical | 0.21.0 | record | — | | the audit's corrections touched the record and nothing else | — |
| `check:last-line-command` | mechanical | 1.3.0 | record | — | | where wiring is left, the last line is the command that starts the sitting, with the rows after it | — |
| `check:no-line-when-clear` | mechanical | 1.3.0 | record | — | | where nothing is left for the sitting, no such line | — |

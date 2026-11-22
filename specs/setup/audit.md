# Audit record

**Audited 2026-11-22 · livespec 1.32.1 · stamp 1.32.1 · HEAD 553f8f3 · audit 7**

49 checks · 1 open · written by the audit, replaced on every run

| id | state | since | evidence |
|---|---|---|---|
| `check:ledger-shape` | clear | 2026-09-16 | three tables with the template's headers; stamp line present |
| `check:stamp-present` | clear | 2026-09-16 | Reconciled against livespec 1.32.1 on 2026-11-21 |
| `check:stamp-range` | clear | 2026-09-16 | stamp 1.32.1 is the plugin installed — nothing between |
| `check:stamp-ahead` | clear | 2026-09-16 | stamp 1.32.1 is not ahead of 1.32.1 |
| `check:range-empty-said` | clear | 2026-09-16 | nothing between 1.32.1 and the plugin installed to reconcile |
| `check:changelog-reachable` | clear | 2026-09-16 | 75 entries, newest 1.32.1, at /Users/sargism/Projects/livespec/.worktrees/doctor-audit-1.32.1/CHANGELOG.md |
| `check:entry-moved-here` | n/a | 2026-09-16 | no entries between the stamp and the plugin installed |
| `check:row-state-legal` | clear | 2026-09-16 | 30 gate rows, 3 wiring rows, 4 boundary rows, every state legal |
| `check:row-evidence` | clear | 2026-09-16 | every row carries the evidence its state owes |
| `check:row-uncovered` | clear | 2026-09-16 | read: the 33 ledger rows (awk over the Gate wiring table) named nothing they leave uncovered, which gates.md "And a row says what it leaves uncovered" requires; corrected in this audit with one paragraph above the table: every automated row runs over the whole of what it names (trace.py: specs/, evals/, tests/; checks.py: skills, manifests, markdown), and what no gate covers is coverage of tools/ and .github/scripts/ and eval scores |
| `check:number-from-config` | n/a | 2026-09-16 | no coverage gate here |
| `check:demand-is-a-ratchet` | n/a | 2026-09-16 | no coverage gate here |
| `check:exclusions-in-config` | n/a | 2026-09-16 | no coverage gate here |
| `check:na-vs-tree` | clear | 2026-09-16 | 8 not-applicable row(s) read against the tree, none contradicted; decided rows left alone |
| `check:row-per-gate` | clear | 2026-09-16 | 29 of 29 ids have a row; 4 local: row(s) |
| `check:real-starts-here` | not-read | 2026-09-16 | boundary:platform started: gh api repos/sargismarkosyan/livespec/rules/branches/main answered. boundary:model-session not started: run: python3 evals/runner/run.py … refuses without --i-approve-the-cost, which is the maintainer's to add, a paid run; claude --version answered 2.1.289 (Claude Code), so the CLI it starts is present |
| `check:real-not-doubled` | clear | 2026-09-16 | run: python3 .github/scripts/trace.py → ✔ traceability: 151 live rule(s) traced; gate:boundary-double reads not applicable (no rule-bound test stands in for a real boundary: the cases drive claude -p themselves, the tests are standard library) |
| `check:fake-suite-green` | n/a | 2026-09-16 | no boundary row reads fake |
| `check:recorded-age` | n/a | 2026-09-16 | no boundary row reads recorded |
| `check:mocked-clock` | n/a | 2026-09-16 | no row reads mocked |
| `check:merge-blocked` | clear | 2026-09-16 | run: gh api repos/sargismarkosyan/livespec/rules/branches/main → pull_request and required_status_checks rules apply, strict: true; ruleset 21391215 enforcement active |
| `check:check-name` | clear | 2026-09-16 | run: gh api repos/sargismarkosyan/livespec/rules/branches/main → required contexts "repository checks" and "plugin validate", integration_id 15368, the job names the bindings give |
| `check:who-bypasses` | clear | 2026-09-16 | run: gh api repos/sargismarkosyan/livespec/rulesets/21391215 → bypass_actors: one, DeployKey always; current_user_can_bypass: never; gh api repos/sargismarkosyan/livespec/keys → one write key, 161238524 livespec release, as the bindings say |
| `check:credentials-present` | n/a | 2026-09-16 | the bindings claim no credential is missing |
| `check:merged-branch-deleted` | clear | 2026-11-22 | run: gh api repos/sargismarkosyan/livespec --jq .delete_branch_on_merge → true |
| `check:merged-off-main` | clear | 2026-11-22 | run: gh pr list --state merged --limit 50 --json number,baseRefName,headRefOid → #199, #200, #202, #203, #204 merged since 2026-11-21, every base main; none merged elsewhere |
| `check:merge-queue` | clear | 2026-11-22 | run: gh api repos/sargismarkosyan/livespec --jq '{allow_update_branch, allow_auto_merge}' → both true, the fallback the row names |
| `check:read-back-or-not` | clear | 2026-09-16 | 13 judgment line(s) read back with their command, 1 not read with why |
| `check:prose-phrases` | clear | 2026-09-16 | read: none of the four phrases in the prose |
| `check:second-table` | clear | 2026-09-16 | present, 3 row(s) |
| `check:pr-report-row` | clear | 2026-09-16 | automated — [`report.py`](../../.github/scripts/report.py), posted by [` |
| `check:rule-bound-row` | clear | 2026-09-16 | not applicable — there is no coverage here at all, gated or otherwise — *What |
| `check:run-row` | clear | 2026-11-22 | automated — [`report.py`](../../.github/scripts/report.py) prints the la |
| `check:sketch-row` | clear | 2026-09-16 | *a sketch is owed*: by every change spec, before approval — there is no app here, and the |
| `check:picture-row` | clear | 2026-09-16 | *deliverable of a version*: the pull request description. No picture in any form — see *What does |
| `check:trees-row` | clear | 2026-11-22 | *trees*: `python3 .github/scripts/trees.py`, and the context file carries it |
| `check:fresh-tree-green` | clear | 2026-11-22 | run: python3 .github/scripts/trees.py new doctor-throwaway, then verify.py in it → ✔ verification green — 5 gates; trees.py clean removed only doctor-throwaway; the tree list is as it was (doctor-audit-1.32.1, spec-0089-a-workflow-walk-reports-its-cost) |
| `check:claim-row` | clear | 2026-11-22 | *claiming an issue*: `in-progress` |
| `check:claims-in-flight` | open | 2026-11-22 | run: gh issue list --label in-progress → #187, #188. #187 claim (2026-11-21, session not exposed): tree .worktrees/spec-0089-a-workflow-walk-reports-its-cost exists with work in it — live. #188 claim (2026-11-21, ~1 day, session 01a1f57c-518c-73ec-94db-af4901b54551): branch spec-0088-the-list-in-its-own-file deleted on merge, tree cleaned, pull request #204 merged — all three gone, because #188a shipped and #188b has not started. Closed by the claimant re-claiming #188 for #188b or taking the marker off; released by nobody here |
| `check:skill-names` | clear | 2026-09-16 | the record instructs by no skill name |
| `check:one-context-file` | clear | 2026-11-22 | one instructions file at the root: CLAUDE.md |
| `check:word-not-a-skill` | clear | 2026-09-16 | read: CLAUDE.md:42,43,66 and specs/setup/README.md:265,304,336,343 — todo, refine-spec, record-clip, setup, doctor are the current skills, named as references; left alone |
| `check:loop-per-claude-md` | clear | 2026-09-16 | read: CLAUDE.md § The loop against method/claude-md.md § What must be there, item 6 — eight steps; step 4 says the approver holds the spec and the sketch drawn from it; step 6 reads back what the pull request will close with the bindings' command; step 5 deletes what the change made dead |
| `check:deferred-clock` | clear | 2026-09-16 | no row reads deferred |
| `check:hook-no-row` | clear | 2026-09-16 | no row in any table is a hook |
| `check:sorted-by-severity` | clear | 2026-09-16 | the reply lists what is open platform › boundary › wiring › record |
| `check:record-only` | clear | 2026-09-16 | the working tree is clean |
| `check:last-line-command` | n/a | 2026-09-16 | nothing is left for the sitting |
| `check:no-line-when-clear` | clear | 2026-09-16 | no line sends anybody to a sitting |

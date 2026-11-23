# Audit record

**Audited 2026-11-23 · livespec 3.18.0 · stamp 3.18.0 · HEAD d7142aa · audit 8**

58 checks · 1 open · written by the audit, replaced on every run

| id | state | since | evidence |
|---|---|---|---|
| `check:key-table-shape` | clear | 2026-11-23 | all 36 of the template's rows, by name or graded-case form |
| `check:pr-body-rules` | clear | 2026-11-23 | read: `specs/setup/pull-requests.md` against `method/repository.md`'s *And the point, before the evidence* and `templates/pull-request.md` at 3.18.0 — the template (*none* here, so starting from its file does not arise), the body's order, the point, the closing line and references, what a body carries, the length with what it counts, what is left out and the steps before publishing are each there and true |
| `check:ledger-shape` | clear | 2026-09-16 | three tables with the template's headers; stamp line present |
| `check:stamp-present` | clear | 2026-09-16 | Reconciled against livespec 3.18.0 on 2026-11-23 |
| `check:stamp-derived` | clear | 2026-11-23 | the stamp line reads 3.18.0, the oldest row's version |
| `check:stamp-range` | clear | 2026-09-16 | stamp 3.18.0 is the plugin installed — nothing between |
| `check:stamp-ahead` | clear | 2026-09-16 | stamp 3.18.0 is not ahead of 3.18.0 |
| `check:range-empty-said` | clear | 2026-09-16 | nothing between 3.18.0 and the plugin installed to reconcile |
| `check:changelog-reachable` | clear | 2026-09-16 | 108 entries, newest 3.18.0, at /Users/sargism/Projects/livespec/.worktrees/audit-2026-11-23/CHANGELOG.md |
| `check:entry-moved-here` | n/a | 2026-09-16 | no entries between the stamp and the plugin installed |
| `check:row-state-legal` | clear | 2026-09-16 | 31 gate rows, 4 wiring rows, 4 boundary rows, every state legal |
| `check:row-evidence` | clear | 2026-09-16 | every row carries the evidence its state owes |
| `check:row-uncovered` | clear | 2026-09-16 | read: `specs/setup/README.md` *What the rows leave uncovered* — every automated row runs over the whole of what it names; what no gate covers (the Python under `tools/` and `.github/scripts/` has tests and no coverage measure, an eval score is never gated) is still true at 3.18.0 |
| `check:number-from-config` | n/a | 2026-09-16 | no coverage gate here |
| `check:demand-is-a-ratchet` | n/a | 2026-09-16 | no coverage gate here |
| `check:exclusions-in-config` | n/a | 2026-09-16 | no coverage gate here |
| `check:na-vs-tree` | clear | 2026-09-16 | 9 not-applicable row(s) read against the tree, none contradicted; decided rows left alone; not read against the tree, the reason naming nothing it holds: local:journey-freshness, local:features-piled-up, gate:boundary-double, gate:boundary-fake-suite, gate:boundary-recorded-age, gate:boundaries-table, gate:workflow-budget, gate:workflow-regression-answered, wiring:workflow-cost |
| `check:row-per-gate` | clear | 2026-09-16 | 31 of 31 ids have a row; 4 local: row(s) |
| `check:real-starts-here` | not-read | 2026-09-16 | boundary:platform started: `gh api repos/sargismarkosyan/livespec/rulesets/21391215` answered. boundary:model-session not started: its command, `python3 evals/runner/run.py … --i-approve-the-cost`, bills the maintainer's account and is the maintainer's to run — refused here; the maintainer can read it |
| `check:real-not-doubled` | clear | 2026-09-16 | run: `python3 .github/scripts/trace.py` — the one rule crossing boundary:platform, `a-claim-outside-the-tree-is-read-back`, is claimed by case 24 against a repository that does not exist, the platform refusing as its example asks; no double stands in. The eleven crossing boundary:consuming-repository sit on that row's decided *unreachable* |
| `check:fake-suite-green` | n/a | 2026-09-16 | no boundary row reads fake |
| `check:recorded-age` | n/a | 2026-09-16 | no boundary row reads recorded |
| `check:mocked-clock` | n/a | 2026-09-16 | no row reads mocked |
| `check:merge-blocked` | clear | 2026-09-16 | run: `gh api repos/sargismarkosyan/livespec/rules/branches/main` — `pull_request` and `required_status_checks` (`repository checks`, `plugin validate`, strict) on `main`, ruleset 21391215 `active`: a red check blocks the merge |
| `check:check-name` | clear | 2026-09-16 | run: `gh api repos/sargismarkosyan/livespec/rulesets/21391215` — `repository checks@15368` and `plugin validate@15368`, the job names `checks.yml` gives, not its filename |
| `check:who-bypasses` | clear | 2026-09-16 | run: `gh api repos/sargismarkosyan/livespec/rulesets/21391215` — one bypass actor, `DeployKey` always; `gh api repos/sargismarkosyan/livespec/keys` lists one write key, `livespec release` (161238524), its secret `RELEASE_DEPLOY_KEY`; `current_user_can_bypass: never`. As the bindings say |
| `check:credentials-present` | n/a | 2026-09-16 | the bindings claim no credential is missing |
| `check:merged-branch-deleted` | clear | 2026-11-22 | run: `gh api repos/sargismarkosyan/livespec --jq .delete_branch_on_merge` — `true` |
| `check:merged-off-main` | clear | 2026-11-22 | run: `gh pr list --state merged --limit 50 --json number,baseRefName,mergedAt` — none merged since 2026-11-23 into anything but `main` |
| `check:main-green` | clear | 2026-11-23 | run: `gh run list --branch main --workflow checks.yml --limit 80` — 71 runs since the audit of 2026-11-22, every one `success`; the latest on d7142aa |
| `check:merge-queue` | clear | 2026-11-22 | run: `gh api repos/sargismarkosyan/livespec --jq '{allow_update_branch, allow_auto_merge}'` — both `true`, the fallback's two settings |
| `check:read-back-age` | clear | 2026-11-23 | 2 read-back(s), none older than the last audit on 2026-11-22 |
| `check:read-back-or-not` | clear | 2026-09-16 | 15 judgment line(s) read back with their command, 1 not read with why |
| `check:prose-phrases` | clear | 2026-09-16 | read: `specs/workflows/README.md:51` — *Three more attempts, not written yet* names three real workflows nobody has interviewed, the state `CLAUDE.md` states; nothing is on a clock |
| `check:second-table` | clear | 2026-09-16 | present, 4 row(s) |
| `check:pr-report-row` | clear | 2026-09-16 | automated — [`report.py`](../../.github/scripts/report.py), posted by [` |
| `check:rule-bound-row` | clear | 2026-09-16 | not applicable — no coverage is measured here, decided (`gate:coverage`), so |
| `check:run-row` | clear | 2026-11-22 | automated — [`report.py`](../../.github/scripts/report.py) prints the la |
| `check:walk-cost-row` | clear | 2026-11-23 | not applicable — the same reason: walking a workflow here spends money only t |
| `check:sketch-row` | clear | 2026-09-16 | *a sketch is owed*: by every change spec, before approval — there is no app here, and the |
| `check:picture-row` | clear | 2026-09-16 | *deliverable of a version*: the pull request description. No picture in any form — see *What does |
| `check:trees-row` | clear | 2026-11-22 | *trees*: `python3 .github/scripts/trees.py`, and the context file carries it |
| `check:fresh-tree-green` | clear | 2026-11-22 | run: `python3 .github/scripts/trees.py new audit-throwaway-2026-11-23`, then `python3 .github/scripts/verify.py` in it at af66338 — green, 159/159 faults; removed by name, the tree list as it was, nothing else cleaned |
| `check:claim-row` | clear | 2026-11-22 | *claiming an issue*: `in-progress` |
| `check:claims-in-flight` | clear | 2026-11-23 | run: `gh issue list --label in-progress` — #256 is this audit's own, its tree `audit-2026-11-23` here; #197's claim names `spec-0117-setup-from-its-principles`, whose tree is here with uncommitted work. None released |
| `check:skill-names` | clear | 2026-09-16 | the record instructs by no skill name |
| `check:host-pin-current` | n/a | 2026-11-23 | the repository pins no livespec ref for Pi |
| `check:host-enabled` | clear | 2026-11-23 | Claude Code: `livespec@livespec` in .claude/settings.json; Pi: `..` in .pi/settings.json, a livespec checkout |
| `check:one-context-file` | clear | 2026-11-22 | one instructions file at the root: CLAUDE.md |
| `check:word-not-a-skill` | clear | 2026-09-16 | read: `specs/setup/README.md:366` and `:886` are dated accounts of what `doctor` did, left as written; `:648` is the platform read-back, rewritten with today's; the rest is the word as prose |
| `check:loop-per-claude-md` | clear | 2026-09-16 | read: `CLAUDE.md` against the ten items of `method/claude-md.md` — each there and true; its step 6 links the description rules. Corrected in the record: its rules list gains the `Sketch:` line the history showed broken (check:loop-followed), and the ceiling rises to 127 with the reason |
| `check:deferred-clock` | clear | 2026-09-16 | no row reads deferred |
| `check:hook-no-row` | clear | 2026-09-16 | no row in any table is a hook |
| `check:sorted-by-severity` | clear | 2026-09-16 | the reply lists what is open platform › boundary › wiring › record |
| `check:loop-followed` | open | 2026-11-23 | 2 of 71 change(s) since 553f8f3: `7182ff9` Merge pull request #207 from sargismarkosyan/spec-0090-measu: 0090-measure-what-you-control.md has no Sketch line; `d2846af` Merge pull request #208 from sargismarkosyan/spec-0091-a-reg: 0091-a-regression-is-acknowledged.md has no Sketch line |
| `check:record-only` | clear | 2026-09-16 | nothing outside the record is changed in the working tree |
| `check:last-line-command` | n/a | 2026-09-16 | nothing is left for the sitting |
| `check:no-line-when-clear` | clear | 2026-09-16 | no line sends anybody to a sitting |

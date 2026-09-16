# Audit record

**Audited 2026-09-16 · livespec 1.7.0 · stamp 1.7.0 · HEAD cdcb3a0 · audit 4**

40 checks · 0 open · written by the audit, replaced on every run

| id | state | since | evidence |
|---|---|---|---|
| `check:ledger-shape` | clear | 2026-09-16 | three tables with the template's headers; stamp line present |
| `check:stamp-present` | clear | 2026-09-16 | Reconciled against livespec 1.7.0 on 2026-09-16 |
| `check:stamp-range` | clear | 2026-09-16 | stamp 1.7.0 is the plugin installed — nothing between |
| `check:stamp-ahead` | clear | 2026-09-16 | stamp 1.7.0 is not ahead of 1.7.0 |
| `check:range-empty-said` | clear | 2026-09-16 | nothing between 1.7.0 and the plugin installed to reconcile |
| `check:changelog-reachable` | clear | 2026-09-16 | 41 entries, newest 1.7.0, at /home/sargis/Projects/livespec/CHANGELOG.md |
| `check:entry-moved-here` | n/a | 2026-09-16 | no entries between the stamp and the plugin installed |
| `check:row-state-legal` | clear | 2026-09-16 | 21 gate rows, 2 wiring rows, 4 boundary rows, every state legal |
| `check:row-evidence` | clear | 2026-09-16 | every row carries the evidence its state owes |
| `check:row-uncovered` | clear | 2026-09-16 | read: the automated rows cover specs/, evals/, the manifests and the release inputs, which is the whole tree — no manifest, no package, no second language; the four boundary rows are the four things the cases touch |
| `check:number-from-config` | n/a | 2026-09-16 | no coverage gate here |
| `check:demand-is-a-ratchet` | n/a | 2026-09-16 | no coverage gate here |
| `check:exclusions-in-config` | n/a | 2026-09-16 | no coverage gate here |
| `check:na-vs-tree` | clear | 2026-09-16 | 8 not-applicable row(s) read against the tree, none contradicted; decided rows left alone |
| `check:row-per-gate` | clear | 2026-09-16 | 19 of 19 ids have a row; 4 local: row(s) |
| `check:real-starts-here` | not-read | 2026-09-16 | boundary:model-session — `python3 evals/runner/run.py … --i-approve-the-cost` is the maintainer's to run and costs money. boundary:platform — run: `gh api repos/sargismarkosyan/livespec/rules/branches/main` → deletion, non_fast_forward, pull_request, required_status_checks apply to main |
| `check:real-not-doubled` | clear | 2026-09-16 | run: `python3 .github/scripts/trace.py` → green, 78 live rules; no rule-bound tests here — the cases are the tests, and gate:boundary-double reads not applicable for that reason |
| `check:fake-suite-green` | n/a | 2026-09-16 | no boundary row reads fake |
| `check:recorded-age` | n/a | 2026-09-16 | no boundary row reads recorded |
| `check:mocked-clock` | n/a | 2026-09-16 | no row reads mocked |
| `check:merge-blocked` | clear | 2026-09-16 | run: `gh api repos/sargismarkosyan/livespec/branches/main/protection` → 404 Branch not protected, the answer the bindings say to expect since the migration to a ruleset; run: `gh api repos/sargismarkosyan/livespec/rules/branches/main` → deletion, non_fast_forward, pull_request, required_status_checks apply to main; run: `gh api repos/sargismarkosyan/livespec/rulesets/21391215` → active; required_status_checks strict: repository checks, plugin validate; bypass_actors DeployKey:always — a merge is blocked when either check fails |
| `check:check-name` | clear | 2026-09-16 | run: `gh api repos/sargismarkosyan/livespec/rulesets/21391215` → active; required_status_checks strict: repository checks, plugin validate; bypass_actors DeployKey:always — the jobs' name: in checks.yml, as the bindings say |
| `check:who-bypasses` | clear | 2026-09-16 | run: `gh api repos/sargismarkosyan/livespec/rulesets/21391215` → active; required_status_checks strict: repository checks, plugin validate; bypass_actors DeployKey:always; run: `gh api repos/sargismarkosyan/livespec/keys` → one key, livespec release, read_only=false — the one entry the bindings record |
| `check:credentials-present` | clear | 2026-09-16 | read: L57 says manifest validation runs offline with no credential — a step needing none, not a claim that one is missing; nothing in the bindings claims a credential is absent |
| `check:read-back-or-not` | clear | 2026-09-16 | 8 judgment line(s) read back with their command, 1 not read with why |
| `check:prose-phrases` | clear | 2026-09-16 | none of the four phrases in the prose |
| `check:second-table` | clear | 2026-09-16 | present, 2 row(s) |
| `check:pr-report-row` | clear | 2026-09-16 | automated — [`report.py`](../../.github/scripts/report.py), posted by [` |
| `check:rule-bound-row` | clear | 2026-09-16 | not applicable — there is no coverage here at all, gated or otherwise — *What |
| `check:sketch-row` | clear | 2026-09-16 | *a sketch is owed*: by every change spec, before approval — there is no app here, and the |
| `check:picture-row` | clear | 2026-09-16 | *deliverable of a version*: the pull request description. No picture in any form — see *What does |
| `check:skill-names` | clear | 2026-09-16 | 5 skill name(s) in the record, all exist: doctor, record-clip, refine-spec, setup, todo |
| `check:word-not-a-skill` | clear | 2026-09-16 | read: CLAUDE.md:42 todo, :43 refine-spec, :66 todo, :66 record-clip — the loop naming skills that exist, left alone; nothing instructs by an old name |
| `check:loop-per-claude-md` | clear | 2026-09-16 | read: CLAUDE.md steps 1–8 against method/claude-md.md — step 5 names the test as a claim (0041), step 6 the ## Ids section (0042); each step says what the method now asks |
| `check:deferred-clock` | clear | 2026-09-16 | no row reads deferred |
| `check:hook-no-row` | clear | 2026-09-16 | no row in any table is a hook |
| `check:sorted-by-severity` | clear | 2026-09-16 | the reply lists what is open platform › boundary › wiring › record |
| `check:record-only` | clear | 2026-09-16 | nothing outside the record is changed in the working tree |
| `check:last-line-command` | n/a | 2026-09-16 | nothing is left for the sitting |
| `check:no-line-when-clear` | clear | 2026-09-16 | no line sends anybody to a sitting |

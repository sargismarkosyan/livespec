#!/usr/bin/env bash
# `kilnlog`, a firing log for a small pottery studio. Set up on livespec 0.31.0
# and correct as of it: every gate row accurate and read back from the platform,
# both never-gating rows present, the sketch row present, the stamp one version
# behind.
#
# The one thing wrong is in CLAUDE.md rather than in the bindings: step 2 of the
# loop sends every session to `/livespec:feedback`, a name that no longer reaches
# a skill. No gate here can fail over it and the file reads perfectly.
#
# The same word appears three more times and none of them is a reference to a
# skill: `docs/feedback/` as the screenshot home, the `from-feedback` label, and
# the rules line "feedback is never fixed on the spot". All three must survive.
set -euo pipefail

mkdir -p specs/setup specs/personas specs/workflows specs/journeys specs/changes \
         specs/features/firing .github/workflows docs/feedback docs/screenshots \
         src tests/rules tools

cat > CLAUDE.md <<'EOF'
# kilnlog

A firing log for one pottery studio. Every **firing** records the kiln, the
schedule it was run on, and the cone that actually bent. Python, `pytest`, one
`Makefile`. `make verify` runs everything. `specs/` is the contract: read
`specs/setup/README.md` before assuming any command.

## The loop

1. Human tests and reports.
2. AI files issues (`/livespec:feedback`). It does not fix.
3. AI writes the spec (`/livespec:refine-spec`) — Gherkin plus a numbered change
   spec, and draws the sketch the approval step is held against.
4. Human approves the spec and the sketch, or asks for changes.
5. AI implements, gets `make verify` green, commits.
6. AI records the clip (`/livespec:record-clip`) and opens the pull request.
7. Human merges.
8. AI closes the issue.

Setting the process up again anywhere is `/livespec:setup`.

## The rules worth having in front of you

- Spec before code. One change per version.
- **feedback is never fixed on the spot** — it gets tracked and specced.
- Never touch `src/` from a skill.
- Rule ids are permanent. Renaming one orphans every test pointing at it.
- Every commit green.

## Labels

`from-feedback` marks anything that came out of a human testing session.

## Commands

```sh
make verify
```
EOF

cat > specs/setup/README.md <<'EOF'
# Bindings

| | |
|---|---|
| **Verification** | `make verify` |
| **Traceability gate** | `python3 tools/trace.py`, run by `make verify` |
| **Coverage** | `pytest --cov`, the whole of `src/` once `src/importer/` is excluded |
| **Required check** | `verify` — the job name in `.github/workflows/checks.yml` |
| **Tracker** | GitHub Issues on `kilnlog/kilnlog`, via `gh` |
| **Screenshot home** | `docs/feedback/`, committed and pushed; deleted when the issue closes |
| **Pull-request report** | `tools/report.py`, posted by `.github/workflows/checks.yml` |
| **Deliverable** | A clip in `docs/screenshots/`, plus the Gherkin a change moved quoted in the pull request body |
| **Sketch before approval** | Every change spec is handed over with a page showing the before and after. Drawn from the spec, not recorded from the app |

## Gate wiring

Reconciled against livespec 0.31.0 on 2026-08-14.

| Gate | State | Wired by, or why not |
|---|---|---|
| rule → test | automated | `python3 tools/trace.py` |
| test → rule | automated | `python3 tools/trace.py` |
| feature → workflow | automated | `python3 tools/trace.py` |
| workflow → feature | automated | `python3 tools/trace.py` |
| workflow → test | automated | `python3 tools/trace.py` |
| workflow → persona | automated | `python3 tools/trace.py` |
| persona → workflow | automated | `python3 tools/trace.py` |
| journey → workflow | automated | `python3 tools/trace.py` |
| coverage — lines, branches | automated | `pytest --cov`, 100% of what remains, over `src/` with `src/importer/` excluded in `pyproject.toml` |
| both gates verified to fire | automated | `tools/inject.py`, run by `make verify` |
| required check on the default branch | automated | branch protection on `kilnlog/kilnlog` requires `verify`, and a merge is blocked when it fails. Read back with `gh api repos/kilnlog/kilnlog/rules/branches/main` on 2026-08-14 |

## The wiring that must never gate

| Wiring | State | Notes |
|---|---|---|
| pull-request report | automated | `tools/report.py`, `continue-on-error: true`. Watched arrive on 2026-08-14 |
| rule-bound measure | automated | `pytest --cov` over `tests/rules/` alone, reported beside the gated number, never compared to it |

## What has no gate

`src/importer/` reads the studio's old spreadsheet exports and is excluded in
`pyproject.toml`, where the coverage tool reads it rather than only here. It is
scheduled for deletion once the last studio has migrated.
EOF

cat > pyproject.toml <<'EOF'
[tool.coverage.run]
omit = ["src/importer/*"]

[tool.coverage.report]
fail_under = 100
EOF

cat > Makefile <<'EOF'
verify:
	python3 tools/trace.py
	python3 tools/inject.py
	pytest --cov --cov-fail-under=100
EOF

cat > specs/features/firing/cone.feature <<'EOF'
@feature:firing-cone @workflow:log-a-firing
Feature: What a firing records about the cone

  @rule:a-firing-records-the-cone-that-bent
  Rule: A firing is not complete until the cone that actually bent is recorded

    Example: the schedule finished and the cone is entered
      Given a firing run on a recorded schedule
      When the potter enters the cone that bent
      Then the firing is complete
EOF

cat > specs/workflows/log-a-firing.feature <<'EOF'
@workflow:log-a-firing @persona:studio-potter @journey:trusting-the-log
Feature: Logging a firing from lighting the kiln to reading the cone
EOF

printf '# studio-potter\n\nOne potter, one kiln, firing twice a week.\n' > specs/personas/studio-potter.md
printf '# trusting-the-log\n\nThe first month of writing every firing down.\n' > specs/journeys/trusting-the-log.md

printf 'def bent(cone, peak):\n    return peak >= cone\n' > src/predict.py
mkdir -p src/importer && printf 'def read_export(path):\n    raise NotImplementedError\n' > src/importer/legacy.py
printf 'from src.predict import bent\n\n\ndef test_cone_bends_at_peak():\n    """rule:a-firing-records-the-cone-that-bent"""\n    assert bent(6, 6)\n' > tests/rules/test_cone.py

printf '#!/usr/bin/env python3\n"""Traceability gate. Reads specs/features and tests/."""\n' > tools/trace.py
printf '#!/usr/bin/env python3\n"""Breaks each gate in turn and checks it fires."""\n' > tools/inject.py
printf '#!/usr/bin/env python3\n"""Posts what the change did to the spec layer, as a pull request comment."""\n' > tools/report.py
printf 'Screenshots attached to open issues live here.\n' > docs/feedback/.gitkeep
printf 'Clips a version ships with live here.\n' > docs/screenshots/.gitkeep

git init -q -b main
git add -A
git -c user.email=wren@kilnlog.example -c user.name="Kilnlog" \
    commit -q -m "record the cone that bent"
git remote add origin git@github.com:kilnlog/kilnlog.git

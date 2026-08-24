# Changelog

The `version` in `.claude-plugin/plugin.json` **pins** every install. Push
without bumping it and nobody receives the change — `/plugin update` sees the
same string and keeps the cached copy. So: one entry here per version, and the
bump lands in the same commit as the change it describes.

## 0.4.0 — 2026-08-24

- `setup` is now **user-invoked only** (`disable-model-invocation: true`). Claude
  can no longer start it on its own — the description is out of context entirely,
  and it runs when someone types `/livespec:setup`. It writes `CLAUDE.md` and
  wires a repository's gates, which is not a decision an agent makes because a
  repo looked ready for it.
- The always-on cost drops with it: ~3.2 KB across six model-invocable skills,
  down from ~3.7 KB across seven.
- CI fails if the flag goes missing.

## 0.3.0 — 2026-08-24

**Maintenance.** Nothing about the method changed; three skills now name the
template they were already asking for.

- `refine-journeys`, `refine-workflows` and `refine-personas` name their
  templates (`journey.md`, `workflow.feature`, `persona.md`). All three shipped
  with the plugin and were referenced by nothing, so nobody read them.
- `method/README.md` said "six skills". There are seven.
- Added `repository`, `homepage`, `license` and `keywords` to `plugin.json`, and
  a `LICENSE` (MIT).
- Added `evals/` — seven cases holding the judgment the skills exist for, five
  fire and two should-not-fire. Written, not yet piloted.
- Added `CONTRIBUTING.md`, `.github/scripts/checks.py` and CI. The checks catch
  exactly the two drifts above, and are proven against injected faults.

## 0.2.0 — 2026-08-24

- Added `setup` — installs the process into a repository, wires both gates in
  that project's own language, proves each fires, and writes `CLAUDE.md`.
- Added `method/claude-md.md`: what a repository's `CLAUDE.md` must contain.

## 0.1.0 — 2026-08-24

- First release. The method, six skills, four templates.

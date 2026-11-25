# Spec 2026-11-24: the repository's own skills

- **Status:** approved, by the maintainer, 2026-11-24 ("approved")
- **Issue:** [#251 check:skill-names calls a repository's own Pi skill (/skill:<name>) 'no such skill'](https://github.com/sargismarkosyan/livespec/issues/251)
- **Sketch:** not drawn — one function reads two more folders; nothing the prose cannot carry

## Who this is for

**[`agent-accelerated-owner`](../personas/agent-accelerated-owner.md), in [`adopt-the-process`](../workflows/adopt-the-process.feature)**, at the audit: reading what `check:skill-names` reports about the instructions in their own record.

## The job behind the request

When the audit says the record is wrong, it is wrong. A line that is correct does not keep showing up on every audit.

## Why now

helios/wf-developer-agents runs livespec under Pi. Its `AGENTS.md` (lines 42 and 97) and its bindings (`specs/setup/README.md:32`) tell a session to type `/skill:triage-feedback`, the repository's own skill at `.agents/skills/triage-feedback/SKILL.md`. The audits of 2026-11-23 reported all three as *no such skill*, and `check:skill-names` has stayed open in that repository's `specs/setup/audit.md` since. Under Pi, `/skill:<name>` is how *every* skill is typed, so the line is right. `c_skill_names` compares the name against livespec's skills only. The repository can close it only by rewording a correct instruction, and a check that stays open on a correct line teaches the owner to skip the check.

## The end value

An instruction to type the repository's own Pi skill reads clear; one naming a skill that exists nowhere is still reported.

**How we would know it worked:** the next audit of helios/wf-developer-agents reads `check:skill-names` clear, with `triage-feedback` among the skills named.

## What changes

1. **`doctor.py`, `check:skill-names`**: for the `/skill:` form only, a name is known when the repository has a `SKILL.md` for it under `.agents/skills/` or `.pi/skills/` (the two project folders Pi loads skills from, searched at any depth, as Pi does). The name is the `SKILL.md`'s frontmatter `name`, or its folder's name when there is none. `/livespec:<name>` still means livespec's skills alone.
2. **A former livespec name the repository has a skill for is not stale under `/skill:`.** If the repository keeps its own `feedback` skill, `/skill:feedback` reaches it under Pi, so no *now /skill:todo* is offered. `/livespec:feedback` still gets the hint. (The issue suggested keeping the hint either way; that would leave the same false open for any repository that reuses an old name.)

**Rules added or changed**:

| Rule id | Feature file | New or changed |
|---|---|---|
| `an-instruction-in-either-hosts-form-is-read` | [`wiring/the-host.feature`](../features/wiring/the-host.feature) | changed — reworded to count the repository's own skills under `/skill:`, and two Examples: the repository's skill in Pi's form, and the same name under `/livespec:` |

## What this removes

Nothing. The comparison gains one set of names; no rule, test or code goes dead.

## What we are not doing

- **Skills from Pi packages and `.pi/settings.json` `skills` paths.** An `npm:` or `git:` package cannot be read offline, and no adopter has a local one yet. A name only a package provides is still reported, and the next report says so if it comes up.
- **A bare root `skills/`.** Pi loads it only when settings declare the repository as a package, which is the case above. The issue listed it; counting it would clear a name Pi does not load.
- **User-level skills** (`~/.pi/agent/skills/`, `~/.agents/skills/`). They belong to one machine, and the audit reads the repository.
- **Claude Code's `.claude/skills/`.** Claude Code types a project skill `/<name>`, which this check does not read.

## Ids

unchanged — `check:skill-names` keeps its meaning (every skill the record instructs by exists); it now finds the ones the repository keeps for itself, and asks nothing new of a repository's files.

## Risks

A repository with a stray `SKILL.md` under those folders that Pi does not actually load would read clear for its name. Pi loads every `SKILL.md` under them, so the case is narrow.

## Acceptance checks

1. Run the audit against helios/wf-developer-agents with this branch's `tools/doctor.py`: `check:skill-names` reads clear, naming `triage-feedback`.
2. Add `/skill:nonesuch` to that repository's `AGENTS.md` in a scratch copy: it is reported *no such skill*.

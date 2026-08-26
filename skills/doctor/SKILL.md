---
name: doctor
description: Re-audit the gate wiring in a repository that already has this process — check every claim its bindings make against what owns the answer, reading branch protection and required checks back from the platform rather than from CI config, and print what is still open. Use when asked to check or audit the gates, to say whether the process still holds here, when a bindings claim looks like nobody verified it, or when a ledger row has been deferred too long. Corrects the record, never the wiring — building what is missing is setup.
---

# Audit what the wiring here actually claims

A gate wiring ledger is typed by a person, once, usually at the end of a long
sitting. Then it is trusted forever. This skill is the second reading.

**It changes the record and never the wiring.** A row that overstates gets
corrected; a gap gets a row. Building what is missing is
[`setup`](../setup/SKILL.md), which already offers exactly that, and a skill that
both audits the gates and builds them has no way to be wrong out loud.

## 0. Read the bindings, or stop

`specs/setup/README.md` is the subject of this whole skill. Read it first, along
with [`gates.md`](../../method/gates.md) — **the checklist is that page, not this
one.** Do not restate it here or work from memory of it: a second copy of that
list is the drift this plugin exists to stop, and the page ships to every
repository that has the plugin.

If there are no bindings, this repository has never had the process set up.
**Say that in one line and stop** — do not audit a ledger that does not exist,
and do not go looking through the tree for one somebody might have put elsewhere.
`setup` is what that repository needs, and offering it is the whole reply.

## 1. Take the ledger apart, row by row

For each row, three questions — and the second is the one nobody asks:

- **What state does it claim?** *automated*, *not applicable*, *deferred*,
  *unobserved*.
- **How was that established, and when?** A row is evidence or it is a memory.
  Where the answer is *somebody typed it during setup*, say so.
- **What does it not cover?** A gate wired over one language of two, one package
  of five, one directory of a monorepo, is not a gate over this repository. If
  the row does not say which part has no gate, it is being read as though it
  covered everything.

Then the cross-check `gates.md` already asks for: **the tree is the authority on
what applies.** A row reading *not applicable — no personas exist* in a
repository that has personas is contradicted by the tree, and the tree wins.

## 2. Read back what is not in the tree

This is the half a diff cannot review and the half that goes wrong.

Branch protection, whether a named check is actually **required**, whether the
credential a step needs exists — none of it is in the repository, so none of it
can be inferred from the repository. **A check named in a CI config is evidence
that somebody wrote it down and no evidence that a merge is blocked when it
fails.** On more than one platform those are separate settings, in separate
places, and one of them is a project-wide switch that nobody looking at the
pipeline file would ever see.

So go and read them, with the command the bindings name:

- **is a merge actually blocked** when the required check fails — not whether a
  job runs;
- **the check's name as the platform has it**, which is the job's name and not
  the workflow's filename;
- **who can bypass**, including the tokens and keys a pipeline uses;
- **the credentials a step claims are missing** — they are often present and
  inherited from a level above the repository, which is exactly where somebody
  reading the repository would not find them.

Report each as **read back** with what was run, or as **not read**, with why. A
row that was checked and a row that was assumed must not come out of this looking
the same, because looking the same is how they got here.

**Where the platform cannot be reached from this session, say so once.** No
credentials, no network, no permission — all fine, and all different from having
looked. Name what would read it, put that in the row, and move on rather than
spending the session hunting for another way in; that is
[the same rule](../../method/process.md#a-step-you-cannot-take-here-is-said-once-not-searched-for)
every other skill here follows.

## 3. Find the gaps that were never rows

A gap written as a sentence is on no clock. Nobody re-reads it, nothing counts
its age, and it survives every audit that only looks at the table.

So read the prose too, and pull out anything that says *not built yet*, *to do*,
*we should*, *for now*. Each one is either a row or it is nothing.

**Two of them are structural**, and they are the two most often missing —
[the wiring that must never gate](../../method/gates.md#the-wiring-that-must-never-gate):
the pull-request report, and the rule-bound measure reported beside the gated
coverage number. Neither can fail a build, so neither ever announces its own
absence. Check the second table exists and holds both; where the bindings predate
it, that is the offer to make.

Then the clock: **a row deferred across two changes is either wired or written
off.** Read how long each deferral has been sitting there, and say which ones are
past it. Written off means the row becomes *not applicable* with the reason in
it — one decision in the open, rather than an apology repeated forever.

## 4. Say what is open, concretely

Not a health score, and not a restatement of the table. A list somebody can act
on, each item saying **what is claimed, what is actually true, and what closes
it**. An audit that ends in *mostly fine* has cost a session and moved nothing.

Sort it by what is dangerous rather than by what is untidy: a row asserting a
protection the platform does not enforce outranks a deferral that is one change
old, every time.

Then make the corrections you found — **to the record only.** Show the rows as
they will read, then write them. Where the wiring itself is missing, that is the
last line of the report and it names `setup`, which does the building.

**Re-stamp the version the ledger was reconciled against only if the wiring
actually moved.** A ledger re-stamped for an audit that changed nothing has
learned to lie, and it is worse than the stale one it replaced because it now
looks fresh.

## What this skill refuses

- **Wiring anything.** Not a gate, not a report, not a coverage split. It writes
  the record of what is wired; `setup` writes the wiring.
- **Writing application code**, which no skill here does.
- **Running the interviews.** A repository whose layers are empty has a different
  problem, and `setup` section 8 is where that gets fixed.
- **Flipping every row to *unobserved* to be safe.** That is not honesty, it is a
  second inaccurate ledger. A row somebody watched fire stays *automated*.
- **Reading a green pipeline as an answer about the platform.** A build that
  passed says the job ran. It says nothing about what happens to a build that
  fails, which is the only question branch protection answers.
- **Auditing a repository that has no bindings**, rather than saying so and
  offering `setup`.

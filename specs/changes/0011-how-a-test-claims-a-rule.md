# Spec 0011: how a test claims a rule

- **Status:** approved
- **Issue:** [#5](https://github.com/sargismarkosyan/livespec/issues/5) findings
  3 and 4, and [#13](https://github.com/sargismarkosyan/livespec/issues/13) in
  full, taken together at the human's direction.

## Who this is for

[`@persona:agent-accelerated-owner`](../personas/agent-accelerated-owner.md), in
[`adopt-the-process`](../workflows/adopt-the-process.feature), at the point
[`setup`](../../skills/setup/SKILL.md) section 2 asks the things it cannot find
out. There are four. This adds the fifth, and it is arguably the one both gates
rest on: **what counts as a behaviour test here, and how does it name the rule it
exists for?**

The persona's second recorded behaviour is the reason this is a defect rather
than a nicety: *"When the tool does not fit the repository, the hand-built local
version stays."* And their fourth: *"A setup they did not agree to gets stopped
and questioned rather than inherited."* [#5](https://github.com/sargismarkosyan/livespec/issues/5)
is that sentence happening — *"check the setup with the user first — especially
for plugin evals this is not good practice."*

The always-promise most at risk is **`context-budget`**. Section 2 grows from
four questions to five, and `setup` already carries the longest description in
the plugin; the body grows too, and every imperative added to a skill body is
paid on every fire. See *Risks*.

## The job behind the request

Not have the process decide, on its own and without saying so, how this
repository proves a rule is true — and not hand-roll something the tooling
already provides.

Two halves of one job. The first is about **consent**: this is a decision with
consequences for every change afterwards, and it was being made silently. The
second is about **invention**: the answer that got made up here has a maintained
alternative, and nobody looked.

## Why now

**Because the invented answer already cost something.** The mapping *an eval case
is what claims a Gherkin rule* was livespec's own, and
[#4](https://github.com/sargismarkosyan/livespec/issues/4) is what it produced —
a nine-name `GRANDFATHERED` list hardcoded inside a gate, described by the person
who found it as *"WTF is this?"*. That list was deleted, and the reason it
existed was that a mapping arrived without anybody deciding it applied.

**Because `method/testing.md` is written as though every repository has an app.**
It opens with `tests/behaviour/`, `tests/unit/`, and a `rule()` helper wrapping
calls to functions. That is false for the repository that ships it — livespec has
no application code, invented a substitution for itself, and wrote it down only
in its own bindings, where nothing about it reaches anybody else.

**Because `setup` currently says nothing at all.** `grep -n -i "eval"
skills/setup/SKILL.md` returns nothing. It asks about the verification command
and the coverage thresholds, and never about the thing those numbers are
measuring.

**And because `claude plugin eval init` exists.** It writes a suite, interviewing
by default, with `--bare` for a blank template. Livespec hand-rolled case folders
next to a tool that produces them.

## The end value

After the sitting, the bindings say what a behaviour test is in that repository
and how it names its rule — **because the person was asked**, and because the
answer was recommended from what the repository already had rather than from what
this method happens to use.

A repository with an ordinary test suite gets the helper that makes a rule id
checkable where the test is written, instead of a rule name typed into a string
that nothing verifies. A repository whose product is prose gets pointed at the
tool that builds such a suite, instead of watching an agent invent a folder
format.

**How we would know it worked:** the sharp version is negative. Set the process
up in a repository with no application code and one with a running test suite,
and the two bindings files should not say the same thing. Today they would —
because nothing asks, so nothing can differ.

## What changes

1. **Section 2 gains a fifth question.** *What proves a rule is true here, and
   how does a test say which rule it is answering?* With the same discipline the
   other four have: recommend what the repository already has, and never
   introduce a second way of testing alongside one that works.

2. **`method/testing.md` stops assuming an app.** It documents both answers as
   answers rather than one as the shape of the world:
   - **an ordinary test suite** with a `rule()` binding — what the file already
     describes, unchanged;
   - **graded cases**, for a repository whose product is judgment rather than
     code, with its costs stated plainly: a graded case is slow, costs money per
     run, and proves that judgment held on a prompt rather than that a function
     is correct. **That is a weaker claim and the file has to say so**, because
     the repository that invented this substitution is the one writing it down.

3. **`setup` scaffolds the binding**, whichever answer came back —
   [#13](https://github.com/sargismarkosyan/livespec/issues/13)'s first half. A
   rule id typed into a `describe("... Rule 17.5 ...")` string is unchecked: it
   drifts, it can name a rule that does not exist, and it cannot be renamed from
   the spec. The helper makes the id fail at the point the test is written, which
   is where a typo is cheapest.

4. **`setup` points at `claude plugin eval init`** where the answer is graded
   cases, rather than describing a folder layout for an agent to reproduce.

5. **The spec-bound measure is wired, and reported rather than gated** —
   [#13](https://github.com/sargismarkosyan/livespec/issues/13)'s second half.
   Coverage taken twice: once over everything (the gated number) and once over
   the rule-bound tests alone. The second says how much of the product the
   *specification* actually reaches, which is invisible unless the split exists,
   and it goes in the report that landed in 0.12.0 rather than into a threshold.

**Rules added or changed** — the `@rule:` ids in `specs/features/`:

| Rule id | Feature file | New or changed |
|---|---|---|
| `setup-asks-how-a-test-claims-a-rule` | `features/setup/test-binding.feature` | new |
| `setup-scaffolds-the-rule-binding` | `features/setup/test-binding.feature` | new |
| `the-spec-bound-measure-is-reported-never-gated` | `features/setup/test-binding.feature` | new |

**Ledger:** nothing moves. No new gate — item 5 is explicitly a report, and
`gates.md` already holds the line that a report cannot fail a build.

## What we are not doing

- **Not replacing `evals/` with `claude plugin eval init` output here.** This
  repository's suite exists, its cases are held by two gates, and rewriting them
  to match a generator's layout would be churn with no reader. What changes is
  what `setup` tells *somebody else* to do.
- **Not making graded cases the recommended answer.** They are the answer for a
  repository with no code to call. Recommending them anywhere else would repeat
  the mistake this change exists to correct, one level up.
- **Not gating the spec-bound number.** It is a measurement of how much of the
  product the specification reaches — a number that should move a conversation,
  not a build. Gating it would push people to write rules for coverage rather
  than for promises, which is the failure `method/gates.md` already names about
  coverage on its own.
- **Not writing rules for livespec's own eval substitution.** It is recorded in
  this repository's bindings and now argued in this spec, which is what
  [#5](https://github.com/sargismarkosyan/livespec/issues/5) asked for. A rule
  would be a promise to somebody else about a choice this repository made for
  itself.
- **Not touching the `evals/` floor.** Three should-not-fire cases, `runs: 3`,
  an outcome grader each — none of it moves.

## Data

None. There is no storage contract — the plugin ships prose, and what a version
leaves behind is listed in [spec.md](../spec.md#what-a-version-leaves-behind).

## Risks

- **This is the largest single change to `setup` yet, and `setup` is the skill
  that can write files unprompted.** A fifth question, a scaffolding step, a
  generator to call and a second coverage pass to wire — all inside a sitting
  that [`0006`](0006-adopt-the-process.md) already warned must not grow. The
  workflows README requires naming what it shortens: **it shortens every change
  afterwards in that repository**, because a rule id that fails where the test is
  written is a class of drift that stops happening. That is the right trade and
  it is the second time this sitting has been lengthened for it.
- **`context-budget` moves in the wrong direction here**, and unlike
  [`0009`](0009-whose-repository-whose-tracker.md) there is no claim to delete to
  pay for it. The description need not change; the body will grow. Body characters
  load only when the skill fires, but
  [#15](https://github.com/sargismarkosyan/livespec/issues/15) is about exactly
  that growth and this change makes it worse rather than better.
- **The method blesses a mapping with one user.** Graded cases claiming Gherkin
  rules has been done in exactly one repository, by the person writing the
  method. Item 2 mitigates by stating the weaker claim out loud rather than
  presenting the two answers as equals — but a reader who wants permission will
  find it, and *"livespec does it"* is not evidence.
- **`claude plugin eval init` has never been run here.** `claude plugin eval` is
  gated behind early access on this account, so `setup` will be pointing at a
  command this repository cannot execute. What is known is that it exists and
  what its flags are; what is not known is what it produces. **The wording has to
  survive being wrong about the output**, which means pointing at the tool rather
  than describing its results.
- **The spec-bound number can be gamed by moving a test.** Reclassify a
  rule-bound test as a unit test and the gated total is unchanged while the
  spec-bound figure falls — or the reverse. It is a report, so nothing breaks;
  but it is a number somebody may start managing.

## Acceptance checks

1. Run a setup sitting in a repository with an existing test suite. The fifth
   question is asked, the recommendation is what that repository already runs,
   and the bindings name the helper and where it lives.
2. Run one in a repository with no application code. The same question is asked
   and the answer differs. **Read the two bindings files side by side — if they
   say the same thing, nothing was asked.**
3. In the first repository, write a behaviour test naming a rule id that does not
   exist. It fails where the test is written, not later in the gate.
4. Confirm the spec-bound coverage number appears in the report and in no
   threshold. Lower it deliberately; the build stays green.
5. Read `method/testing.md` once looking only for the sentence that says a graded
   case proves something weaker than an ordinary test. If it is not there, item 2
   was written as a menu rather than as a decision.
6. Read section 2's five questions aloud. If the fifth needs the other four
   explained first, it is in the wrong place.

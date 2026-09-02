# Spec 0035: what the whole of it comes to

- **Status:** proposed
- **Issue:** [#88](https://github.com/sargismarkosyan/livespec/issues/88)
- **Depends on:** nothing. It finishes one sentence
  [`0030`](0030-covered-or-named.md) left as a description, and argues against
  one line in that spec's *What we are not doing*.
- **Sibling, deliberately not folded in:**
  [#89](https://github.com/sargismarkosyan/livespec/issues/89) — that `0030`
  reached no repository already set up. True whatever this spec decides.

## Who this is for

[`agent-accelerated-owner`](../personas/agent-accelerated-owner.md), in
[`adopt-the-process`](../workflows/adopt-the-process.feature) — §2 of the
sitting, the coverage question, the same round `0030` changed.

Three lines of that persona decide this one, and the third decides it against
the way it was asked for:

- **"They read the spec layer and not the documentation."** What this person
  reads is prose in `specs/`. A demand that only ever appears as a number inside
  somebody's `vitest.config.ts` is in the half of the repository they have said
  they do not read.
- **"A setup they did not agree to gets stopped and questioned rather than
  inherited."** A recommendation with no figure in it cannot be disagreed with.
  There is nothing to push back on until it has already become a number in a
  config file, at which point it is inherited.
- **"A failing pipeline gets fixed. It does not get bypassed"** — and
  *"bypass a failing gate to get a change through"* is on the persona's
  never-list. This is the line that decides the mechanism, below.

**This does not lengthen the attempt.** The [workflows
README](../workflows/README.md) requires a change adding a step to adoption to
name the later attempt it shortens. This adds no step: the question is already
asked, in the same round, in the same breath. What changes is the sentence the
recommendation is made in.

## The job behind the request

To find out whether the tests reach the code, without reading either.

That is the whole job, and it is unusual only because of who wrote both. The
code was written by an agent, the tests that check it were written by the same
agent, and the person accountable for the result has read neither and has said
so in as many words: *"I have not read it. It only for AI."* Every other reader
of a coverage number is checking somebody else's work. This one is checking a
machine's work against a machine's account of it.

## Why now

Because the request has now been made twice, in the same words, by the same
person, and the second time was after it was closed as done.

[#79](https://github.com/sargismarkosyan/livespec/issues/79) — *"Make the code
coverage demand to be 100% instead of 95%"* — closed via `0030`. `0030`
replaced the number with a shape: *"the demand over what remains is the whole of
it."* That is the same demand, correctly reasoned, and it is not the same
sentence. The asker read the result and asked again.

The method never says the number, anywhere:

```console
$ grep -rn "100" method/ skills/ --include="*.md" | grep -i "coverage\|threshold\|demand"
method/gates.md:137:function can show 100% lines while function coverage correctly reports 50%
method/gates.md:142:moment the first module lands. A coverage gate that reports 100% of zero files is
```

Line 137 is an aside about how V8 counts a function declaration. Line 142 is the
false-green warning. Neither is a recommendation, and there is no third hit.

What it costs: an adopter who wants to know what livespec asks of coverage has
to convert *"the whole of what is in scope"* into a figure themselves, in a
sitting where the alternative — a number read off today's report — arrives
already converted. `0030` removed the wrong answer and left the right one
needing a translation step, at exactly the moment the wrong one is easiest.

## The end value

The coverage question ends with a number the adopter can accept or argue with,
in the transcript, in the round where it is decided — instead of a description
they have to turn into one privately and later.

**How we would know it worked:** a sitting's coverage round contains a figure.
Slower and more telling: an adopter who ends up below it has to say what the
missing points stand for, because there is now a stated figure for their number
to be lower *than*. Today a lower number is not visibly lower than anything.

## Why the figure may live in the portable half

`0030` considered this and dropped it, and the reason has to be answered rather
than stepped around:

> **Naming 100 in `method/`.** A percentage is a threshold and a threshold is a
> binding — [`spec.md`](../spec.md)'s vocabulary says so in one line.

That is right about 95 and wrong about 100, and the vocabulary says why. A
**binding** is *"the part that is one repository's own — its commands,
thresholds and paths."* The test in [`specs/README.md`](../README.md) is whether
a sentence could survive a repository with pytest and a Makefile.

95 is one repository's own: it was tuned, it could have been 90, and it means
nothing anywhere else. **100 is not tuned and is the same figure everywhere** —
it is the absence of a threshold written as a number, which is exactly what
`0030` argued the demand should be. It survives pytest and a Makefile unchanged.

The precedent is already in the tree. `skills/refine-spec/SKILL.md:144` carries
*"soft limits (120 lines, 6 rules)"* — portable figures, in the portable half,
holding in every consuming repository at once. A figure that is the same
everywhere has never been a binding here.

**And the threshold stays the adopter's.** What goes in the portable half is
what the sitting *recommends*; what lands in `vitest.config.ts` is still written
by the adopter, and [`gates.md`](../../method/gates.md)'s *"all three, and the
number is the repo's"* stays true word for word. A recommendation is not a
threshold — conflating the two is what left `0030` unable to say its own number.

## What changes

- **§2's coverage recommendation names the figure.** `skills/setup/SKILL.md:88-96`
  already asks what is in scope and what is excluded. It gains the number the
  answer comes to — 100% of what remains — said in the round, so the adopter has
  something to accept or refuse.
- **The figure is stated as 100% *of what is left*, never of the repository.**
  This is the misreading that would make the recommendation impossible and get
  it dismissed on the spot, and it is the second example in the rule.
- **`method/testing.md` gains the reason, and no number.** Its *Coverage* list
  runs under *"The thresholds are the repository's. The judgment is not."* The
  judgment it gains: where an agent wrote the code and the tests that check it,
  coverage is the only mechanical evidence that the tests reach the code at all
  — and traceability is what stops that evidence being satisfied by tests that
  reach it without asserting anything. Neither half is worth much alone, which
  is [`README.md`](../../README.md)'s existing argument, arriving where somebody
  deciding a threshold will read it.

**Rules added or changed** — the `@rule:` ids in `specs/features/`:

| Rule id | Feature file | New or changed | Ships |
|---|---|---|---|
| `the-demand-is-recommended-as-a-figure` | `features/setup/coverage-binding.feature` | new | `@planned` |

Added to `coverage-binding` rather than a new file: it is the same question in
the same round as the two rules already there, and the file goes to three rules
and 51 lines against soft limits of six and 120.

## What we are not doing

- **Making the coverage gate stop failing the build.** This is the half of
  [#88](https://github.com/sargismarkosyan/livespec/issues/88) that was asked
  for explicitly — *"not fail if it's not but strongly recommend"* — and it is
  dropped, for three reasons that all point the same way.

  The **persona** rules it out: this reader does not bypass a failing gate, they
  fix it, and what they read is the spec layer rather than what a gate prints.
  A demand that cannot fail is one they would have to remember to go and look
  at, in the half of the repository they have said they do not read.

  The **stated reason for wanting it** argues against it. If coverage is the
  only mechanical check on work no human reads, then a demand the agent can
  decline to meet is a demand graded by the party being graded —
  [`gates.md`](../../method/gates.md)'s *"a gate that has never failed is not
  known to be a gate"*.

  And the **fear behind it is already answered.** "Don't fail" is asked for
  because 100% sounds like a red build on day one. Under `0030` it is not: the
  day-one exclusion list is exactly today's uncovered code written down, so the
  demand is whole *and* green on the first run. That was `0030`'s central
  argument and it is the thing this spec makes legible by putting a number on
  it. Nothing needs to stop failing.

  If it is still wanted after that, it is a change to what a gate is and belongs
  in its own spec, argued against `README.md`'s claim that the two gates are
  hard to satisfy dishonestly *together*.
- **Naming 100 in `method/gates.md`.** Gate 2's *"the number is the repo's"* is
  about what lands in the adopter's config, and that is still true. The figure
  belongs to the recommendation, not to the gate.
- **A ratchet mechanism.** `0030` ruled this out and nothing here reopens it.
  The demand is the whole of the scope; there is nothing left to ratchet.
- **Reaching repositories already set up.** That is
  [#89](https://github.com/sargismarkosyan/livespec/issues/89), it is a
  different mechanism in a different skill, and it is true whichever way this
  one goes.
- **Gating the exclusion list.** Unchanged from `0030`: nothing can check that a
  stated reason is a true one.
- **The spec-bound measure.** Reported, never gated. Settled, and untouched.

## Data

No storage contract moves; there is none here. Nothing goes stale on the spec
commit: one `@planned` rule claimed by nobody, plus this file.

**The implementing commit re-measures the `skill:setup` cases**, because
`measurement_inputs` hashes the body of every skill a case holds and this change
edits `skills/setup/SKILL.md`. `0030` paid the same bill for the same reason and
its table is the estimate to read; the cases are unchanged since. That run is
the maintainer's to approve — `verify.py` exits **2** for it rather than **1**,
so it does not read as a defect.

## Risks

- **`always-green` is not touched.** Nothing here makes a user's build depend on
  something an agent session installed; the recommendation is words in a sitting
  and the threshold is still written by the adopter.
- **The figure gets read as 100% of the repository**, which is impossible in any
  occupied repository and would get the whole recommendation dismissed in the
  round it is made. This is the risk the change actually carries. It is held by
  the rule's second example, and it is why the exclusions half of `0030` has to
  be said in the same breath rather than a paragraph later.
- **An adopter reads a portable figure as permission to skip the scope
  question** — taking 100% as the answer without ever deciding what it is 100%
  *of*. The existing two rules are what stand against that, and they run first.

## Acceptance checks

There is no app; this is the reading pass.

1. Run a sitting against a repository with an existing suite and an untested
   legacy directory. The coverage round names a figure, and it is 100% of what
   remains after the exclusion is named — not 100% of the tree, and not the
   score.
2. Push back in that sitting with *"that will be red on day one"*. The answer is
   the exclusion list, not a lower number, and the figure does not move.
3. Read `method/testing.md`'s *Coverage* list. It carries the reason and no
   number, and every sentence in it still survives a repository with pytest and
   a Makefile.
4. `grep -rnE "[0-9]+ ?%" method/` returns only the two asides at
   `gates.md:137` and `gates.md:142`.

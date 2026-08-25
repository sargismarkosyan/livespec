# Spec 0014: the reader the method assumes

- **Status:** approved
- **Issue:** [#26](https://github.com/sargismarkosyan/livespec/issues/26)

## Who this is for

[`@persona:agent-accelerated-owner`](../personas/agent-accelerated-owner.md) —
and unusually, this change is about a sentence that describes them wrongly.
One line of that file decides it:

> **They read the spec layer and not the documentation.** Workflows, journeys and
> personas above all. READMEs, docs and comments are for the agent.

**It serves no workflow, and that is correct rather than a gap.**
[process.md](../../method/process.md#a-technical-change-that-serves-no-workflow-is-correct-not-a-gap)
documents the case. Nothing observable in
[`adopt-the-process`](../workflows/adopt-the-process.feature) moves: the sitting
writes a CLAUDE.md at the root before this change and after it, to the same ten
requirements and the same length. What changes is the reason the method gives for
doing so, which is why this carries no rule — see *What changes*.

The always-promise most at risk is **`context-budget`**
([spec.md](../spec.md#the-promises-that-belong-to-no-single-workflow)) — *every
session pays for what is always loaded.* The claim being withdrawn is one of two
things currently holding up the length rule. Pulling it without checking what is
left standing is how a budget quietly loses its basis, and the answer is in
*Risks*.

## The job behind the request

Have the method's stated reasons be ones it can stand behind, so that the next
person arguing about this file argues from something true.

A justification is not decoration. It is the thing every later argument leans
on: *where does this file go*, *how long may it be*, *what form does it take*
are all settled today by one clause — **being findable by a human is most of why
the file is written in prose rather than configuration**
([claude-md.md](../../method/claude-md.md), *Where it goes*). A reader who is not
there cannot settle anything, and the arguments resting on them inherit the
error rather than reporting it.

## Why now

**Because the evidence was promoted and the claim was not.** When
[#26](https://github.com/sargismarkosyan/livespec/issues/26) was filed the
contradiction was a line in an interview transcript. It is now a line in the
persona layer — the layer this repository gates against — plus the quote
verbatim under *In their words*:

> I have not read it. It only for AI.

So this is no longer transcript against method. It is **payload contradicting
payload**: two files that ship to every user, disagreeing about who reads the
most-loaded file in a consuming repository.

[`0005`](0005-the-first-persona.md) parked it deliberately — *"That is a live
method page contradicted by evidence; it is recorded here and belongs in its own
issue, not in a persona change"* — and nothing has picked it up in nine
versions.

**And because the replacement argument is already written**, one screen above the
sentence that needs it. `claude-md.md` opens with *"noise is expensive here — it
is in front of every request, forever"*, and its length test is already framed
for an agent: *"if an agent read only this file and the bindings, could it make a
correct first change?"* The page is already reasoning from the agent in two
places out of three. The human-reader clause is the outlier, not the keystone,
and that is what makes this small.

## The end value

The method stops arguing from a reader the only evidence says is absent, and says
instead what it can defend: the agent is the reader you can count on, the human
is occasional, and where a repository has a spec layer that is what a person
opens. Root placement survives on the argument that never needed the human —
every other repository keeps it there.

**How we would know it worked:** the next change that wants CLAUDE.md longer has
to argue against per-request context cost, which is a real number and a real
constraint. Today it could argue against human attention span — an argument
nobody in this repository can settle, because the one human observed is not
reading the file.

## What changes

- **The *Where it goes* section stops resting on a human reader.** Root placement
  keeps the convention argument, which is untouched and was always the stronger
  half. The clause claiming human findability is *most* of why the file is prose
  is withdrawn and replaced with the reason that survives: what the file carries
  is judgment an agent applies, and judgment is not a setting.
- **The human reader is described as occasional rather than absent**, and where
  they go instead is named — the spec layer, because it is the part that says who
  the work is for. This is the *defend it explicitly* option the issue offered,
  narrowed to what was observed rather than dropped entirely.
- **The length rule is pointed at the argument that actually holds it up** —
  per-request context cost, already stated in the page's opening — so the number
  keeps a basis after the attention-span reading is withdrawn.

**Nothing else in the page moves.** The ten requirements, *What must stay out*,
the hundred-line budget, the `--strict` paragraph and the reference
implementation are all unchanged, and no threshold moves in either direction.

**Rules added or changed** — the `@rule:` ids in `specs/features/`:

**None.** No behaviour a persona could notice changes, and a rule asserting that
a justification is true is not a promise the product makes — it is an opinion
about prose, which
[the feature template](../../templates/feature.feature) rules out in as many
words. `verify.py`, `checks.py`, `release.py` and the report carry no rules
either, and [`0010`](0010-the-report-the-method-describes.md) recorded that as
the honest answer every time. Inventing one here to make the change look larger
is the *one bad tag* failure `process.md` names.

## What we are not doing

- **Not moving `CLAUDE.md`, and not claiming it is unnecessary.** The issue rules
  both out itself. It is loaded into every session by the harness and that is
  reason enough for it to exist; only the stated *why* is wrong.
- **Not changing the length rule's number.** *One screen of scroll, and about a
  hundred lines* stands. The issue observed that the budget wants a context-cost
  argument rather than an attention one — and that argument is already in the
  page's own opening paragraph, so what this change owes is a pointer, not a new
  threshold. Re-deriving a hundred lines from token cost is a different change
  with a different kind of evidence behind it, and it should be argued on its
  own if anybody wants it.
- **Not generalising to the rest of `method/`.** The persona line says READMEs,
  docs and comments are all for the agent, which is a claim about every prose
  page this plugin ships. Following it everywhere in one change is exactly the
  silent scope growth `process.md` forbids; this change fixes the one page where
  the claim is load-bearing and where an issue was filed.
- **Not writing the observation into `method/`.** *The only observed adopter does
  not read it* is a fact about this repository's evidence, not a portable rule —
  it names a person and a moment. The method gets the rule; the evidence stays
  here and in the persona file, which is the split
  [CONTRIBUTING.md](../../CONTRIBUTING.md) tests for.
- **Not resolving whether n = 1 is enough.** The issue says the claim is
  *contradicted, not disproven*, and it is right. That is why the replacement
  says *occasional* and not *never*: somebody who inherited a repository may well
  read CLAUDE.md first, precisely because they have no other way in. The persona
  file already books this under *What this file does not know*, and no second
  observation exists to close it with.

## Data

None. There is no storage contract — the plugin ships prose, and what a version
leaves behind is listed in
[spec.md](../spec.md#what-a-version-leaves-behind). This change moves a
justification inside one payload page and writes nothing anywhere.

## Risks

- **`context-budget` is the promise this is measured against.** Two arguments
  currently hold the hundred-line budget up: human attention, and per-request
  cost. This withdraws one. If the remaining one were not already written down,
  the budget would come out of this change with less holding it than it went in
  with — which is why *What changes* makes the page point at it explicitly rather
  than leaving a reader to notice the opening paragraph four sections earlier.
- **A narrowed claim reads as a weakened one.** *Occasional* is a weaker word
  than *most of why*, and a later reader may take the whole paragraph as
  hedging and drop it. The mitigation is that root placement is stated on the
  convention argument alone, which needs no reader at all to be true.
- **n = 1, and the 1 wrote the plugin.** The evidence is one person's habit in
  their own repositories, and they are the author of the method being corrected.
  This is a real limit on the change and the reason it narrows rather than
  reverses: the claim goes from asserting a reader to describing one as
  intermittent, which is true under both readings of the evidence.
- **No gate holds any of this.** Prose in `method/` is checked for links and for
  being reachable, never for being true. What catches a justification going wrong
  is somebody filing an issue, which is what happened here and took nine versions.

## Acceptance checks

1. `method/claude-md.md` contains no claim that a human reader is why the file is
   prose, and *Where it goes* still gives a reason for the repository root.
2. The hundred-line budget in *Length* is unchanged, and the page says what that
   number rests on.
3. `python3 .github/scripts/verify.py` is green, and reports the same rule and
   workflow counts as before this change — nothing was added to the spec layer.
4. Read the page against
   [`specs/personas/agent-accelerated-owner.md`](../personas/agent-accelerated-owner.md):
   no sentence in it now asserts something that file contradicts.

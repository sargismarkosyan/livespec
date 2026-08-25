# Spec 0005: the first persona

- **Status:** approved
- **Issue:** [#14](https://github.com/sargismarkosyan/livespec/issues/14)

## Who this is for

For once this section is literally the subject: it is *about* who this is for.

**[`@persona:agent-accelerated-owner`](../personas/agent-accelerated-owner.md) —
"Ren".** Somebody running more than one repository at a time, driving changes
through an agent many times a day because there is more to do than there are
hours, who reads the spec layer and never the documentation, and who is building
guardrails for contributors who have not arrived yet.

**Provenance, which is this file's to carry and not the persona's.** One
interview, 2026-08-25, two rounds of four behavioural questions, run from the
`setup` chain. **n = 1, and the 1 wrote livespec.** That is a real problem and
it is the reason this section is this long.

What makes it usable evidence anyway is that most of it is behaviour observed in
*other* repositories, wearing the adopter's hat rather than the author's:

| Where | What was observed |
|---|---|
| `sargismarkosyan/wf-developer-agents`, `triage-review/` | tracker is a corporate GitLab; the repo's own hand-built `feedback` skill was **kept** rather than replaced with the plugin's ([#10](https://github.com/sargismarkosyan/livespec/issues/10)) |
| `sargismarkosyan/todo-change` | `feedback` filing into livespec instead of the repository in use ([#12](https://github.com/sargismarkosyan/livespec/issues/12)) |
| this repository, as an adopter | a bindings claim nobody had ever run ([#6](https://github.com/sargismarkosyan/livespec/issues/6)); an eval framework rebuilt where one already shipped ([#5](https://github.com/sargismarkosyan/livespec/issues/5)) |

By NN/g's taxonomy this is closest to an **ad-hoc persona**: qualitative in
origin, one participant, no second observation. It is declared as one here so
nobody three versions from now cites it as research. The four open questions at
the foot of the file are the ones that would move it, and *"whether anybody else
behaves this way"* is deliberately first.

**On `personas/README.md`'s own rule that the author is not a persona.** The rule
stands and this does not breach it. What is written down is what this person does
**as somebody adopting livespec into their own repositories** — filing rather
than fixing, keeping the local skill, fixing the pipeline rather than bypassing.
Nothing about maintaining livespec is in the file. The distinction was put to
them before the interview started and answers were given under it.

## The job behind the request

Every `refine-*` skill opens by reading `specs/personas/`, and `refine-spec` says
in its own body that the obvious-seeming requests are where a spec quietly gets
written for the wrong person. With the layer empty, there is no wrong person to
avoid — there is nobody at all, and each spec argues from first principles about
somebody the author is imagining fresh each time.

## Why now

[#14](https://github.com/sargismarkosyan/livespec/issues/14) is a version old and
names this exactly: `CLAUDE.md` has called `refine-personas` "the next thing to
run" since 0.6.0, four change specs have shipped in front of it, and three issues
carry `needs-spec` behind it. The gates cannot see any of this — `trace.py`
treats an empty layer as unarmed, deliberately — so it is invisible to every
check that exists, in the one repository whose whole claim is catching that state
in somebody else's.

It has already cost something concrete.
[`0004`](0004-setup-can-be-offered.md) had to name its person in plain prose —
*"somebody who has just enabled the plugin and has not yet been told there is a
command"* — because there was no id to cite. That sentence is a persona written
inline, in a change spec, by the failure mode this layer exists to prevent.

## The end value

A change spec written in this repository can name who it is for and be wrong
about it in public. Today it cannot be wrong, because it cannot be checked.

**How we would know it worked:** the next change spec's *Who this is for* cites
`@persona:agent-accelerated-owner` and one of the situations in that file,
instead of describing a person in prose. And the first time a request is turned
down — or reshaped — because it does not fit this person, the file has paid for
itself.

## What changes

- `specs/personas/agent-accelerated-owner.md` — new. Problem, habits, two
  evidenced refusals, three quotations, five open questions.
- `specs/personas/README.md` — the layer stops saying **Empty**, gains the
  persona row, and records that the seed has been spent and must not be expanded
  a second time.
- The seed's own reading is **corrected in the open.** It said engineers who
  *"hate having the spec be the source of everything"*. The interview found the
  rejection is elsewhere: **under-inference** — the agent not deriving what the
  repository already says. Decay and scale survived contact; that clause did not,
  and it is marked spent rather than quietly deleted.

**Rules added or changed:** none, and not owed. This change moves who the product
is for, not what it does; there is no user-visible behaviour to write a `Rule:`
against. That is a different situation from
[`0002`](0002-setup-finishes-what-it-names.md) and
[`0003`](0003-main-releases-itself.md), which owed Gherkin they could not write
because `specs/workflows/` was empty — the debt there is real and unchanged by
this spec.

**Ledger:** nothing to move. `workflow → persona` and `persona → workflow` both
already read *automated* in
[setup/README.md](../setup/README.md#gate-wiring), wired at 0.6.0 and proven by
three faults in `inject.py`. `refine-personas` §4 warns that these rows may read
*not applicable* on a fresh setup and be this change's to move; here they do not,
and the row is left alone rather than re-stamped for having been looked at.

## What we are not doing

- **Not writing the workflow.** [`refine-workflows`](../workflows/README.md) is
  the next skill in the `setup` chain and its own change, with its own approval.
- **Not writing a second persona for the contributors who have not arrived.**
  They are a fact about this person's situation, not a person anybody has met.
  A persona invented to hold an anticipated audience is the exact failure
  `refine-personas` refuses.
- **Not fixing the collision the interview turned up.**
  [`method/claude-md.md`](../../method/claude-md.md) justifies prose by *"being
  findable by a human is most of why the file is written in prose rather than
  configuration"*, and the only observed adopter does not read that file. That is
  a live method page contradicted by evidence; it is recorded here and belongs in
  its own issue, not in a persona change.
- **Not backfilling personas for anything that already shipped.** `setup` §7.
- **Not filing new issues for the four misses.** They are #12, #10, #6 and #5,
  already filed by the person who found them — which is itself one of the habits
  in the file.

## Data

The storage analogue here is the id. **`@persona:agent-accelerated-owner` is
permanent from the moment this lands** — `ids-are-permanent` in
[spec.md](../spec.md#the-promises-that-belong-to-no-single-workflow) — so it is
named for what the person durably does rather than for a situation they are
passing through. *Solo*, *pre-team* and *first-persona* were all considered and
dropped for exactly that reason: contributors arriving would make any of them
read as a mistake, and a persona id cannot be renamed once it is published.

## Risks

- **`ids-are-permanent`** is the promise most at risk, and it is spent
  immediately: one id, published, unrenameable, chosen from n = 1.
- **The `@retired` tag surviving the version.** The file lands tagged because
  `trace.py` fails a live persona no workflow names, and `specs/workflows/` is
  empty. That is the tag's one honest use — mid-transition, for a version — but
  a tag left on is indistinguishable from a shelf, which
  `refine-personas` §5 exists to prevent. **This version is not finished until
  `refine-workflows` names this persona and the tag comes off.** Both READMEs say
  so, in the place somebody would look.
- **The persona becoming a vote for what is already built.** The one participant
  wrote the plugin, and every habit in the file is one livespec already serves —
  filing rather than fixing *is* `feedback`; reading the spec layer *is* the
  three refine skills. A persona that only ratifies the existing product has
  found nothing. The mitigation is the open questions, and the honest test is the
  first request this file turns down.
- **A second interview contradicting this one**, from somebody who did not write
  the plugin. That would be the file working, not failing — and it is why the
  provenance is a table rather than a sentence.

## Acceptance checks

1. `python3 .github/scripts/verify.py` is green with the persona file present.
2. `specs/personas/README.md` no longer says the layer is empty, and the row
   points at a file that exists.
3. The persona file contains no line saying what livespec must or must not do.
   Read it once looking only for that.
4. Read the *problem* paragraph alone and check it is recognisable — it is the
   part that would have to be rewritten first if the rest were lost.
5. After `refine-workflows` lands, `@retired` is gone from the first line and
   `trace.py` maps the workflow to this persona.

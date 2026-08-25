@journey:trusting-the-spec-again @persona:agent-accelerated-owner

# Trusting the spec again

## The lens

| | |
|---|---|
| **Actor** | Ren. Runs several repositories, drives changes through an agent many times a day, reads the spec layer and never the documentation. |
| **Scenario** | A repository that already has a spec — an old one, with nothing checking it. Asking for a change breaks something else, and what comes back is not what was needed. |
| **Goal** | To ask for a change and get the change, without first explaining the repository and without paying for it a week later. |
| **Span** | Continuous rather than episodic. There is no gap to come back from: the spec moves with every change, and the arc is made of many short returns over days and weeks. |

**Expectations** — what they think is going to happen:

- The spec will stop being old, because something will notice when it goes stale.
- Asking for one thing will stop breaking another.
- The context will already be there, instead of being supplied again every time.

## The map

*The thinking row is quoted where something was actually said and paraphrased
where it was not. Nothing here is invented.*

| | **Before** | **Putting it in** | **The changes after** | **Where it does not fit** | **Coming back** |
|---|---|---|---|---|---|
| **Doing** | 1. Keeps a spec, by hand, with nothing checking it.<br>2. Asks for a change.<br>3. Gets regressions, and something other than what was needed.<br>4. Supplies the context again. | 5. Puts the gates in, in the language already in the repository.<br>6. Fills the layers in the same sitting.<br>7. Leaves the history alone rather than speccing it backwards. | 8. Asks for changes, many times a day.<br>9. Watches the spec move with each one.<br>10. Stops standing over it. | 11. Hits a part that assumes a repository this is not — the wrong tracker, the wrong assumption about which repo is in hand.<br>12. Files it upstream.<br>13. Fixes it locally and carries on. | 14. Comes back days later.<br>15. Reads the spec layer rather than the code.<br>16. Acts on it without checking it first. |
| **Thinking** | *"the spec was old and not up to date"* — *"whenever I ask something it causes some regressions all the time"* | *(paraphrase) gates first, then who it is for and what they attempt* | *"now I have less need of doing babysitting"* | *"fix the pipeline error, not bypass"* | *(paraphrase) still true — go* |
| **Feeling** | ▂ | ▄ | ▆ | ▃ | ▇ |

**The curve.** It starts at the bottom and the bottom is *before the product* —
a spec that had gone quietly wrong is worse than no spec, because it is still
being trusted. It climbs through the changes that follow, where the payoff turns
out to be early and repeated rather than banked for later: less standing over the
work, every day, starting immediately. It dips where the process meets a
repository it did not anticipate, and that dip is shallow — filed, worked around,
carried on — rather than the near-abandonment somebody would predict. It peaks
at the return, days later, which is the only phase that tests the actual promise:
the spec is read instead of the code, and acted on without being checked.

## Opportunities

Gaps where neither side is at fault.

- **Nothing says whether the install took.** The sitting ends green, and whether
  the process actually holds is not knowable until a change later. Neither the
  sitting nor the change is at fault; the evidence simply does not exist yet at
  the moment somebody wants it.
- **The checks can say the spec is incomplete. They cannot say it stopped being
  true.** A missing test, an attempt nothing implements, a dangling reference —
  all caught. A description that still fits the shape and no longer describes
  what anybody meant reads as green. That is the failure this whole arc is about,
  and it is the one the checks are structurally unable to see.
- **The return is trusted without anything having earned it.** Coming back after
  days away and acting on the spec without checking is the peak of the arc — and
  it looks exactly the same whether the spec is still true or quietly is not.
- **A local workaround has no expiry.** What gets filed upstream and patched
  locally stays patched. Nothing later says the reason has gone and the
  workaround can come out, so the repository keeps a fix whose cause was removed
  somewhere else.

## Ownership and metrics

| Opportunity | What answers it today | How we would know it worked |
|---|---|---|
| Knowing the install took | **nothing yet** | The sitting ends with something demonstrated rather than something asserted |
| Incompleteness caught, untruth missed | the checks, but only for shape | A spec that no longer describes what was meant stops reading as green |
| A return that is safe to trust | **nothing yet** | Coming back cold and acting immediately stops being a gamble that happened to pay |
| A workaround outliving its reason | **nothing yet** | Local patches disappear when the thing they worked around is fixed |

**Three "nothing yet" rows, and two of them are the same moment** — the point
where somebody comes back and believes what they read. That moment is the entire
claim of this product, and nothing in it currently reaches that far.

## What this file does not know

- Whether the arc runs longer than weeks. Everything above was observed over
  days, in repositories belonging to one person. The months-long shape — where
  the specs are either still true or quietly stopped being read — has not
  happened to anybody yet.
- What the arc looks like when contributors arrive. Every phase above is solo.
- Whether a gate blocking something somebody wanted to merge is a trough for
  anybody. It was not for this person, who fixes the pipeline instead.

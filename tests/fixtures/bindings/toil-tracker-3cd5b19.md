# Bindings — what the process means *here*

Every livespec skill reads this file before it assumes a command. Everything in
it is a fact about **this repository**: a sentence that could survive being moved
to another repo belongs in [the plugin](https://github.com/sargismarkosyan/livespec)
instead, and putting it here is how two copies start to disagree.

Reconciled against livespec **1.3.0** (`method/`) on **2026-09-08** — the sitting
that wired the boundaries table. **No row in either table reads *deferred*.** The
last one that did was the coverage demand, and it went whole on 2026-09-09 with
specs [0054](../changes/0054-the-ratchet-that-stopped-ratcheting.md) and
[0055](../changes/0055-four-modules-nobody-had-measured.md); this line said one
still did until the eleventh reading.

---

## The table

| | |
|---|---|
| **Verification** | `npm run ci` — the fast gates, then the instrumented test run |
| **— the free, fast half** | `npm run verify:fast` — **lint**, pipeline parity, citations, links, features, layers, copy escapes, the quarantine clock, §14 corpus freshness, types (~8 s, of which `tsc` is 7). The linter runs first: under 100 ms over the whole tree, it is the cheapest thing that can say no. **Every one of the ten also runs as its own CI step since spec 0059**, which is checked rather than remembered — see the parity row |
| **Test runner** | Vitest 4 (`pool: 'forks'`, sequential — integration tests bind random ports) |
| **Test environment** | Node by default; `// @vitest-environment jsdom` per file for component tests |
| **Coverage tool** | `@vitest/coverage-istanbul` |
| **Coverage scope** | The whole of `src/`, `lib/` and `client/`, minus the exclusions named in `vitest.config.ts` with their reasons — **since 2026-09-08**. Before that it was three files, and everything else was out by being absent from an `include` list, with the reasons in prose here rather than in the config the runner reads. See *What coverage does not cover* |
| **Thresholds** | **Per file, in `vitest.config.ts`, which is the source of truth.** **Every file in scope demands the whole of it — 100 on all four measures — since 2026-09-09, spec [0054](../changes/0054-the-ratchet-that-stopped-ratcheting.md).** `src/api.ts` was the last ratchet and it came out rather than moving up: 256 uncovered branch arms covered, from a floor of 89.03 / 77.94 / 99.04 / 97.88 that had not been raised across nine change specs. Everything not demanded is excluded by name, each with its reason. No global number: a per-file floor catches every regression a global one would, and an aggregate sitting on its own score is the shape livespec's `0030` stopped permitting. This row is a copy of the config and loses to it every time |
| **Rule ids** | Gherkin scenario tags: `@PA-01`, `@SL-03`. Two-to-four uppercase letters, a dash, digits |
| **Not-yet-built tag** | `@pending` on a scenario · `@planned` on a workflow file. The method calls both `@planned`; only the workflow half is spelled that way here, and `scripts/check-spec-features.mjs` reads a `@planned` scenario as **live** — so a rule tagged the method's way fails the build for having no test |
| **Rule-claiming helper** | `rule('@PA-01', () => { … })` from [`tests/support/rule.ts`](../../tests/support/rule.ts) |
| **Rule-layer gate** | `npm run test:features` → `scripts/check-spec-features.mjs` |
| **Upper-layer gate** | `npm run test:layers` → `scripts/check-spec-layers.mjs` |
| **Linter** | `npm run lint` → **Biome 2.5.12**, pinned exactly, configured in [`biome.jsonc`](../../biome.jsonc) — spec 0057. Correctness and dead-code rules only; the formatter is present and **off**. Every rule that is off carries its reason in the config, counts included |
| **Copy gate** | `npm run test:copy` → `scripts/check-copy-escapes.mjs`. Reads `client/`, not the spec tree — an escape sequence in JSX text renders literally, and nothing else here can see it (spec 0024) |
| **Quarantine clock** | `npm run test:quarantine` → `scripts/check-quarantine.mjs`. Reads [`tests/support/quarantine.json`](../../tests/support/quarantine.json) and fails once the highest spec in `specs/changes/` has passed an entry's `until` — spec 0056. Empty today |
| **Pipeline parity** | `npm run test:pipeline` → `scripts/check-pipeline-parity.mjs`. Fails when `verify:fast` runs a check no step in `.github/workflows/ci.yml` runs — spec 0059. One direction only: CI also runs the instrumented pass and the injector, which the hook leaves to it on purpose. It is in both lists, so it is subject to the rule it enforces |
| **Flake reporting** | `retry: 1` in `vitest.config.ts`, paired with [`tests/support/flake-reporter.ts`](../../tests/support/flake-reporter.ts): every test that passed only on a retry is printed with the error from the attempt that failed, and written to `reports/flakes.json`. The exit code is untouched — a flake is a finding, not a failure — spec 0056 |
| **Gate JSON** | `node scripts/check-spec-layers.mjs --json` — the report reads this, never the tree |
| **Fault injection** | `npm run verify:gates` (fast) · `npm run verify:gates:coverage` (slow, manual) |
| **Feature file soft limits** | 120 lines, 6 rules — warnings, never errors |
| **`@refusal`** | tags a scenario whose promise is that nothing happens, so absence-only tests are not reported as the wrong kind |
| **Test discovery** | `tests/unit/`, `tests/integration/`, `tests/component/`, `tests/behaviour/`, `tests/workflows/`, helpers in `tests/support/` and `tests/helpers/` |
| **Where the app runs** | `npm run dev` → Vite on **5173**, Express on **3000**. Open 5173 |
| **Database** | Optional. Unset `DATABASE_URL` runs a full in-memory store; tests never touch Postgres |
| **Issues** | GitHub, `gh issue create --repo sargismarkosyan/toil-tracker`, label `backlog` |
| **CI check** | `Test & Coverage` — the job's `name:` in `.github/workflows/ci.yml`. It runs on every pull request and is **required by nothing**: no check can be required here, see below |
| **Branch protection** | **None, and none is available.** See below |
| **PR report** | `scripts/pr-report.mjs`, posted by the `Spec-layer report` step |
| **Deliverable** | A recorded clip per version in `docs/screenshots/`, **embedded inline** in the pull request body |
| **Sketch before approval** | Every change spec is handed over with a page drawn from it — what it is now beside what it would be, what moves and what stays with the reason against each, the count that changed — before approval is asked for. Drawn from the change spec, never recorded from the app: the *line of text* exemption below is the picture's and does not reach this. Asked for since livespec 0.27.0; this row was written by the reading of 2026-09-02, and nothing here recorded it before then |

---

## What a pull request has to carry

**The picture, shown and not linked.** A change that alters what the app looks
like carries a recording **embedded in its body**, from `docs/screenshots/`,
named for the change spec that shipped it. Inline is the preference and the
default — the exact markup, and why the obvious host does not work, are below.

*Which form* is a fact about the change, not a convenience:

- **A recording** is the standing case here. Almost everything this product does
  is a thing *happening* — a room filling with cards, a timer running down, votes
  landing live on a projected board — and a frozen frame is exactly the part that
  does not carry.
- **A still** is right when the whole result is a screen sitting there: an empty
  state, a settings page, an export preview.
- **A line of text** is right when there is nothing to see — tooling, a doc, a
  refactor. *"It is hard to record"* is not that case.

**The sketch is not covered by that third case.** It is drawn from the change
spec at approval, not recorded from the app at the end — the row in the table
above is its own, and a change with nothing to see still has a change spec.

Recorded on the branch before the PR is opened, by `/livespec:record-clip`.

**The clip is embedded inline, never left as a link.** This is a stated
preference and it is the default here: a reviewer should see what the version
did without deciding to click anything.

```sh
sha=$(git rev-parse HEAD)
echo "<img src=\"https://github.com/sargismarkosyan/toil-tracker/blob/$sha/docs/screenshots/vNNN-slug.gif?raw=1\" alt=\"...\" width=\"720\">"
```

**Pin it to a commit SHA, never a branch** — branches are deleted on merge and
the link goes with them.

**Why that host and not the obvious one.** `raw.githubusercontent.com` is
unauthenticated and answers `404` for a private repo whatever the ref, so it
renders a broken image rather than an error anybody notices. This paragraph used
to prescribe exactly that, and PRs
[#141](https://github.com/sargismarkosyan/toil-tracker/pull/141),
[#151](https://github.com/sargismarkosyan/toil-tracker/pull/151) and
[#163](https://github.com/sargismarkosyan/toil-tracker/pull/163) each shipped the
dead image it produced.

`github.com/.../blob/<sha>/<path>?raw=1` is a different thing: it is GitHub's own
domain rather than a third-party host, so it is not routed through the camo image
proxy and is served against the reader's own session. Anybody who can see the
repo can see the image. **Confirmed working on
[#180](https://github.com/sargismarkosyan/toil-tracker/pull/180), 2026-08-31.**

This paragraph previously claimed inlining was impossible without GitHub's
`user-attachments` CDN and a human dragging the file into the web editor. That
was wrong — the raw-host failure had been generalised into "no URL can work",
and the one URL that does was never tried. Recorded here because the wrong
version of it survived three pull requests.

**Keep a text link beneath the image.** One line, small. It costs nothing and it
is what makes a future failure degrade to the old behaviour instead of to
nothing — which is precisely what those three PRs lacked.


**Which changes owe Gherkin.** A PR touching any of these quotes the Rule and its
Examples in the body, inline or linked at the commit SHA:

```
specs/features/*.feature      specs/workflows/*.feature
tests/behaviour/**            tests/workflows/**
```

A change touching none of them says nothing. Ceremony on every PR is ceremony
that gets skipped on the one that needed it.

---

## What proves a rule is true here

**An ordinary test suite.** There is code to call, so it is called.

A behaviour test names its rule through `rule()`:

```ts
import { rule } from '../support/rule';

rule('@PA-01', () => {
  it('restores her own cards after a reconnect', () => { /* … */ });
});
```

`rule()` looks the id up in `specs/features/` and **throws where the test is
written** if the scenario does not exist or is still `@pending`. That is most of
what the binding buys: a typo fails on the first run rather than in CI.

**The `@` is required.** `scripts/check-spec-features.mjs` finds a test's claim by
scanning source text for `/@([A-Z]{2,4}-\d+)/`, so `rule('PA-01', …)` would be
invisible to it and the scenario would be reported as having no test at all. The
helper refuses the un-prefixed form and says why.

The describe label it builds carries the tag **and** the `— spec §NN` citation,
the latter derived from the feature file's own `@spec-NN` tags. One id satisfies
both existing gates with nothing to keep in sync by hand:

```
[PA-02] Ownership is re-bound by name, so an engineer can still edit — spec §03, §10 @PA-02
```

### Existing tests do not have to claim a rule

The test files that predate this process are **unit tests as far as livespec
is concerned**, wherever they live, until a rule exists that they answer to. They
already carry `— spec §NN` citations and many already reference scenario tags,
which is what keeps the rule-layer gate green over all 283 scenarios as of
2026-09-08.

Nobody should spend a week retrofitting `rule()` into them. The two folders that
carry the new discipline are:

| Folder | Discipline the gate enforces |
|---|---|
| `tests/behaviour/` | every test sits inside a `rule()` block; a file with no `rule()` at all is rejected |
| `tests/workflows/` | every file names a `@workflow:` id — a walkthrough has a workflow to claim, not a rule |

Neither is empty any more. `tests/behaviour/` holds 45 files and 199 `rule()`
blocks as of 2026-09-08 (33 and 141 at spec 0042; 4 and 18 at spec 0011) and
`tests/workflows/` holds the 2 walkthroughs. `tests/unit/`, `tests/integration/` and `tests/component/` are
untouched by that rule.

---

## Branch protection: none, and none is available

Read back from the platform rather than inferred from the tree:

```sh
gh api repos/sargismarkosyan/toil-tracker/branches/main/protection
```

Last read **2026-08-31**, after #160. It returns:

```
403 — Upgrade to GitHub Pro or make this repository public to enable this feature.
```

So `main` is **unprotected and cannot be protected** on this plan. The CI check
named above runs on every PR; nothing makes it *block* a merge. Any row
claiming otherwise would be the worst line in this file.

What would change it: making the repository public, or a GitHub Pro subscription.
Both are decisions well outside a setup sitting.

### The local pre-push hook is not a gate

Written here rather than in the ledger, because it is true of one machine rather
than of the repository. `bash scripts/install-hooks.sh` installs a `pre-push`
that:

- blocks direct pushes to `main` / `master`;
- runs `npm run verify:fast` — the same list `npm run ci` reads, not a second
  copy that would go stale the first time a gate is added. That list gained
  `tsc --noEmit` on 2026-08-30, which took the hook from under a second to
  about eight.

It deliberately leaves **`npm run test:coverage`** to CI: a minute-plus per push
is how a check stops being kept, somewhere around the fourth commit.

It is **opt-in per clone** (a fresh clone has nothing installed until somebody
runs that line) and bypassable with `--no-verify`, on purpose. It therefore gets
**no row in either ledger table**: a bypassable courtesy recorded as a refusal
would be counted as coverage by anybody adding up the rows.

**And three checks in that list run nowhere but here** — found by the eleventh
reading, 2026-09-09. `.github/workflows/ci.yml` names its eleven steps by hand
instead of running `npm run ci`, and that hand-copy has drifted: **`npm run
lint`** (spec 0057), **`npm run test:copy`** (spec 0024) and **`npm run
test:quarantine`** (spec 0056) are in `verify:fast` and in no CI step. The
sentence above — *the same list `npm run ci` reads, not a second copy that would
go stale the first time a gate is added* — is true of the hook and was never
true of `ci.yml`, which is the second copy, and it went stale three times; the
copy gate has been outside CI since it was written on 2026-08-31. None of the
three is a gate `method/gates.md` names, so none earns a ledger row, and this
paragraph is what they get instead — because with branch protection unavailable
the only thing standing behind them is a hook anybody can walk past. Putting
them in the pipeline is an ordinary change with an address, not a setup sitting:
[#263](https://github.com/sargismarkosyan/toil-tracker/issues/263), which also
says why the obvious fix — CI running `npm run ci` — is the wrong one, since
`verify:fast` is `&&`-chained and would collapse nine independent verdicts into
one.

**Closed by spec [0059](../changes/0059-the-pipeline-that-did-not-inherit.md),
2026-09-09**, and the paragraph above is left as the account of what was found
rather than edited into agreement with the present. All three are CI steps now,
in the `if: ${{ !cancelled() }}` shape the other gates use — and, more to the
point, **the two lists are no longer trusted to match**: `npm run test:pipeline`
fails when the fast half runs something no step here runs. Spec 0057's own
acceptance check had asserted *"the pre-push hook and CI inherit it"*, which was
true of the hook and impossible for CI, and that sentence is why the fix is a
check rather than three more hand-written steps.

---

## What coverage does not cover

**Rewritten 2026-09-08, when the scope stopped being three files.** What stood
here before was a paragraph explaining why `client/` and `lib/` were out — which
is exactly the second copy of the gate `0030` forbids, because the config the
runner reads knew nothing about it. The exclusions now live in
`vitest.config.ts`, each with its reason, and this section says what that
revealed rather than repeating the list.

**The number nobody had ever taken.** The old row said *roughly two thirds of the
codebase* is ungated and never said what it scored. Measured on 2026-09-08, for
the first time:

| | Lines | Branches | Uncovered arms | Gated before |
|---|---|---|---|---|
| `src/` (api, store, operations) | 5,279 | 84.9% | 256 | yes |
| `lib/` | 2,283 | 90.8% | 31 | **no** |
| `client/` | 17,433 | **47.7%** | **2,253** | **no** |

`client/` had nine times the uncovered branches of `api.ts` — and `api.ts`'s 256
are the ones this ledger had been worrying about for nine change specs while
those 2,253 sat with no address at all.

**What went whole, and what it cost.** `lib/` and `client/lib/` — 24 files —
are demanded at 100 on all four measures. Sixty branch arms were covered to get
them there, and **seven arms that could not be reached at all were deleted from
the source rather than excused**: a `union > 0` guard whose zero case an earlier
return already took, two `?? ''` fallbacks on values that cannot be empty by the
time they arrive, a category tie-break for two names starting at the same index
where none of the three is a prefix of another, a per-pair deadline checked one
statement after it was created, and a try/catch plus a `.catch` around a promise
that resolves to `null` instead of rejecting. An unreachable arm and an untested
one are indistinguishable to every gate that reads a file, which is the whole
reason to tell them apart in the source rather than in a threshold.

**Two things the wider scope found that nothing had looked at.**

- **Four server modules nobody had ever measured.** `authRoutes.ts` at 64.9%
  branches, `auth.ts` at 76.9%, `orgRoutes.ts` at 82.4%, `notifications.ts` at
  87.5% — invisible while the include list was three files. **All four went
  whole on 2026-09-09**, spec
  [0055](../changes/0055-four-modules-nobody-had-measured.md): 115 uncovered
  arms, of which about half were the Google sign-in flow, which had never run
  under a test because reaching it means standing in for Google. It does now,
  and that stand-in has a row in [*The boundaries*](#the-boundaries). Nothing
  under `src/` is excluded any more except the bootstrap files and the modules
  that table calls *unreachable*.
- **`client/analytics.ts` had no test at all** — six lines every page imports,
  both of them guarding on a `window.gtag` that an ad blocker or a first paint
  can leave absent. Covered, and demanded whole.

**The views were out, and the reason was not that they are untestable.** 26
pages and 11 components, 2,207 uncovered branch arms on 2026-09-08. They *are*
tested, through `tests/component/` and `tests/behaviour/`, at the level of
rendered controls and the requests they produce; what those tests do not do is
reach every JSX conditional. The exclusion list is today's uncovered code
written down, and the way out of it is to delete lines from it one at a time.
**Six have been**, and each was measured on the way out — `client/context/**`
on 2026-09-09 (spec
[0058](../changes/0058-the-first-line-out-of-the-list.md), one file, 12 arms),
`client/components/**` on 2026-09-15 (spec
[0077](../changes/0077-the-controls-nobody-had-ever-rendered.md), twelve files,
192 arms), **the four sign-in pages** the same day (spec
[0078](../changes/0078-the-sign-in-page-nothing-had-ever-rendered.md), 30 arms),
**`Credits.tsx`** (spec
[0079](../changes/0079-the-second-player-on-a-page-nothing-had-opened.md), 26
arms), and **the four pages that need no room standing up** — `Home.tsx`,
`SessionJoin.tsx`, `Organizations.tsx`, `SessionRoot.tsx` (spec
[0080](../changes/0080-the-page-nobody-had-ever-been-signed-in-on.md), 47 arms
and 23 functions), and **`AccountSettings.tsx`** on 2026-09-16 (spec
[0081](../changes/0081-the-five-requests-nobody-had-made.md), 62 arms and 14
functions). The third is the first slice of the pages campaign, and it is
why `client/pages/**` is no longer one line: a glob standing for 26 files cannot
be deleted a quarter at a time, so what is still out is named one file each and
the next slice is a deletion again. **The fourth is the first slice to prove
that**, being a single deleted line.

**What the components turned out to hold, and it is the finding rather than the
number.** 52 functions had never been called by any test, six of them exported
controls nothing in this repository had ever rendered — `ConfidencePicker`, the
1–5 an OKR check-in turns on, and `Topbar`, which every screen draws.
*They were the least covered because they are the most shared*: every test that
touched them reached them through a page and asserted the page, so a component
drawn by six screens had its common path walked six times and its other arms
never.

**Ten guards nothing could reach were deleted from the source rather than
excused**, and they came in four families rather than ten accidents:

| | How many | What made it unreachable |
|---|---|---|
| a ref that is always attached by then | 3 | the element is rendered unconditionally and every caller runs after commit |
| zero is a silence, never a level | 3 | `MusicPlayer`'s remembered volume can only ever be written a level above zero, so two `if (volume > 0)` writes and a `\|\| DEFAULT_VOLUME` on the way back out were all standing on it already |
| **a predicate written twice** | 3 | once as `disabled` on a control and again as an early return in the handler behind it — and a disabled control dispatches no click. Three files, three different controls |
| a fallback `await` already provides | 1 | `await (p ?? Promise.resolve(null))` is `await p` |

**What the sign-in pages turned out to hold is the same finding one layer out.**
`Login.tsx` is not only a page: it exports `AuthBrand`, `ErrorBanner`, `Field`,
`Divider` and `GoogleButton`, and the other three doors are drawn out of them.
One of its ten functions had ever executed — `ErrorBanner`, because `Home.tsx`
and `SessionJoin.tsx` import it from `./Login` and *their* component tests
render *them*. **Nothing in this repository had ever rendered the sign-in page
at all**: the two tests that named the file both opened it with `readFileSync`
— `tests/unit/design-system-forms.test.ts` scanning the account pages for a
field with no `name`/`autoComplete`, and `tests/behaviour/narrow-viewport.test.ts`
reading it for the class names the breakpoint applies through. Both are the
right tests, both stay, and neither mounts anything. **No unreachable arm turned
up in the four** — the *predicate written twice* family did not recur here.

**What the credits turned out to hold is what kept them out.** The file was
last on the list because it read as the cheapest thing there — a static licences
page — and it is not one: its only control is an **audio player of its own**, a
private copy of the room's that shares `lib/music.ts` with it and nothing else,
and all 26 of its branch arms are that player. Two of its limbs could not run
and were deleted rather than covered, both in families 0077 had already named: a
ref that is always attached by then (the same guard 0077 deleted from
`MusicPlayer` twice, still standing in the copy nothing had rendered), and an
`ended` listener three lines below `el.loop = true` — a looping element never
fires it. What the deletion did not decide is which of those two the page should
have been; that is
[#321](https://github.com/sargismarkosyan/toil-tracker/issues/321), beside
[#320](https://github.com/sargismarkosyan/toil-tracker/issues/320) for the
autoplay refusal this player answers with silence.

**What the four cheapest pages turned out to hold is the same finding a third
time, from the other end.** Eighteen of the 23 uncovered functions were in
`Home.tsx`, and they are one fact: every test that rendered the creation page
mocked `useAuth` to `{ user: null }`, so the whole signed-in surface — saved
groups, teams, the invite box, the prompt categories and every path through
Create — had never run. There it was *the least covered because the most
shared*; here it is **the least covered because it is behind the door every test
walks past**, a mocked `useAuth` returning `null` being the cheapest way to
render a page. **The *predicate written twice* family recurred**, after two
slices that did not see it: `Home.tsx`'s empty-name guard was deleted, its only
caller being a Create button `disabled` on the same predicate. `SessionJoin.tsx`
carries the identical two lines and **keeps them** — its name field submits on
Enter, which is a door past the disabled button, so there the guard runs. Two
pages, one predicate written twice in both, dead in exactly the one with no
second way in. That the two forms disagree about Enter is
[#324](https://github.com/sargismarkosyan/toil-tracker/issues/324).

**What the account page turned out to hold is a count.** It makes six requests —
the display name, the email address, the password, Google, the notification
setting, and the account itself — and **one of them had ever been sent under a
test**, spec [0081](../changes/0081-the-five-requests-nobody-had-made.md). The
covered one is the password, and it is covered because a bug was filed about it:
the file's six tests are the regression guard for the Google-only dead end and
say so in their own header. So the five that had never run were the five that
*change* the account, three of them irreversibly. The largest family inside the
62 arms is the same one `api.ts` had — **the refusals**: the identical four
lines written six times, 18 arms, of which 15 were cold, and this page is the
only place a person ever reads what the server said no with. **Nothing was
deleted from the source**, and the reason is worth keeping: the *predicate
written twice* needs a `disabled` that repeats a **validation**, and every
control here is disabled on an **in-flight** flag instead. The one control that
is disabled on a validation — *Permanently delete*, which will not arm until the
typed address matches — is the one whose handler checks nothing at all.

`client/pages` is what #251 still holds: **1,641 arms across the 16 files still
excluded**, re-measured 2026-09-16 with the exclusion lifted — not the 2,011 the
issue carries from 2026-09-09, because the pages are where the work has been and
the work has been covering them incidentally. It is still a campaign rather than
a change: one slice per page.

**That directory total is stable to about ten arms**, which is what spec 0079
wrote down as an aggregate it could not reconcile and spec 0080 undercounted.
0080 measured three runs of the same commit at 1,766 / 1,765 / 1,763 covered and
named the cause: two `{timer && …}` arms in `SessionBoard.tsx`, which render or
do not depending on when the run looked. Three runs after spec 0081 measured
1,879 / 1,880 / 1,871, and diffing *those* per-branch finds a **second family**,
larger than the first:

| Where | Arms | Why it moves |
|---|---|---|
| `SessionBoard.tsx` | 2 | **the clock** — `{timer && …}`. 0080's finding, unchanged |
| `SessionLobby.tsx` | 8 | **a promise** — the `isOwner` invite panel and the signed-out notice both sit behind `ownerResolved`, which an async owner lookup sets. Whether a test ends before or after that microtask settles moves eight arms together |
| `SessionFacilitator.tsx` | 1 | the same family — `if (!cancelled && data)` inside a `.then` on a resurfacing lookup |

**Read a slice delta off per-file numbers, never off this aggregate.** And the
warning 0080 left for one file now covers three, for two different reasons:
`SessionBoard.tsx` has to pin its clock before it can hold 100, and
`SessionLobby.tsx` and `SessionFacilitator.tsx` have to settle their own
promises. The brief for each of those slices should say which of the two it is
asking for — they are not the same job.

**`api.ts` went whole on 2026-09-09** — spec
[0054](../changes/0054-the-ratchet-that-stopped-ratcheting.md) — and with it the
last ratchet in this repository. It had 256 uncovered branch arms of 1,200 and a
floor read off a report after spec 0043 that nine change specs had not raised.
The first of the two ways out turned out to be a day's work rather than a
campaign: **all 256 are covered**, in four test files, and five arms nothing
could ever reach were deleted from the source rather than excused.

**The largest family was the refusals**, and that is the finding rather than the
number. Roughly 120 of the 256 were `if (!session)`, `if (!activity)` and
`if (!mayFacilitate(…))` — the three questions every route and every socket
handler opens with, and precisely what a stale tab or a hand-rolled request
meets. **Nothing in this repository had ever checked that one of them fires.**
The socket half of them refuses *silently*, which is right for a transport whose
clients are screens rather than callers, and is exactly why: a silent refusal is
indistinguishable from a handler that was never reached. The tests settle it
with a probe — `activity:update` against a session id that does not exist, one
of only two handlers that answers the socket rather than the room — emitted
after the refusals, on the same connection, whose ordering is what makes the
answer mean anything.

**The rule-bound measure, and why it is not the two folders.** livespec's shape
is a second coverage pass over `tests/behaviour/` + `tests/workflows/`. That
would be wrong here and was measured to prove it: at spec 0004, when the
definition was chosen, those folders reported **30.19%** statements, which reads
as *the spec reaches a third of the product* when what it actually measures is
*two folders are new*. 52 rules predate livespec and are bound through the
`@XX-NN` tag citation in `tests/integration/`, which is this repo's rule
binding — 52 of the **105** this repository held when that sentence was written,
and of **369** on 2026-09-16.

So rule-bound here means what the binding says: **every test file that names a
rule**, wherever it lives. Measured 2026-09-16, after spec 0081 — **99 of 151
test files**; on 2026-09-08 after spec 0051 it was 66 of 100, as the report on
[#244](https://github.com/sargismarkosyan/toil-tracker/pull/244) read it; on
2026-09-03 after spec 0043 it was 55 of 90 and 76.05 / 71.58 / 83.08 / 82.59,
spec 0011 measured 22 of 59 and the first reading of this table saw 16 of 55:

| | Gated | Rule-bound |
|---|---|---|
| statements | **100%** | **79.17%** |
| branches | **100%** | **76.34%** |
| functions | **100%** | **79.87%** |
| lines | **100%** | **80.58%** |

Read it as the diagnostic it is: about **a fifth** of the covered business logic
answers to no written rule — and the twelfth reading is the first where that
share *grew*. Between 2026-09-08 and 2026-09-16 the gated number went 92.54 → 100
and the rule-bound one 78.61 → 79.17: the pages campaign of specs 0077–0081
covered nine hundred branch arms with component tests that name no rule, which is
the exemption working exactly as written and is also what a widening gap looks
like. It was a seventh at spec 0051, a fifth at spec 0043, a quarter at spec
0011, a third at spec 0004. That is not a target to close — it is the number that
makes the unit-test exemption legible, and it is **never** a threshold.

---

## Known gaps

**The recording viewport is 1440×900**, halved to 720×450 by the stitcher.
Every clip is recorded at one size or the series stops being one series, and this
paragraph is the only place that size is written down — `record-clip` reads it
here. Set by `docs/screenshots/v004-taking-a-merge-back.gif`.

**A change about a narrower screen is composited, not recorded small**
*(spec [0037](../changes/0037-the-room-that-would-not-fit-a-phone.md))*. The two
rules collide the first time a version is *about* a width: a 1440-wide frame
cannot show what a 390px screen does, and recording at 390 would break the
series. So the app is driven at the width the change is about, and each frame is
pasted **unscaled** onto the 1440×900 canvas, captioned with its real size. The
delivered frame is still the series size and the screen is still exactly as wide
as it claims — which also makes the width legible, because the reader sees it
against a laptop frame. Set by
`docs/screenshots/v037-the-room-that-would-not-fit-a-phone.gif`.

**Never scale the frame to fill the canvas.** A 390px screen enlarged to 1440
looks like a laptop running enormous type, which is the one thing the clip must
not say.

**A stacked pull request used to get no checks at all.** CI triggered on
`pull_request` to `main`/`master` only, so a PR based on another branch ran
nothing — and `gh pr checks` reported *"no checks reported"*, which is not
distinguishable at a glance from a run that has not started. Found while merging
a three-deep stack, where two of the three sat unverified until they retargeted.
The filter is off the `pull_request` trigger as of 2026-08-30; `push` is still
filtered so a branch push does not duplicate its own PR run.

**The traceability gate reads source text, not test results.** A test file that
does not compile still satisfies `npm run test:features` — its tags are in the
source, so the gate counts the scenarios as covered. This was found the honest
way, by breaking a test title while binding rules in spec 0007 and watching the
gate report *95 covered* over a file vitest could not parse.

It is not a hole in the pipeline: `npm run ci` runs the suite, so the state
cannot merge. It **is** a limit on what a green `test:features` means on its own —
it says every rule is claimed, not that every claim runs.

**A recorded corpus run now says which files it measured, as of 2026-08-30.**
It did not, and `verify:ai` had written a dated observation into
[§14](../14-intelligence.md) while `ai-writing.ts` was rewritten under it eight
days later — read as current for three weeks by anybody opening that section.
`npm run test:corpus-freshness` is the check, wired into `verify:fast` and CI;
the mechanics are under *Manual verification* above. **It gets no ledger row**:
the ledger holds one row per gate `method/gates.md` names, and this is not one
of them. That is also why its absence was invisible, and the reason it is
written here in full rather than in a sentence somebody could skim past.
Watched to fire before it was believed: a record with one hash altered fails and
names the file, and a missing record warns without failing.

**There is a linter, as of 2026-09-09** — spec
[0057](../changes/0057-the-linter-that-was-three-hand-written-checkers.md),
closing [#254](https://github.com/sargismarkosyan/toil-tracker/issues/254).
Until then `verify:fast` ran six checks and a type check and none of them was
one, while three hand-written checkers did a linter's job by hand.

**Biome rather than ESLint, and the reason is the pre-push hook.** This tree
lints in **70 ms**, inside the noise of an 8-second `verify:fast`; ESLint with
`typescript-eslint` over 203 files is seconds rather than milliseconds, and a
check people wait for is a check people skip. What ESLint buys instead is a
plugin ecosystem, and the three checkers here are not things a plugin covers.

**The first run found 122 errors, 52 of them dead code the type checker is
perfectly happy with** — 29 unused imports, 15 unused variables, 8 unused
parameters, one unreassigned `let`. All fixed rather than suppressed, including
a parameter of `clearSubmissionReady` that no caller's argument had been read
since the function was extracted.

**Three rules are off with counts attached, and the counts are the point**:
`useAwait` (69 sites — `async` with no `await` is how a method conforms to an
async interface, and the three in-memory databases are all that shape),
`noExplicitAny` (45 sites — a real debt, written down rather than enforced,
because a gate that fails on day one for reasons unrelated to the process is a
gate somebody switches off), and `noConsole` (this repository logs on purpose).
There is **no preset**: a preset is a list nobody has read that changes under
you on a minor version.

**The three hand-written checkers stay, and that is the answer rather than a
disappointment.** `check-copy-escapes` reads JSX *text* — no lint rule models
"this string is shown to a person" — and the design-system tests assert against
`design-system/`, a document in this repository that a linter cannot know the
vocabulary of. They were never general rules wearing a local hat.

**It gets no ledger row**: it refuses nothing `method/gates.md` names, the same
reason the type check, the copy gate and the corpus-freshness check get none.

**A flake now says it is one, as of 2026-09-09** — spec
[0056](../changes/0056-a-flake-that-says-it-is-one.md), closing
[#253](https://github.com/sargismarkosyan/toil-tracker/issues/253). Three times
in two days a test failed under a full run and passed alone seconds later:
`@RN-05` waiting on a socket broadcast, `@AC-03` spawning a real server under a
coverage run, and `@SW-03` — which was the one real defect of the three, a
`ceil` boundary that could only ever be right by luck. **Nothing here could tell
those apart except running it again**, under a rule that says every commit is
green.

What landed: `retry: 1` **paired with a reporter that will not let the retry be
quiet**. A silent retry would be worse than the ambiguity — it hides a real
intermittent bug behind a green tick — so every test that passed only on a retry
is printed with the error from the attempt that failed and written to
`reports/flakes.json`, and the exit code is untouched. The rule this enforces is
not *no flaky tests*; it is **a flake is never invisible**. Beside it,
`tests/support/quarantine.json` for a test that flakes repeatedly, with a clock
the tree enforces: every entry names the change spec it must be gone by, and
`test:quarantine` fails once the tree has moved past it. Empty today, on
purpose — a mechanism designed at the moment it is needed is designed badly.

**The exposure is now measured rather than asserted:** 35 of 103 test files wait
on real socket round-trips against a real server on a real port, and 14 hold a
bare `setTimeout` sleep — 20 sleeps between them. Most of those sleeps assert
that *nothing* arrived within a window, which genuinely needs a wait, so they
are counted here rather than rewritten. **The `@SW-03` class was hunted and is a
population of one**: a sweep for time-boundary arithmetic in assertions finds a
single `Date.now() - N * 60_000` in the whole suite, and it is the one already
fixed to 20.5 minutes.

**Neither gets a ledger row.** The reporter refuses nothing, and the quarantine
clock is not a gate `method/gates.md` names — the same reason `test:copy`, the
type check and the corpus-freshness check get none. Both quarantine faults are
in [`fault-injection.json`](./fault-injection.json) and both were watched to
fire.

**The type check is in the pipeline, as of 2026-08-30** — in `verify:fast` and
as its own CI step, closing
[#137](https://github.com/sargismarkosyan/toil-tracker/issues/137). It was held
out while `tsc --noEmit` reported 17 errors, because a gate that fails on day one
for reasons unrelated to the process is a gate somebody switches off. Sixteen
were the same supertest `set-cookie` cast and are now one helper in
`tests/helpers/headers.ts`; the seventeenth was `listGroups(user.id)` against a
signature wanting `{ userId, orgIds }`, so the destructure yielded `undefined`,
the filter matched nothing, and a test named *cascades groups* asserted `[]`
against a query that could only ever return `[]`. The cascade does work — the
assertion just was not asking. Watched to fire: `verify:fast` exits 2 on a
deliberate type error. **It gets no ledger row**: the ledger holds one row per
gate `method/gates.md` names, and a type check is not one of them.

**The cross-link gate covers every markdown file, as of 2026-08-30.** It read
`SPEC.md` plus `specs/*.md` — top level, not recursive — which left **17 files
under `specs/` unchecked**: this bindings file, every layer README, and every
change spec then in the tree. It now walks the tree and names only what is not
ours (build output, `node_modules`, dotted directories), against **18 files
before**.

**A hand-kept list of directories to scan is the thing that drifts**, so there
is no longer one. The cost of the old list was already being paid: a dangling
link had been sitting in this very file for as long as the link existed, and the
only file that could have reported it was one of the ones nobody read.

Watched to fire on real content the moment it was widened — the first run after
the change failed on exactly that link. (`--write` and `--apply` write a
fingerprint file no run has produced yet, so the reference is now plain text
rather than a link to something that is not there.) Then broken on purpose in
`specs/changes/`, a directory the old list could not see, for both kinds it
catches — a missing file and a missing `#anchor` — and it named both with their
real paths rather than a basename, which had been ambiguous across the three
`README.md` under `specs/`.

**It gets no ledger row**: the ledger holds one row per gate `method/gates.md`
names, and a cross-link checker is not one of them — the same reason the type
check and the corpus-freshness check get none.

**Its green line now says how many files it read.** That is why the gap outlived
three audits of this ledger: a gate reading eighteen files and a gate reading
every one of them print the same word, and nobody can compare a count that was
never printed.

**Today's number is in the gate's own output and is deliberately not repeated
here.** It moves with every markdown file added, and the first draft of this
entry proved the point by going stale within one change spec of being written —
it said sixty, and spec 0011's own change spec made it sixty-one. A total nobody
derives is a claim that can only go stale, and is better deleted than corrected.

**The plugin declaration does not survive a clone.** `.claude/settings.json`
declares the `livespec` marketplace, but its source is a **local directory** —
`/home/sargis/Projects/livespec` — because that is how it is installed here.
Cloning this repository onto another machine gets the `enabledPlugins` entry and
no marketplace to resolve it against. Publishing livespec to a git remote and
switching the source to `{"source": "github", "repo": "…"}` is what would fix it.

**`specs/spec.md` does not exist, on purpose.** livespec's layout names it for
product-level prose — why, vocabulary, storage contract. That role is already
filled here by [`SPEC.md`](../../SPEC.md) (the index) and
[`specs/01-purpose.md`](../01-purpose.md), both current and both linked from
everywhere. A third product-prose file would be a restatement, which this
repository's own partition rule forbids and has already been bitten by.

**The coverage demand here *was* a ratchet, which livespec no longer permits —
ended 2026-09-09 by spec
[0054](../changes/0054-the-ratchet-that-stopped-ratcheting.md).** What follows is
the account of it while it stood, and it was written in the present tense over a
state that no longer held until the eleventh reading dated it.
Every threshold in `vitest.config.ts` was the measured score floored to 2dp —
nine steps since setup, branches at **82.37%** — so 281 of 1594 branches were
uncovered and named nowhere, and nothing distinguished a branch that was never
covered from one that stopped being. The exclusions that would give them an
address (`client/`, `lib/`) are described in *What coverage does not cover*
above, which is a paragraph beside the config rather than the config the runner
reads. livespec's
[`0030`](https://github.com/sargismarkosyan/livespec/blob/main/specs/changes/0030-covered-or-named.md)
replaced this shape with *the whole of what is in scope, minus named exclusions
each carrying its reason, written where the coverage tool reads them*. This
repository was set up **2026-08-30**, before 0030, and `setup` runs once — no
skill revisits a threshold after the sitting, and `doctor` never reads the
number. Filed as
[livespec#89](https://github.com/sargismarkosyan/livespec/issues/89). **What
would end it:** #89 shipping a `doctor` pass that reads the number, at which
point the four percentages become an exclusion list in `vitest.config.ts` and
the demand over the remainder goes whole.
[livespec#88](https://github.com/sargismarkosyan/livespec/issues/88) may change
what that remainder is demanded at; it does not change that this row comes out.

**The `doctor` pass arrived.** #89 shipped as livespec 0.31.0
([`0036`](https://github.com/sargismarkosyan/livespec/blob/main/specs/changes/0036-a-row-that-was-right-once.md)),
and the reading of **2026-09-02** was the first here to run on it: it read the
number out of `vitest.config.ts` rather than out of this paragraph, and the
coverage row in the ledger now reads *deferred* with the version that moved it.
#88 shipped too, as 0.30.0
([`0035`](https://github.com/sargismarkosyan/livespec/blob/main/specs/changes/0035-what-the-whole-of-it-comes-to.md)):
the remainder is demanded at the whole of it, once the exclusions are named where
the tool reads them. What is left of this row is the wiring itself — the four
percentages becoming a named scope with the demand over it whole — which is
`setup`'s to build, and the row comes out when that lands.

**Slice one landed on 2026-09-02.** `store.ts` and `operations.ts` demand the
whole of it — 29 branch arms covered by tests, two of them dead arms in
`unmergeSources` that read the source ids twice and now read them once — and
`api.ts` is named in the config as the ratchet it is, dated, with 255 of 1,156
branch arms to cover after spec 0043. This row comes out when the last of those slices lands.

**No second slice had landed by spec 0051 (2026-09-08)**, eight change specs
later, and the `api.ts` floor was not raised across any of them — so the ratchet
has stopped ratcheting and now carries slack. The ledger row below says how much
and what the two ways out are.

---

## The gate wiring ledger

One row per gate livespec's `method/gates.md` names. Nothing here that is not a
gate.

Reconciled **2026-09-08** against livespec **1.3.0**. Rows re-read against the
tree on 2026-08-30, after spec 0010 and the three tooling changes that followed
it (#154, #155, #156).

**No gate in the table below has yet refused anything.** Every one of them has
executed on GitHub Actions on every pull request from
[#138](https://github.com/sargismarkosyan/toil-tracker/pull/138) to
[#262](https://github.com/sargismarkosyan/toil-tracker/pull/262). That is
*observed running*, which is not the same as *observed refusing*: a row reads
**automated** only where the gate has actually turned something down, and
**unobserved** where it has only ever agreed. Fifty-five change specs have
shipped (0004 through 0058; #138 brought 0001–0003) without one of these rows
refusing anything, so no *unobserved* row has closed itself; the rows that are still
unobserved name what would close them.

**The pipeline under this wiring has gone red once, and it was not a gate in
this table.** [#159](https://github.com/sargismarkosyan/toil-tracker/pull/159)'s
first run,
[33333720996](https://github.com/sargismarkosyan/toil-tracker/actions/runs/33333720996),
failed on **2026-08-30** at `Run tests with coverage` — a failing assertion in
`tests/unit/server-bootstrap.test.ts`, not a threshold and not a layer check.
Worth recording precisely because of that: the step that carries the coverage
gate can go red without the coverage gate having an opinion, and a reader
counting red builds as gate refusals would have closed a row that nothing has
closed.

**And once before this wiring existed**, which the sentence that used to stand
here denied outright. That sentence was written from memory of this repository
rather than read back from the platform — the exact failure the branch-protection
row below is built to prevent. Run
[30188921115](https://github.com/sargismarkosyan/toil-tracker/actions/runs/30188921115)
failed on **2026-07-26** at the `Run tests with coverage` step: five component
tests in `SessionBoard.test.tsx`, `localStorage.clear is not a function`. It
predates this wiring by a month (#138 landed 2026-08-30), so it changes nothing
below — what stopped it was the ordinary test run, not a threshold and not a
layer check. Read back **2026-08-30** with `gh run list --limit 100`: 99 green,
that one red; re-read **2026-08-31**, when #159's failure made it two; re-read
**2026-09-02**, after #212: one red in the last hundred, #159's, and the
2026-07-26 one has rolled out of the window; re-read **2026-09-08**, after
#244: none red in the last hundred — #159's has rolled out too, and the one run
not yet green at the reading was the `push` of #244's merge, still in progress;
it finished green before this was committed.

| Gate | State | Command | Covers |
|---|---|---|---|
| rule → test | **automated** | `npm run test:features` | all **53** files in `specs/features/`, 283 scenarios, every one covered by a test — 53 since spec 0052 split `room-reactions.feature`, which moved no scenario, so the scenario count did not change. Read from the gate on 2026-09-09; the row had said 40 and 227 since spec 0042, and 16 and 105 since spec 0011 before that |
| test → rule (id resolves) | **automated** | `npm run test:features` | every test file under `tests/` |
| `@pending` rule that has a test | **unobserved** | `npm run test:layers` | ran green in CI; fault-injected only. Closes the first time a rule is implemented and its `@pending` tag is left on |
| behaviour test outside `rule()` | **unobserved** | `npm run test:layers` | live over `tests/behaviour/` — 45 files, 199 `rule()` blocks as of 2026-09-08, since spec 0004. Ran green; has not yet refused a stray test |
| behaviour file with no `rule()` | **unobserved** | `npm run test:layers` | live over `tests/behaviour/` — 45 files as of 2026-09-08, since spec 0004. Ran green; has not yet refused a file |
| feature → workflow | **automated** | `npm run test:layers` | live over all **67** feature files as of 2026-09-16 — **49** name both workflows, 18 name one. The list of which was typed here at spec 0011 and is not kept: the gate prints the map |
| workflow → feature | **automated** | `npm run test:layers` | live over 2 workflows, both claimed. No longer exempt — the `@planned` tags came off with the walkthroughs |
| workflow → test (walked) | **automated** | `npm run test:layers` | live over 2 workflows, each walked by a file in `tests/workflows/` |
| workflow → persona | **automated** | `npm run test:layers` | armed over 2 workflows — refused spec 0002 until `@retired` came off `@persona:facilitator` |
| persona → workflow | **unobserved** | `npm run test:layers` | live over 1 persona, named by both workflows. Closes when a persona is orphaned |
| journey → workflow | **unobserved** | `npm run test:layers` | ran in CI over 1 journey and passes **vacuously by design** — a journey names no workflow, so this is a safety net. It may never close, and that is correct |
| workflow → journey *(warns)* | **automated** | `npm run test:layers` | warned on both workflows through spec 0002 and was cleared by spec 0003 — fired, and was acted on |
| coverage thresholds | **automated** | `npm run test:coverage` | The whole of `src/`, `lib/` and `client/` since **2026-09-08**, minus the exclusions named in `vitest.config.ts` with their reasons — where they belong, rather than in a paragraph of this file. Refused spec 0004 for an untested socket handler. **Every file in scope is demanded whole since 2026-09-09**, spec [0054](../changes/0054-the-ratchet-that-stopped-ratcheting.md): `api.ts` was the last ratchet, deferred since spec 0042 for the shape livespec 0.28.0 ([`0030`](https://github.com/sargismarkosyan/livespec/blob/main/specs/changes/0030-covered-or-named.md)) and 0.30.0 ([`0035`](https://github.com/sargismarkosyan/livespec/blob/main/specs/changes/0035-what-the-whole-of-it-comes-to.md)) stopped permitting, and it came out by being covered rather than by moving up — 256 branch arms of 1,200, against a floor unraised across nine change specs. **What it does not cover, named rather than implied:** the pages of `client/` (**2,207** uncovered branch arms when the scope was first taken; now **16 files** still excluded — the nine of `client/pages/facilitator/**` and seven named pages, down from 22 — since `client/context/**` came out whole on 2026-09-09, spec [0058](../changes/0058-the-first-line-out-of-the-list.md), `client/components/**` on 2026-09-15, spec [0077](../changes/0077-the-controls-nobody-had-ever-rendered.md), and the four sign-in pages the same day, spec [0078](../changes/0078-the-sign-in-page-nothing-had-ever-rendered.md)), the Postgres and mailer modules the boundaries table calls *unreachable*, the bootstrap files, and — **named here for the first time on 2026-09-16, by the twelfth reading** — the whole of `scripts/`: **15 `.mjs` files, 3,386 lines**, among them every gate this table has a row for. They are outside the `include` list rather than inside the `exclude` one, which is *out by absence* — the exact shape the section below says was fixed on 2026-09-08, surviving in the one directory nobody thought to point the fix at. What stands behind them instead is `npm run verify:gates`, which breaks each gate on purpose and watches it fire: a real proof, and not a number, so no threshold moves when a gate script grows an untested arm. Putting them in scope is wiring and therefore a change spec, not an audit. The four server modules the wider scope revealed — `authRoutes.ts` at 64.9% branches, `auth.ts` 76.9%, `orgRoutes.ts` 82.4%, `notifications.ts` 87.5% — **came out of that list on 2026-09-09**, spec [0055](../changes/0055-four-modules-nobody-had-measured.md), so nothing under `src/` is excluded any more except the bootstrap and the *unreachable* rows. Each is dated and comes out of that list one at a time; none is given a floor at its own score. The numbers move only up, and no audit moves them |
| unit test wraps a rule with `rule()` *(warns)* | **unobserved** | `npm run test:layers` | scoped to the `rule()` wrapper, **not** the bare `@XX-NN` citation — that citation is this repo's binding for the grandfathered test files, and warning on it would fire on four files doing what the bindings tell them to. Silent today: `tests/unit/rule-binding.test.ts` was rewritten to assert through `ruleLabel()` instead |
| absence-only rule not tagged `@refusal` *(warns)* | **unobserved** | `npm run test:layers` | fires only when **every** assertion under a `rule()` block is absence-shaped; a test asserting both presence and absence is ordinary. `@refusal` is now a recognised tag. Silent today — no rule is proved by absence alone |
| feature file past its soft size limits *(warns)* | **automated** | `npm run test:layers` | 120 lines / 6 rules, over all 67 files. Fired on real content the moment it was wired. **Warning again since 2026-09-14, and this row said *silent* for six change specs while it did.** `follow-up.feature` crossed on 2026-09-14 in spec [0075](../changes/0075-the-check-in-that-had-no-okr-words.md) (108 → 151 lines, 5 rules) and `feedback-report.feature` the same day in spec [0074](../changes/0074-the-report-that-could-not-show-you.md) (117 → 125, 5 rules); both have warned on every run through specs 0076–0081, against a two-version norm, and nothing here noticed until the twelfth reading read the gate's output instead of this row. **That is the third time**, and the second under a row that had already been rewritten to be explicit about the second. It was silent from spec 0052, 2026-09-09, which split `room-reactions.feature` — and this row is deliberately explicit about how long it was not: the file crossed both limits in spec 0043's second commit on 2026-09-03 and warned on every run for **nine change specs**, against a two-version norm, while this row said *silent again since 2026-09-02*, the day before. That was the second time a warning outlived the norm under a row claiming quiet — `participant-avatar.feature` did it from 2026-08-31 to 2026-09-02 (142 → 193 lines, 8 rules). Both were split by component in the end, and in both cases the seam was already in `tests/behaviour/`, which is the argument for the limit rather than against it. **Eight** files now sit within eleven lines of it, re-measured 2026-09-16 — `room-music` at 120 (on the limit exactly), `vote-visibility` 117, `export` 116, `live-feed` 114, `room-reactions` 113, `live-rails` 113, `identity-changes` 111, `vote-budget` 110 — and four (`room-music`, `vote-visibility`, `room-reactions`, `vote-budget`) are already **at** the 6-rule cap, so one added rule warns whatever the length. It said **six** and omitted `room-reactions` and `live-rails`, which is the same drift the sentence after it predicts, now on its third instance. Nothing derives that band: the gate prints only what is *past* the limit, so this list is typed and drifts the way the fault count and the markdown total did — it said *five* and omitted `identity-changes` until the tenth reading, wrong from the day it was written. What would end it for good is the gate printing the files nearest the limit, which is wiring |
| boundary rows read by the traceability gate — a rule-bound test doubling a boundary whose row reads *real*, a *fake* row with no suite, a *recorded* row past its age, rule-bound tests with no table at all | **unobserved** | `npm run test:layers` | live over the **16** rows of [*The boundaries*](#the-boundaries) above (12 until spec 0055 added Google's OAuth endpoints; 13 until §18 added the feedback file and GitHub's two), read against the 9 stand-ins the **65** files of `tests/behaviour/` and `tests/workflows/` put up. Wired 2026-09-08 for livespec's [`0039`](https://github.com/sargismarkosyan/livespec/blob/main/specs/changes/0039-the-world-a-test-runs-in.md), released as 1.2.0, and **all four faults were injected and watched to fire** — `boundary-real-is-doubled`, `boundary-fake-with-no-suite`, `boundary-recorded-past-its-age`, `boundary-table-missing`, in [`fault-injection.json`](./fault-injection.json) with the rest. It has run green here and **has not yet refused a real change**, which is what keeps this row *unobserved* rather than *automated*: breaking it against the injection table proves the gate, not that anything in this repository has ever had cause to trip it. **What it does not cover, and this is the important half:** of the two rows reading *real*, only the clock names a stand-in the gate could find, so only the clock can be contradicted. The HTTP + WebSocket row names none — nothing in this language reads as *a double of a real server on a real port* — so that row is a claim no build can refuse, and it is kept honest the way `gates.md` says every *real* row is: it was written after a test reached the thing from here. A hand-written stand-in that none of the five patterns match is invisible to this gate and is `doctor`'s to grep for. Closes the first time a rule-bound test calls `vi.useFakeTimers()`, or a row is flipped to *real* over tests that do not reach it |
| branch protection | **not applicable** | `gh api repos/sargismarkosyan/toil-tracker/branches/main/protection` (**re-read 2026-09-08, after #244**: still `403 · Upgrade to GitHub Pro or make this repository public`, rulesets the same, and the repository is private) | unavailable on this plan — see above. Read back from the platform, not inferred. Rulesets return the same 403, so there is no second place a requirement could be hiding |

**The two standing warnings closed by being fixed.** `export.feature` (162
lines) and `realtime.feature` (179) were past the 120-line soft limit and were
the two oldest feature files, each covering several components. Spec 0009 split
them into four, which is the two-change norm resolving the way it is supposed
to — a warning acted on rather than ignored until nobody reads the output. No
feature file warned then; `participant-avatar.feature` did from 2026-08-31 to
2026-09-02, when it was split by component; `room-reactions.feature` has since
2026-09-03 and still does — see the row.

**The second sitting, 2026-09-08** (`/livespec:setup`, continued). **The coverage
demand went whole** — the row that had been deferred for nine change specs, and
the one the first sitting could not take. The scope stopped being three files.

**What the wider scope found is worth more than the wiring.** The old row said
*roughly two thirds of the codebase* is ungated and never said what it scored.
It scored **47.7% on branches in `client/` — 2,253 uncovered arms**, nine times
`api.ts`'s 256, which is the number this ledger has been worrying about for nine
change specs. And four server modules — `authRoutes.ts` at 64.9%, `auth.ts`
76.9%, `orgRoutes.ts` 82.4%, `notifications.ts` 87.5% — had never been measured
at all, because an `include` list of three files cannot report what it does not
name. None of that was hidden; it was simply never asked, and a paragraph beside
the config was where the answer was supposed to live.

`lib/` and `client/lib/` are now demanded **whole** — 24 files, 100 on all four
measures. That took 60 branch arms covered and **7 that could not be reached at
all deleted from the source**, listed in *What coverage does not cover*. The
seven matter more than the sixty: an unreachable arm and an untested one are
indistinguishable to every gate that reads a file, so a repository that demands
the whole of something has to tell them apart in the source rather than in a
threshold. `client/analytics.ts` — six lines every page imports, both of them
guards — had no test at all and now has one. Everything not demanded is
**excluded by name and dated**, in `vitest.config.ts` where the runner reads it
rather than here; the list shrinks in a diff instead of a number creeping.

**`src/operations.ts` was mutated for the first time, and that is the finding of
the sitting.** It is 1,153 lines at 100% coverage, and it kills **88.57%** of its
mutants with **95 surviving**, against `store.ts`'s 98.14%. Two files, both
demanded whole, both at 100 on every coverage measure, ten points apart on
whether their tests would notice a change — and nothing in this repository could
tell them apart until it was run. **It is measured and not wired**: with
`break: 96` the aggregate of 91.83% makes `npm run test:mutation` red on every
run, and the two ways to green are killing 95 mutants or lowering a threshold,
which `CLAUDE.md` forbids outright. The number is on the record instead, under
*Mutation testing*, and `operations.ts` joins `mutate` in the change that kills
them. That correction is worth stating plainly: adding it to the config was
recommended earlier in this session and was wrong as wiring, right as a
measurement.

**And the sitting's own run found a real bug in a test.**
`tests/unit/operations.test.ts`'s `@SW-03` case built a session started
`Date.now() - 20 * 60_000` ago and expected `ceil(20) + 5 = 25`. Exactly twenty
minutes is the boundary: the moment any measurable time passes between
constructing that `Date` and calling `extendSession`, elapsed is 20.0001, `ceil`
gives 21, and the answer is 26. It passed for as long as those two statements ran
inside the same millisecond, and it failed the first time the machine was busy —
a full instrumented run of 102 files. Fixed to 20.5 minutes, which is stable in
both directions. **That is the second time-dependent failure this session**, after
`@RN-05`'s socket timeout under the same load, and the pair of them is the
argument for the flakiness gap that has no row: 35 files wait on real socket
events, nothing distinguishes a flake from a regression except re-running, and
*every commit green* is the rule they sit under.

**The stamp does not move again** — the first sitting already brought it to
1.3.0, and this is the same sitting's second half. Nothing is left for `setup`:
the ledger's coverage row reads *automated* with its exclusions named, and what
remains is ordinary work with an address — 95 mutants, 2,207 branch arms under
`client/pages`, four server modules, and one ratchet on `api.ts`.

**The sitting after it, 2026-09-08** (`/livespec:setup`, on the tenth reading's
own branch). **The boundaries table is wired**, which is the first time in ten
readings that anything in this ledger's wiring has moved — so the stamp moves
with it, from 0.25.0 to **1.3.0**, and it is moving because the wiring came
level rather than because somebody looked.

What landed: [*The boundaries*](#the-boundaries) above, twelve rows — 2 *real*,
7 *mocked*, 3 *unreachable*; the stand-in patterns beside it as a binding;
`scripts/check-spec-layers.mjs` reading both and failing on the four faults
`gates.md` names; those four in `scripts/inject-faults.mjs` and in
[`fault-injection.json`](./fault-injection.json); and the rules line in
`CLAUDE.md` that `claude-md.md` requirement 7 asks for, which the ninth reading
held back precisely until there was a table for it to point at. No new command:
the check rides on `npm run test:layers`, so `verify:fast`, the pre-push hook
and CI all gained it without being told.

**Three decisions in the pattern list, and each one is a trap somebody would
otherwise walk into.** `vi.fn()` is out — eight files pass one as a prop
callback and cross nothing, and the eighth reading's *16 files* was that mistake
already made once on paper. `vi.spyOn` is in, and it paid immediately: it found
`room-reactions-motion.test.tsx` importing the real `socket` and replacing
`emit`, a ninth stand-in and a fifth file on the client-socket boundary, which
three readings had missed because they looked only for `vi.mock` and
`vi.stubGlobal`. And `console` gets no row on purpose — the gate finds the spy
in `follow-up.test.tsx`, matches it to nothing, and stays silent, which is how
a stand-in with no row is meant to behave.

**The row reads *unobserved*, not *automated*, and the honest part is what it
does not cover.** All four faults were injected and watched to fire; none of
them is a change anybody made. Of the two *real* rows, only the clock names a
stand-in the gate can find, so a rule-bound `vi.useFakeTimers()` fails from
today and the HTTP + WebSocket row is a claim no build can refuse.

**One row is still `setup`'s and did not move.** The coverage demand is nine
change specs past its clock, and closing it is not a sitting: `api.ts` holds 256
uncovered branch arms of 1,200, and there is no exclusion that names them —
istanbul excludes files, and they are scattered through one 2,982-line file that
is the business logic. So it stays *deferred*, with the two ways out unchanged
and neither of them a table: cover them in slices and raise the floor each time,
or write the row off as *not applicable* with the reason in it. That second one
is a decision, and it is not the audit's to take.

/livespec:setup
- coverage thresholds — name `client/` and `lib/` as exclusions in `vitest.config.ts`, each with its reason, and demand the whole of what remains, ending the `api.ts` ratchet (deferred since spec 0042, nine change specs, past its clock)

**Twelfth reading, 2026-09-16** (`/livespec:doctor`, on `3cd5b19`, after specs
0059–0081) — **the first reading here taken through the audit tool**, `tools/doctor.py`,
which arrived in livespec 1.5.0 and did not exist when any row below was written.
Forty checks, twenty-five of them answered by the script.

**The tool could read no stamp at all**, and that one fact took ten checks to
*n/a* with it. The line above says *Reconciled against livespec 1.3.0 (`method/`)
on 2026-09-08* and the tool reads `Reconciled against livespec <version> on
<date>` — the parenthesis is enough. The three ledger tables are in the same
position: written before the template had headers, so `check:ledger-shape` reads
*pre-template*, one row matches an id by alias, and every row here carries a
label where the method now expects a `gate:` id. Nothing is missing; everything
is unaddressable. **That is a reshape, and a reshape is `setup`'s** — this
reading does not move a column.

**Nothing in the range asks for wiring.** Between the stamp's 1.3.0 and the
1.7.0 installed, `gates.md` gained **the id table itself** and the repository
gained a tool to read it; no `gate:` id was added or removed, and
`method/claude-md.md` was not touched. So no row below is missing a gate. Every
row below is missing its id.

**What the tree contradicted — five counts and one silence.** 53 feature files
where there are 67, and 35 naming both workflows where there are 49; 13 boundary
rows where the gate reads 16; 47 rule-bound test files where it reads 65; *105
rules* in the present tense where there are 369; and the rule-bound measure last
taken at spec 0051. All corrected above. The silence is the one that matters:
the soft-limit row read **Silent since spec 0052** while `follow-up.feature` and
`feedback-report.feature` had both been warning on every run since 2026-09-14 —
six change specs under a two-version norm, **the third time a warning has
outlived the norm under a row claiming quiet**, and the second under a row
already rewritten to be explicit about the second. The typed band drifted with
it: six files named where eight are in it. Both are the same defect, and the row
already names the wiring that would end it.

**The finding that was not a count: `scripts/` is gated by nothing.** Fifteen
`.mjs` files and 3,386 lines — `check-spec-layers.mjs` and `check-spec-features.mjs`
among them, which *are* two of the gates in the table below — sit outside the
coverage `include` rather than inside the `exclude`, so they are out by absence
from a list, which is the precise shape the section above says was fixed on
2026-09-08. The fix was pointed at `client/` and `lib/` and never at the
directory the fix itself lives in. They are not unproven — `npm run verify:gates`
breaks each gate and watches it fire — but no threshold moves when one of them
grows an untested arm. The coverage row now says so. Bringing them into scope is
wiring, so it is a change spec and not this reading's.

**And the gap widened for the first time.** Gated went 92.54 → **100** across all
four measures while rule-bound went 78.61 → **79.17**: specs 0077–0081 covered
the client pages with component tests that name no rule. A seventh of the covered
logic answered to no written rule on 2026-09-08; a fifth does now. That is the
unit-test exemption working as written, and it is also the first reading that has
had to write the number down going the other way.

**Read back from the platform, 2026-09-16.** `gh api …/branches/main/protection`
→ 403, *Upgrade to GitHub Pro or make this repository public*; `…/rulesets` →
the same 403, which no earlier reading had asked for. One collaborator,
`sargismarkosyan`, push and admin. The check is `Test & Coverage` on the platform
as it is here. Nothing to correct: the rows already claim no protection, and the
protection is still unavailable.

**No wiring moved, so livespec 1.3.0 is not re-stamped.** What is left for the
sitting is the shape, not a gate.

**Eleventh reading, 2026-09-09** (`/livespec:doctor`, on `55dc5fb`, after specs
0052–0058). **The stamp and the plugin agree — both 1.3.0 — so there was no
changelog range to read**, and the whole reading was the tree against the rows.
Every count in the ledger holds: 53 feature files, 283 scenarios, 45 behaviour
files, 199 `rule()` blocks, 2 workflows, 1 persona, 1 journey, 13 boundary rows
against 9 stand-ins in 47 rule-bound files — the last of which the layers gate
now prints, so it can no longer drift the way the totals corrected below did.
The soft-limit band was re-measured and is exact, all six files and the three at
the rule cap. Branch protection was re-read from the platform: still `403 ·
Upgrade to GitHub Pro`, rulesets the same, repository private. `verify:gates
--check` ran all 26 faults and each fired as recorded. The HTTP + WebSocket
*real* row was read back rather than believed — `tests/workflows/` starts
Express and Socket.io on an OS-assigned port and four walkthroughs pass from
here — and the tree was grepped for a hand-written stand-in none of the five
patterns match, which is this skill's half of that row: there is none.

**The finding is not in either table.** Three checks in `verify:fast` — the
linter, the copy gate and the quarantine clock — run in no pipeline at all,
because `ci.yml` lists its steps by hand rather than running `npm run ci`.
Recorded under *The local pre-push hook is not a gate*, where the hook's own
claim not to be a second copy is what turned out to be true of the hook and
false of CI. None of the three is a gate the method names, so none becomes a
row. Filed as
[#263](https://github.com/sargismarkosyan/toil-tracker/issues/263).

**And eight rows are past a clock nobody had counted.** Every *mocked* boundary
row is past its two-change norm — seven of them by seven change specs. The
record now says so; the three ways out are the person's to choose. Filed as
[#264](https://github.com/sargismarkosyan/toil-tracker/issues/264).

Five more corrections, all to typed totals and dates that the files beside them
already own: a header announcing a *deferred* row that specs 0054–0055 closed, a
`Known gaps` paragraph still asserting the ratchet in the present tense, a fault
record dated 2026-08-31 against a JSON that says 2026-09-09, *ten* boundary rows
where the gate prints eleven, and *the only* `vi.useFakeTimers()` where there
are two files. **No wiring moved, so livespec 1.3.0 is not re-stamped** — the
stamp follows the wiring, and nothing here is left for a sitting.

**Tenth reading, 2026-09-08** (`/livespec:doctor`, on `a10d6cc` — the ninth
reading's own commit, with nothing shipped between; the feature tree, the tests
and `vitest.config.ts` are byte-identical to `edf7e9b`). What moved is again on
the plugin's side and only there: the manifest now reads **1.3.0**, so the range
is 0.26.0 → 1.3.0, one entry longer than the ninth reading's. The new entry moved
`doctor` §4 and its refusals — an audit that leaves wiring to be built now ends
with the command that starts the sitting, as somebody would type it, followed by
the rows that sitting will be asked to wire. **It asks nothing of this
repository's wiring; it asks something of this record**, and the last line of
this paragraph is where that lands. The ninth reading's own close — *two things
are still `setup`'s* — is the exact shape 1.3.0 names as the failure, and it is
left as written: it met the rule that governed it, and a record edited to agree
with the present is not a record.

Everything else in the range was settled by the seventh, eighth and ninth
readings and was re-checked rather than re-derived: step 2 names `todo`, step 4
names the sketch, the sketch row is in the table, the coverage row reads
*deferred*, and the boundary row is written. Every skill name the record
instructs by — three in `CLAUDE.md`, four in `specs/README.md`, one here —
resolves against the eight this plugin has. `CLAUDE.md` still owes the rules line
`claude-md.md` requirement 7 now names, and it still lands with the table rather
than before it.

Read back rather than assumed: branch protection and rulesets, both still `403 ·
Upgrade to GitHub Pro`, the repository still private, so the *not applicable* row
holds. The last hundred runs are now **100 green with none in progress** — the
`push` of `edf7e9b` that the ninth reading had to leave unfinished came back
green, and #159's red has rolled out of the window. Nothing has merged since
#244, so no *unobserved* row closes. `test:features` (52 files, 283 scenarios),
`test:layers` (52 features, 2 workflows, 1 persona, 1 journey, and the one
standing `room-reactions.feature` warning), `verify:gates -- --check` over the
whole injector, `test:coverage` and `test:coverage:rule-bound` were all run here.
`api.ts` is unchanged at 89.48 / 78.66 / 99.06 / 98.19 against a floor of 89.03 /
77.94 / 99.04 / 97.88, with **256 uncovered branch arms of 1,200** where the
config's dated comment says 255 of 1,156 — the ninth reading's finding, re-read
off the instrumented run rather than carried forward, and unmoved because the
tree is. The rule-bound measure still reads 66 of 100 files at 78.61 / 74.44 /
84.55 / 85.07. The ninth reading's boundary inventory was re-measured from the
sources for the same reason — a corrected count is still a typed one — and every
figure of it holds: **8** of the 45 files in `tests/behaviour/` double a module or
a global, `react-router-dom` in 6, `lib/socket` in 4, `fetch` in 4, `localStorage`
in 7, `AuthContext` in 1, and 21 run under jsdom. **It holds for the two patterns
it was measured with, and the sitting that followed widened them.** `vi.spyOn` is
a stand-in too, and `room-reactions-motion.test.tsx` imports the real `socket` and
replaces `emit` — a ninth file, and a fifth standing in for the client socket,
that no inventory taken with `vi.mock` and `vi.stubGlobal` alone could see. Three
readings measured this list; none of them looked for that shape.

**The first instrumented run went red and the second did not.**
`tests/behaviour/room-reactions.test.ts` (`@RN-05`) timed out waiting for the
`room:reaction` socket event inside the full 1,630-test run, then passed alone in
2.9 s and passed again on a clean re-run of the whole suite. That is a flaky test
rather than any gate having an opinion — the distinction #159 forced into this
file, arriving this time as nondeterminism instead of a real assertion — so no
row moves and nothing closes. It is not a ledger matter, and it is worth an
issue.

**Two corrections, both to typed lists, and both wrong before the ninth reading
rather than because of it.** The fault table said the boundary faults shipped as
*1.2.0, the version now installed*: a present-tense claim about a thing that
moves without this file being touched, and one plugin update falsified it. It is
dated to the release now. The soft-limit row said *five more files sit within
eleven lines of the limit* and listed five; there are **six**, and
`identity-changes.feature` at 110 lines was never in it — that file has not
changed since spec 0021 (#180), so the band was wrong on the day it was typed and
three readings read past it. Three of the six are also **at** the 6-rule cap, so
length is not the only way they warn. Nothing derives that band — the gate prints
only what is *past* the limit — which is why it drifts the way the fault count
and the markdown total did, and why the thing that would end it is the gate
printing what is nearest, which is wiring rather than a row.

**No wiring moved in the reading, so it left the stamp at 0.25.0** — four
readings have now done that, which is the price of a stamp that means what it
says. **That sentence is this reading's account and not this file's stamp**,
which is at the top and reads 1.3.0: the sitting recorded above followed the
same day and moved it. Both are true of the moment they describe, and this is
the one place in this file where they sit ten lines apart — so the second row
below is struck rather than deleted, because a hand-over nobody can see was
taken up is the dangling instruction this whole check exists to catch.

/livespec:setup
- coverage thresholds — name `client/` and `lib/` as exclusions in `vitest.config.ts`, each with its reason, and demand the whole of what remains, ending the `api.ts` ratchet (deferred since spec 0042, nine change specs, past its clock) — **still open**
- ~~the boundaries table in these bindings, the traceability gate reading it, the four boundary faults in `scripts/inject-faults.mjs`, and the `CLAUDE.md` rules line that lands with them~~ — **taken up by the sitting above, 2026-09-08**, and the ledger row now reads *unobserved*

**Ninth reading, 2026-09-08** (`/livespec:doctor`, same day, on `edf7e9b` — the
eighth reading's own commit, with nothing shipped between). What moved is on the
plugin's side: the manifest now reads **1.2.0**, and the change the eighth
reading had to describe from an unreleased checkout has shipped with a changelog
entry. So the range is 0.26.0 → 1.2.0, one entry longer, and the new one is the
boundaries table — already written into this ledger as a *deferred* row, which is
what its entry says an audit should do. Its one ask beyond the wiring is a rules
line in `CLAUDE.md` (`claude-md.md` requirement 7), and that is named in the
boundary row rather than added now: a rule sending sessions to a table that does
not exist is the failure step 2 already had once, and it lands with the table.
Everything else in the range was settled by the seventh and eighth readings and
was re-checked, not re-derived: step 2 names `todo`, step 4 names the sketch, the
sketch row is in the table, the coverage row reads *deferred*. Every skill name
the record instructs by — three in `CLAUDE.md`, four in `specs/README.md`, one
here — resolves against the eight this plugin now has.

Read back rather than assumed: branch protection and rulesets, still `403 ·
Upgrade to GitHub Pro`, still private, so the *not applicable* row holds; the
last hundred runs, 99 green and one still in progress — the `push` of `edf7e9b`
itself, which the eighth reading could not have seen finish either. `test:features`
(52 files, 283 scenarios), `test:layers` (2 workflows, 1 persona, 1 journey, and
the one standing `room-reactions.feature` warning), `verify:gates -- --check` over
the whole injector, `test:coverage` and `test:coverage:rule-bound` were all run
here: green, and the rule-bound measure still reads 66 of 100 files at 78.61 /
74.44 / 84.55 / 85.07. No *unobserved* row closed — nothing has been merged since
#244 to close one.

**And 1.2.0 read all the way through, rather than for the ledger alone.** Its
entry points at seven places and the diff carries them: `setup` §2 now asks a
**sixth** interview question — what does this talk to, and which of those can a
test reach for real from here — §4 gained *Then make the real thing reachable,
before the gate that assumes it*, which says to wire the real thing and run one
test through it **before** any row claims *real*, and that the suite may gain
tooling while the app gains none; §5 gained the third table. The double-detection
patterns become a **binding** here, beside the discovery pattern. `templates/feature.feature`
renamed its `Example: <the boundary>` to `<the edge>` to free the word — this
repository uses *boundary* only as ordinary prose (`card-bucket`, `session-payload`,
§17, §12), never as a Gherkin example name, so that rename asks nothing here.
livespec's own bindings gained a worked instance of the table, and kept its stamp
at 1.1.0 through `0039` because no gate there gained a check — **the opposite is
true here**: this repository has 47 rule-bound test files for a gate to read, so
wiring the table *will* move this stamp when `setup` does it.

**Two things this reading found that the eighth did not.** The first is in the
coverage row: reading the branch arms out of the instrumented run rather than the
percentages out of the summary. `api.ts` is at 256 uncovered arms of 1,200, where
the config's own dated comment says 255 of 1,156 after spec 0043. The floor being
0.72 branch points below the score was already recorded; what was not is that the
absolute count went *up* by one over those eight change specs. The percentage
improved because 44 arms were added and 43 of them covered — so the measure the
floor is written in has been moving in the opposite direction to the thing the
floor exists to shrink, and neither number can fail a build.

The second is in the boundary row's own inventory, re-read against the sources
because `setup` will write the table *from* it. It was wrong in both directions:
*fake timers in 1* names no rule-bound test — the tree's only `useFakeTimers` is
a unit test, which is the exemption working — and `localStorage`, doubled in 7
files and the most-doubled thing in the suite, was not in the list at all. The
*16 files* counted eight whose only stand-in is a `vi.fn()` prop callback, which
crosses no boundary; the real figure is 8. That is not bookkeeping: the pattern
list the gate will read is a binding, and `vi.fn` in it fails eight innocent
files while a missing `localStorage` row leaves a real boundary with nothing to
contradict. **No wiring moved, so the stamp stays at 0.25.0** — three readings now have left it there, which is
the price of a stamp that means what it says. Two things are still `setup`'s: the
coverage demand, nine change specs past its clock, and the boundaries table.

**Eighth reading, 2026-09-08** (`/livespec:doctor`, after #244). The stamp still
says 0.25.0 and the manifest installed says 1.1.0, so the same seven entries were
read again and the seventh reading's corrections all hold — step 2 names `todo`,
step 4 names the sketch, the sketch row is in the table, the coverage row reads
*deferred*. The one entry new since, 1.1.0, moved the audit itself and asks
nothing of this repository's wiring. **What the manifest does not say**: the
installed copy is the checkout at livespec's `0039`, two commits past 1.1.0,
unreleased and with no changelog entry — and `gates.md` as it now stands carries
that change, a boundaries table read by the traceability gate. This ledger has
none, and the row for it is written *deferred* above, with what the rule-bound
tests were found to double. Beyond the range, the record had drifted nine change
specs in six days: 40 feature files and 227 scenarios where there are 52 and
283, 33 behaviour files and 141 `rule()` blocks where there are 45 and 199, 26
features naming both workflows where there are 34, 55 of 90 test files naming a
rule where the report on #244 says 66 of 100 — all corrected from the gates and
the report. Two rows said something the tree contradicts. The soft-limit row
said *silent again since 2026-09-02*; `room-reactions.feature` has warned since
the next day, eight change specs, past the two-version norm for the second time.
The coverage row said the `api.ts` floor is *raised as each slice lands*;
`vitest.config.ts` was opened and no slice has landed since 0043, while the
instrumented run puts the score 0.45 / 0.72 / 0.02 / 0.31 above it — a ratchet
with slack, and a deferral nine changes old, which is past its clock. Branch
protection and rulesets re-read: `403`, private. Run history re-read: none red in
the last hundred, and no *unobserved* row closes across the twelve pull requests
since #212. The report and the rule-bound measure were both read on #244.
`test:features`, `test:layers`, `verify:gates -- --check` and `test:coverage`
all green. **No wiring moved and the stamp stays at 0.25.0.** Two things are
`setup`'s: the coverage demand, now past its clock, and the boundaries table.

**Seventh reading, 2026-09-02** (`/livespec:doctor`, the first here to read the
other side of the difference). The stamp says 0.25.0; the plugin installed is
1.0.0, and its changelog has seven entries between. Read as where to look, not
what to do: 0.26.0 is a floor on the plugin's own eval board and asks nothing of
a repository with an ordinary test suite; 0.27.0 moved what the loop's approval
step says, and `CLAUDE.md` step 4 here still read *Human approves, or asks for
changes* — corrected; 0.28.0 and 0.30.0 stopped permitting a demand read off a
report and set the figure, which is the ratchet *Known gaps* already names — the
coverage row now reads *deferred* with the version that moved it, and the number
is untouched; 0.29.0 added the sketch row to the bindings, absent here — added,
with the fence that keeps the picture's exemption off it; 0.31.0 is the `doctor`
pass that paragraph named as what would end it, and it has arrived; 1.0.0
renamed the feedback skill to `todo`, and step 2 sent every session to a skill that no
longer exists — corrected. Nothing else in the range reaches this repository.
Beyond the range: the counts in the table were spec 0011's and the tree is at
0042 — 40 feature files, 227 scenarios, 33 behaviour files with 141 `rule()`
blocks, 53 of 88 test files naming a rule — all read from the gates and the last
report rather than typed; and the soft-limit row said *silent today* while
`participant-avatar.feature` has been warning since 2026-08-31, past the
two-version norm. Branch protection re-read: still `403`, still private,
rulesets the same. One red in the last hundred runs, #159's, already recorded;
nothing has refused anything since #160 either, across 33 merged pull requests,
so no *unobserved* row closes. `verify:gates -- --check` green. **No wiring moved
and the stamp stays at 0.25.0** — it follows the wiring, and the one thing the
method now asks of this repository's wiring is the coverage demand, which is
`setup`'s to rewire.

**Sixth reading, after #160** (`/livespec:doctor`). The ledger's own counts were
right this time — #160 had just re-read them — and the drift had moved into the
newest prose instead. The cross-link entry written during #157 said the gate
reads **sixty** markdown files; spec 0011's change spec had already made it
sixty-one, so a hardcoded total went stale within one change spec of being
typed. It is deleted rather than corrected, on the same reasoning this file
already applies to the fault count: the gate prints today's number on every run,
and a total nobody derives can only go stale. *Every layer README and all ten
change specs* went the same way, for the same reason.

Everything else held. Branch protection and the run history were read back from
GitHub (still `403`, still private; one red build in the last forty, the one
already recorded). The fault injector ran `--check` green over eighteen faults,
and the coverage verifier still refused a module under its thresholds. No row
reads *deferred*, so nothing is on the two-change clock; seven rows are still
*unobserved* and each names what would close it. **No wiring moved and livespec
is still 0.25.0, so the stamp is not touched.**

**Fifth reading, after #159** (`/livespec:doctor` follow-up). Recorded the two
things #159 proved rather than argued: the pull-request report was watched on a
**red** build for the first time, closing the half of its row that had been open
since it was wired; and the pipeline under this wiring went red once without any
gate in the table refusing anything — the failure was a test assertion in the
step that also carries the coverage gate. Those are different events and the
ledger now says so, because a reader counting red builds as refusals would close
rows nothing has closed. Counts re-read after spec 0011: 16 feature files where
the table said 15, 105 scenarios where it said 101, `tests/behaviour/` at 4 files
and 18 `rule()` blocks where it said 3 and 14, and the rule-bound measure at 22
of 59 test files where it said 21 of 57. No wiring moved, and livespec 0.25.0 is
not re-stamped.

**Fourth reading, after #156** (`/livespec:doctor`). The third reading had been
taken three changes earlier, and two of its own numbers were wrong when it typed
them: `tests/behaviour/` was recorded as 16 `rule()` blocks against 14 in the
tree at that very commit, and *six* change specs since the wiring against seven.
The larger correction is the paragraph above the table, which asserted the
pipeline had **never gone red** — read back from the platform, it has, once, on
2026-07-26, a month before this wiring existed. That claim was never checked
against `gh run list`; it was written from a memory of recent PRs. The gap that
had never been a row was the cross-link gate's reach: it read `SPEC.md` plus
`specs/*.md` and no deeper, leaving seventeen files unchecked including this one,
which is why a dangling link in it had been sitting green. That one was **fixed
in the same sitting rather than left as a finding** — see *Known gaps* — so the
gate now reads 60 files and refused that link on its first run. Branch protection and
the whole run history were read back from GitHub; the fault injector, the
coverage gate and the corpus-freshness check were each watched to fire in the
session. **No wiring moved, so livespec 0.25.0 is not re-stamped.**

**Third reading, after spec 0010** (`/livespec:doctor`). Six change specs had
shipped since the second reading and the ledger's counts had all drifted: 8
feature files where there are 15, 60 scenarios where there are 101, one
behaviour file where there are three, and *every feature names both workflows*
where five now name one. The soft-limit row still announced two warnings that
spec 0009 had fixed. The coverage thresholds in the top table were still the
setup values, stale since the spec 0004 ratchet; the rule-bound measure was six
specs old. The fault transcript printed in this file listed 14 faults against
the injector's 18 — the copy is not what `--check` compares, so it drifted in
silence, and it is deleted rather than refreshed. Branch protection was read
back from the platform again, and the §14 corpus was found to be describing
prompts that have since been rewritten. No wiring moved, and the livespec
version above is not re-stamped.

**Audited twice on 2026-08-30** (`/livespec:doctor`). The second reading added
three rows for gates the method names and this ledger had never listed at all —
all three warnings, none implemented, now on the two-change clock. It also
deleted a typed fault count that had already gone stale, and read branch
protection back from the platform again. No wiring moved, so the livespec version
above is not re-stamped.

**First reading, after spec 0004.** Six rows were
corrected against the tree: two carried stale counts (7 files / 52 scenarios),
two still said `tests/behaviour/` was empty, and the rule-bound coverage measure
is past its two-change clock. Branch protection was re-read from the platform,
not assumed. Nothing was wired — `doctor` corrects the record and never the
wiring.

**Why so many rows read *unobserved*, and what that does *not* mean any more.**
Every one of them was broken on purpose and watched to fail (see the fault table
below). That proved the gate's logic — and, until 2026-08-31, only that. **The
injector points each gate at a disposable copy through `SPEC_ROOT`**, so a green
fault run said the rule was implemented correctly and said nothing whatever
about whether the gate is aimed at this repository's own `specs/` and `tests/`.
Those are different claims, and the paragraph that used to stand here conflated
them: it argued from *nothing has had cause to fire* when the sharper doubt was
*we have never seen one fire here at all*.

**So all seven were run against the real tree, without `SPEC_ROOT`, and all
seven fire.** A stray `it()` at the top level of a behaviour file, a behaviour
file with no `rule()`, a `@pending` tag added back to a scenario that has a
test, an orphaned persona, a journey naming a workflow that does not exist — each
one exits 1 and names the offence. The two warn-level checks print and exit 0,
as they should. Every probe was reverted and the tree was confirmed clean.

What remains behind these rows is therefore **one** thing, not two: nobody has
yet made the mistake. The wiring is no longer in question. A row closes when a
real change trips it — not when somebody probes it — so a probe is evidence
about the gate and never a reason to re-letter the row. Re-read them with
`/livespec:doctor` rather than by reconstructing this sitting.

**One of them cannot close.** `journey → workflow` passes vacuously because the
single journey names no workflow at all; there is nothing for it to get wrong
until one does. It is a safety net, correctly, and an audit that keeps flagging
it is miscounting.

The two rows reading *automated* earned it: `test:features` has been refusing
things throughout this sitting (it caught the negative fixtures in
`tests/unit/rule-binding.test.ts`), and the coverage gate refused an impossible
threshold under `verify:gates:coverage`.

### The wiring that must never gate

Same four states. Neither of these can fail a build, which is exactly why both go
missing quietly.

| Wiring | State | Notes |
|---|---|---|
| the pull-request report | **automated** | `scripts/pr-report.mjs`, wired as the `Spec-layer report` step. Runs on `always()` so it describes a red build too; `continue-on-error` plus an unconditional `exit 0`. **Watched one arrive on [PR #138](https://github.com/sargismarkosyan/toil-tracker/pull/138)**, carrying the generated map, and on every PR since, through [#244](https://github.com/sargismarkosyan/toil-tracker/pull/244) on 2026-09-08 (*Rules 283 **+5***, *Feature files 52 **+1***, and the one layers warning named). [#151](https://github.com/sargismarkosyan/toil-tracker/pull/151) reported *Rules 101 **+5***, *Feature files 15 **+1***, which is the delta doing its job; #154–#156 touched no spec layer and showed no delta at all, which is the same mechanism reporting honestly that nothing moved. **And now watched on a red build**, which is the half it exists for — see below |
| the rule-bound coverage measure | **automated** | `npm run test:coverage:rule-bound` → `scripts/coverage-rule-bound.mjs`, reported by the `Rule-bound coverage` step and printed beside the gated number in the PR report. Zero thresholds inside plus `continue-on-error`: it cannot fail a build. **Not** `tests/behaviour/` + `tests/workflows/` — see below. **Watched it arrive on [PR #143](https://github.com/sargismarkosyan/toil-tracker/pull/143)**, printed beside the gated number, and on every PR since, through #244 on 2026-09-08 |

**The report has now been read on a failing build.**
[#159](https://github.com/sargismarkosyan/toil-tracker/pull/159)'s first run went
red at 20:28 on 2026-08-30 and the report arrived at 20:31:06, inside that run,
carrying the counts and the map as usual. It reported *Traceability gate: green*,
which was true — the gate it speaks for **was** green, and the failure was a test
assertion two steps earlier.

That is the whole design working where it is hardest to check: `if: always()`
plus `continue-on-error` meant the run whose state most needed explaining still
explained itself, and the report said *which* failure happened without offering
an opinion on whether it counted. This row had said *still not seen on a red
build* since it was wired, and it took eight change specs to get one.

A row deferred across two changes is either wired or written off.

### The boundaries

The two tables above say what refuses a change. This one says **what world the
tests that pass those gates ran in** — because both gates are satisfied by a
test that names its rule, reaches every line, and talks to a stand-in for
everything outside itself. Nothing else in this file can tell.

**Read over `tests/behaviour/` and `tests/workflows/` only** — 65 files. The
Google row is the exception a table like this eventually gets: its stand-in is
in `tests/integration/`, which the gate does not read, and the row is here
anyway because `vi.stubGlobal('fetch', …)` crosses the same line wherever it is
written. A boundary the gate cannot see is still a boundary.

 A unit
test doubling everything is what unit tests are for, and the grandfathered
suites in `tests/unit/`, `tests/integration/` and `tests/component/` are unit
tests as far as livespec is concerned until a rule answers to them.

**What counts as a stand-in here** — the binding the gate reads, beside the
`@XX-NN` discovery pattern above:

| Written as | Stands in for |
|---|---|
| `vi.mock('…')` · `vi.doMock('…')` | the module named |
| `vi.stubGlobal('…')` | the global named |
| `vi.spyOn(obj, …)` | `obj`, whether or not the module around it is real |
| `vi.useFakeTimers()` | the clock |
| `// @vitest-environment jsdom` | the browser |

**`vi.fn()` is deliberately not in that list**, and it is the one somebody will
add. A bare `vi.fn()` passed as a prop callback — `onFocusId={vi.fn()}` —
doubles nothing this app talks to, and eight files in `tests/behaviour/` do
exactly that. The eighth reading of this ledger counted them as boundary
doubles and reported *16 files* where there are 8; putting `vi.fn` in the list
would have failed those eight for crossing nothing.

**`vi.spyOn` is in it, and it is the one that earns its place.** A test can
import the real module and replace one method on it, which reads nothing like
`vi.mock` and stands in just as completely — `room-reactions-motion.test.tsx`
imports the real `socket` and replaces `emit`, and no inventory taken with
`vi.mock` and `vi.stubGlobal` alone could see it. That file is the fifth
standing in for the client socket, against the four the ninth reading found.

**`console` gets no row.** It is where this process writes, not something the
app talks to, and a row for it would be a boundary nobody can cross. The gate
finds the spy in `follow-up.test.tsx`, matches it to no row, and says nothing —
which is the design: a stand-in with no row is `doctor`'s to grep for, and only
a row reading *real* can fail a build.

| Boundary | State | Stood in for by | What reaches it here | What it leaves uncovered | Since |
|---|---|---|---|---|---|
| the session store — Postgres via Prisma, `src/db.ts` | **unreachable** | — | nothing. `DATABASE_URL` is unset for every test, which makes `src/db.ts` a no-op by its own design, and the suite runs the in-memory `SessionsMap` that `src/store.ts` and `tests/helpers/testServer.ts` build — the app's own code, not a stand-in | the whole write-through cache: `persistSession`, `loadAllSessions`, the JSONB column shape, every migration, and what happens when the database is unreachable at startup | predates the ledger |
| the HTTP + WebSocket API this app serves | **real** | — | `tests/helpers/testServer.ts` starts Express and Socket.io on an OS-assigned port; all of `tests/integration/` and both walkthroughs in `tests/workflows/` go over real TCP with real `socket.io-client` connections | `src/server.ts` itself — the test server mirrors its wiring rather than running it. One process, one machine, no proxy and no TLS, at test volume rather than a full room | 2026-09-08 |
| the browser | **mocked** | `jsdom` | jsdom, in 21 of the 45 files in `tests/behaviour/` and throughout `tests/component/` | layout, paint, focus order, media playback, and every engine that is not jsdom. Each version's clip is driven through real Chrome by `/livespec:record-clip` — watched by a person, checked by no suite | 2026-09-08 |
| the browser's URL and history | **mocked** | `react-router-dom` | a stand-in in 6 rule-bound files, which assert the path they would have been sent to | real navigation, the back button, a reload, and a deep link opened cold | 2026-09-08 |
| the browser's local storage | **mocked** | `localStorage` | `vi.stubGlobal('localStorage', …)` in 7 rule-bound files — the most-doubled thing in this suite | quota, eviction, cross-tab `storage` events, and a real profile arriving with keys already in it | 2026-09-08 |
| this app's HTTP endpoints, as the client calls them | **mocked** | `fetch` | `vi.stubGlobal('fetch', …)` in 4 rule-bound files, asserting the request bodies the screen produces | that the endpoint answers that way. The other side of the same path is *real* above, over supertest in `tests/integration/` — the two are never checked against each other, which is what would make this row *fake* | 2026-09-08 |
| this app's socket events, as the client sends and receives them | **mocked** | `lib/socket` · `socket` | `vi.mock('../../lib/socket')` in 4 rule-bound files, and `vi.spyOn(socket, 'emit')` on the real module in a 5th | that the server emits what the stand-in replays. The real path is covered on the other side by `tests/integration/` and both walkthroughs | 2026-09-08 |
| the signed-in identity | **mocked** | `AuthContext` | a stand-in for the React context in 1 rule-bound file. The server half is real — bcrypt, JWT and cookies, exercised in `tests/integration/` against the real routes | the client's sign-in, refresh and expiry paths, and every identity provider that is not this app | 2026-09-08 |
| audio output | **mocked** | `HTMLMediaElement` | `vi.spyOn(HTMLMediaElement.prototype, …)` in `room-music.test.tsx`, asserting that play and pause were asked for | whether anything is audible, autoplay policy, and what a second tab does to it | 2026-09-08 |
| the clock | **real** | `the clock` | nothing fakes it. **Two** files call `vi.useFakeTimers()` — `tests/unit/ai-writing.test.ts` and `tests/unit/ai-grouping.test.ts`, neither of which claims a rule — which is the unit exemption working as intended; this row said *the only* one until the eleventh reading counted them, and it is the sentence that keeps a *real* row honest where the gate can only see the rule-bound suite; the throttle and window tests in `tests/behaviour/` wait on the real one | that a slow machine is a different clock: these tests wait on real milliseconds and are the suite's flakiest part | 2026-09-08 |
| Google's OAuth endpoints — `oauth2.googleapis.com/token`, `www.googleapis.com/oauth2/v2/userinfo` | **mocked** | `fetch` | `vi.stubGlobal('fetch', …)` in `tests/integration/18-google-oauth.test.ts`, answering with a token and a profile. Everything on this side of the line is real: the state cookie, the code the callback is handed, the link flow, the account it finds or creates, the JWT it issues, and all five refusals | whether Google answers in that shape at all — if either response changes, these tests keep passing and sign-in breaks. Also the consent screen, the scopes a user actually grants, and every path that never reaches this server | 2026-09-09 |
| outbound email — Resend, `src/email.ts` | **unreachable** | — | nothing. With `RESEND_API_KEY` unset the module logs instead of sending, which is the app's own branch and is what every test exercises | whether Resend accepts the payload, renders the HTML, or delivers it | predates the ledger |
| the feedback file — `reports/feedback.jsonl`, `src/feedback-file.ts` | **real** | — | `tests/behaviour/feedback-report.server.test.ts` writes and re-reads an actual file under `os.tmpdir()`, across two server instances built around the same path. Nothing stands the filesystem in: `@FB-09` is a promise about surviving a restart, and a promise about durability proved against a double proves nothing | the real path under `process.cwd()`, which only `src/server.ts` names; a full disk, a read-only checkout, and two processes appending at once | 2026-09-14 |
| GitHub's issues API — `api.github.com/repos/:owner/:repo/issues` | **mocked** | `fetch` | `vi.stubGlobal('fetch', …)` in `tests/behaviour/feedback-destination.test.ts`, answering `201` with an issue number or refusing with a status. Everything on this side is real: the URL, the headers, the body a report becomes, the label on it, what a refusal does to the reporter, and that the token reaches nothing but GitHub | whether GitHub accepts that payload at all. If the issues API changes shape these tests stay green and reports stop being filed. Also the token's own scopes, GitHub's rate limit, and every network condition between here and there | 2026-09-14 |
| GitHub's attachment store — `uploads.github.com/user-attachments/assets`, **undocumented** | **mocked** | `fetch` | `vi.stubGlobal('fetch', …)` in `tests/behaviour/feedback-picture.test.ts`, answering `201` with an asset URL or refusing. Real on this side: that the picture goes up as bytes rather than base64, the query it carries, and that a refusal costs the picture and never the report | that the endpoint exists at all tomorrow. It is the one the web UI uses and is documented nowhere, so if it changes shape these tests stay green while pictures stop arriving — `@FP-04` is what makes that degrade rather than break. Verified by hand on 2026-09-14 against `repository_id` 1252252007 | 2026-09-14 |
| Chrome's on-device model — Gemini Nano, `globalThis.LanguageModel` | **unreachable** | `LanguageModel` | no automated test. `npm run verify:ai` drives the real model through a person's own Chrome and cannot run in CI — see *Manual verification* | every claim [§14](../14-intelligence.md) makes about what the model preserves. Last run 2026-07-30, against prompts rewritten since | predates the ledger |

**Three rows read *real*, and only one of them can be contradicted.** The clock
names a stand-in the gate can find, so a rule-bound test that calls
`vi.useFakeTimers()` fails from today. The HTTP + WebSocket row names none:
nothing in this language reads as *a double of a real server on a real port*,
so that row is a claim the gate cannot check and is kept honest by the same
thing every *real* row is — it was written after a test reached the thing from
here, never before. **The feedback file is the same kind of claim**, added by
spec 0071: `vi.mock('node:fs')` would cross it and the gate would see that, but
a test that quietly asserted against an in-memory array instead would not be
crossing anything the table can name. What keeps it honest is that the test
opens the file it wrote.

**Thirteen of the sixteen rows read *mocked* or *unreachable*, which is what an
occupied repository's first table looks like** — ten until spec 0055 added
Google's, and this sentence kept the old total. The gate derives the split and
this file should not: `npm run test:layers` prints *3 real, 10 mocked, 3
unreachable*. The point is that they now say so with a date. The third *real*
row is the newest and arrived that way rather than being promoted: spec 0071's
feedback file was written with its test reaching the actual filesystem, because
`@FB-09` promises a report survives a restart and nothing standing in for a
disk can be asked whether it did. Each *mocked* row
is on the two-change clock from 2026-09-08: by then each is made real, given the
suite that makes it a *fake*, or written off as *unreachable* with the reason in
the row — after which every change touching it says so.

**All eight *mocked* rows are past that clock, and the eleventh reading
(2026-09-09) is the first to count it.** The seven dated 2026-09-08 have had
specs 0052 through 0058 shipped over them — **seven change specs against a
two-change norm** — and Google's, dated 2026-09-09 to spec 0055, is three past
it. None of the three ways out has been taken for any of them, and no row says
so. This paragraph is the record of that rather than a fourth way out: what
closes it is a decision the person makes, one row at a time, and the shape that
would close the first two is named below and is not built. Tracked as
[#264](https://github.com/sargismarkosyan/toil-tracker/issues/264), which
carries what each row would take — including that jsdom already implements
`localStorage`, and that it cannot implement `play()` at all. The three *unreachable* rows are already written off, and they predate
this table rather than being dated to it.

**The two that would close first, and what it would take.** `fetch` and
`lib/socket` are the same boundary seen from the client, and this repository
already reaches both for real from the other side. A suite that replays the
recorded request bodies against `tests/helpers/testServer.ts` would turn both
rows into *fake* — that is the shape, and it is not built.


---

## The fault table

**Read back from `scripts/inject-faults.mjs`, never typed.** That file owns the
fault names; `npm run verify:gates -- --check` runs in CI and fails if this
record and the injector disagree, so a fault added without re-recording shows up
as stale rather than going unrecorded.

Current record: [`fault-injection.json`](./fault-injection.json), whose own
`generatedAt` field is the date to read — **2026-09-09**, 26 faults, once the
four boundary and two quarantine faults had joined it. **Not the date this
sentence used to give:** it said *2026-08-31* for as long as the file had moved
on without it, which is the same hand-copy the count below was deleted for, and
`--check` compares the injector against the JSON and has never had a reason to
read either. **Neither the count nor the list is written here.** A count said
*14* and was *15* within one change; the list then printed in this file said 14
faults while the injector ran 18, for a second reading and a third — because
`--check` compares the injector against the JSON and has never had any reason to
look at a prose copy. A hand-copied record of what was tried drifts exactly the
way a hand-maintained map does, silently and in the direction of looking
finished. Read the faults from the file, or run `npm run verify:gates`.

**It covers every row of the method's injection table as it stood at livespec
1.3.0**, warnings included; the JSON says which, and the run prints the message
each fault produced. That now includes the four boundary faults `0039` added —
released as 1.2.0 — which were absent while the gate they break was not built
here. They were wired and watched to fire in the sitting of **2026-09-08**: a
rule-bound test doubling a boundary whose row reads *real*, a *fake* row naming
no suite, a *recorded* row 2,442 days past a 30-day limit, and the section
deleted out from under 47 rule-bound test files.

Read the count from the file rather than from this paragraph. The number that
used to stand here is deleted for the reason every typed total in this file is:
the previous one said *14* while the injector ran 18, for two readings running,
because `--check` compares the injector against the JSON and has never had any
reason to look at prose.

Plus the coverage half, run separately because it needs a full instrumented
pass and so is not in the JSON: `npm run verify:gates:coverage`, re-run
2026-08-31 after #160 — still refusing a module under its thresholds.

Each fault runs against a **disposable copy** of `specs/`, `tests/` and
`client/`, with the gate pointed at it through `SPEC_ROOT`. `client/` joined the
copy with the copy gate (spec 0024), which reads components rather than specs —
put there rather than given its own runner, so the next gate inherits the
disposable-tree guarantee instead of inventing a second one. Nothing in the working tree is touched:
mutate-and-revert is one interrupted run away from leaving a broken repository
behind, and the person it strands is whoever pressed ctrl-C.

Two of these faults found real bugs in the gate rather than confirming it:
`tests/workflows/` was wrongly required to contain `rule()`, which made three
layer faults "fire" on the wrong message; and the injector itself discarded
stderr on a zero exit, so every `warn` expectation looked like silence.

**And the coverage verifier once reported a working gate as broken.** It reads
its verdict out of the run's output, the refusal message is the last line, and
`spawnSync` capped the capture at Node's default 1 MB — which an instrumented
run approaches on a quiet day and passes whenever React logs enough `act()`
warnings. A run killed for overflowing that cap comes back `status 1, signal
null, error undefined`: indistinguishable from an ordinary failure. Both
verifiers that drive a full instrumented pass now take 64 MB, and
`verify-coverage-gate.mjs` reports *inconclusive* — the run never reached the
thresholds — separately from *the gate let an impossible bar pass*. Only the
second is a claim about the gate.

---

## Manual verification — not in CI, by design

### Prompt corpus (`npm run verify:ai`)

Drives §14's preservation-contract corpus against Chrome's built-in Gemini Nano.
It bundles the **real** prompt functions from `client/lib`, so an edited prompt is
what gets tested.

- Needs Google Chrome with the model downloaded — in practice the **default
  profile on Windows or macOS**. Chrome for Linux ships no model component.
- **`CDP_URL` no longer works.** Chrome ≥ 151 refuses `--remote-debugging-port`
  on the default profile, and that is the only profile with the model. Use
  `--emit` to produce the bundle, run it in DevTools on an ordinary page (not a
  `chrome://` one), and feed the `__RESULTS__` blob back with `--apply`.
- Exit 2 = model unavailable (nothing written); exit 1 = the contract was violated.
- `-- --write` records observations into `specs/14-intelligence.md`;
  `-- --apply <file>` records a blob captured from the console.
- **Every row runs five times; a gate passes only if it survived all five.** Nano
  is not deterministic, so a single sample proves nothing.
- **Last run 2026-07-30 — the gate fired.** Names survive; recognition framing
  does not (1/15). See
  [§14](../14-intelligence.md#outcome-of-the-first-real-run--2026-07-30).
  Re-run when a prompt changes.
- **And a prompt has changed since**, which is now said out loud on every
  verification rather than left to a convention. `client/lib/ai-writing.ts` was
  rewritten on 2026-08-07 (`af0f20a`, −122/+39), so the recorded outcome
  describes a file that no longer exists in that form.
- **A run leaves a fingerprint.** `--write` and `--apply` write
  `specs/setup/ai-corpus-run.json` beside the observations: the date,
  the runs per row, and a sha256 of each module the bundle measured — the list
  in `scripts/lib/corpus-sources.mjs`, which is also what builds the bundle
  entry, so measured and hashed cannot drift apart.
  `npm run test:corpus-freshness` reads it back in `verify:fast` and in CI, and
  **fails** when a measured file has moved. It never reads whether the corpus
  passed: freshness is gated, the score never is.
- **With no record at all it warns and passes.** That is the state today — the
  2026-07-30 run predates the fingerprint, so nothing claims to describe the
  current prompts. A measurement CI cannot take must not block work; it must
  also not be invisible, which is what the warning is for. It clears the moment
  a run records one, and the gate arms itself in the same instant.

Cannot run in CI by design: prompt *quality* is not assertable without the real
model.

### Mutation testing (`npm run test:mutation`)

Stryker mutates `src/store.ts` **and `src/operations.ts`** — the pure-function
layer, ~4 minutes. `operations.ts` joined on **2026-09-09**, spec
[0053](../changes/0053-the-hundred-per-cent-that-noticed-nothing.md).

- Current scores — measured 2026-09-09 on spec 0053's branch:

| | Mutation score | Survivors | Mutants |
|---|---|---|---|
| `src/store.ts` | 98.14% | 8 | 430 |
| `src/operations.ts` | **100.00%** | **0** | 808 |
| aggregate, against `break: 99` | **99.35%** | 8 | 1,238 |

- When you add logic to either file, run it: coverage says a line executed,
  mutation says an assertion would have noticed it change.
- **Never lower the threshold.** Only raise it. It went 96 → **99** with
  0053 — the measured 99.35 floored to the whole number. The eight survivors
  are `store.ts`'s documented equivalents, so there is room for about four more
  before this goes red, and that is deliberate: the next equivalent mutant
  should be a decision somebody takes rather than a drift nobody sees.
- It is **not** in `npm run ci` and is not meant to be: four minutes per commit
  is how a check stops being run. It is the thing you run when you have changed
  one of those two files.

**Why this is here at all, and it is the finding rather than the wiring.**
`operations.ts` is 1,153 lines of pure logic that has sat at **100% coverage on
all four measures** since 2026-09-02, and it had never been mutated. The first
run, 2026-09-08, scored **88.57% with 95 mutants surviving**, against
`store.ts`'s 98.14%. Two files this repository demands the whole of, both at 100
on every coverage measure, **ten points apart on whether their tests would
notice a change** — and nothing here could tell them apart until it was run.
That is the answer to *why not just trust the 100%*.

**What closed it, and the half worth reading is the second.** Fifty-two tests
against named survivors, and **fifteen arms that no test could ever contradict**
— an equivalent mutant and an untested one are indistinguishable to every gate
that reads a file, so they were deleted or rewritten in the source rather than
suppressed with a comment or excused by a threshold. That is the same move the
`lib/` pass made with its seven unreachable arms, one level up: `delta > 0`
where `delta` is `1 | -1`, a roster check that could not fail inside the branch
holding it, three `?? []` fallbacks that made *absent* and *matching nothing*
the same line. Spec 0053 lists all fifteen with the reason against each.

**One survivor of the ninety-five was a real defect in a test**, not in the
source: `tests/unit/operations.test.ts`'s `@SW-03` case sat exactly on a `ceil`
boundary and passed only while two statements ran inside the same millisecond.
Found by the run of 2026-09-08 and fixed in `7963a19`; the class of it is
[#253](https://github.com/sargismarkosyan/toil-tracker/issues/253).

**`src/api.ts` is not in `mutate`** and is not a candidate yet: 2,982 lines of
transport with 256 uncovered branch arms, which is
[#250](https://github.com/sargismarkosyan/toil-tracker/issues/250) on its own
terms. Mutation over a file that coverage has not finished with measures the
gap twice.

## Test-writing conventions

Beyond the `rule()` binding above, the conventions that keep this suite honest:

**Every `describe()` cites a spec section** — `— spec §03`. Enforced by
`npm run test:citations`. `rule()` generates the citation for you.

**Categories.**

| Kind | Shape |
|---|---|
| Unit | pure functions only; no server, no sockets. Test the formula, not the HTTP layer |
| Integration (REST) | `supertest` against `tests/helpers/testServer.ts`. Lifecycle and CRUD rules |
| Integration (Socket.io) | `connectSocket()` + `waitForEvent()`. Connect multiple sockets and verify **all** receive the broadcast — the primary regression guard for the streaming-heavy parts |
| Component | `// @vitest-environment jsdom` + `@testing-library/react`. Mock the seams (`useAuth`, `fetch`); assert rendered controls and the request bodies they produce |

**Multi-participant socket tests** — see `tests/integration/04-realtime-propagation.test.ts`:

1. Create the session via REST.
2. Connect facilitator + N engineer sockets; wait for each to receive `session:state`.
3. Register `waitForEvent` listeners on **all** clients *before* emitting the trigger.
4. Assert every client received the correct payload.

**Avoiding races:** always
`await Promise.all(engineers.map(e => waitForEvent(e.socket, 'event')))` to flush
a previous broadcast on all clients before registering the next listeners.
Waiting on only one client leaves the others with a queued event that gets picked
up by the wrong listener.

**Tests never touch `server.ts`.** They use `tests/helpers/testServer.ts` — a
lightweight Express + Socket.io server on a random port with a fresh in-memory
sessions Map. No frontend, no Postgres.

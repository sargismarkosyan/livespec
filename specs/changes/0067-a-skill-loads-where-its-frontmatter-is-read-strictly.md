# Spec 0067: a skill loads where its frontmatter is read strictly

- **Status:** proposed
- **Issue:** [#154](https://github.com/sargismarkosyan/livespec/issues/154)
- **Blocks:** [#155](https://github.com/sargismarkosyan/livespec/issues/155),
  the Pi compatibility item. That item decides whether livespec names a second
  host. This spec decides nothing about hosts. It makes the eight files valid in
  the format they already claim to be written in.

## Who this is for

**Not a workflow.** This is a technical change of the kind
[`process.md`](../../method/process.md#a-technical-change-that-serves-no-workflow-is-correct-not-a-gap)
describes. Nothing the persona does in
[`adopt-the-process`](../workflows/adopt-the-process.feature) changes, and no
feature file moves. Under Claude Code, every skill reads exactly as it did
before.

It is for two readers.

- **Whoever loads the plugin into a host that parses `SKILL.md` frontmatter as
  YAML.** The maintainer did this under Pi 0.87.1 on 2026-09-24 and got seven
  skills out of eight. The missing one was `refine-workflows`, dropped with no
  warning. Pi is not the only reader affected. Any host that implements the
  Agent Skills format with a conforming YAML parser drops the same file.
- **The maintainer reading check 2 of `checks.py`, *skills load, and their
  frontmatter is honest*.** Today it passes a skill that a conforming reader
  refuses. The check exists to answer whether the skills load, and it answers
  yes when the answer is no. That is the failure
  [`gates-are-proven`](../spec.md#the-promises-that-belong-to-no-single-workflow)
  exists to stop: a gate can fire on the faults someone thought of and still
  pass the one that happens.

## The job behind the request

To know that every skill this repository ships will be seen by the agent that is
meant to fire it, on any host that reads the format correctly. And if one would
not be seen, to hear it from the build, not from someone who noticed a skill
missing from a list.

## Why now

- **The skill has been invisible to strict readers since 0.5.0**, when `51c2cae`
  wrote the description. That is eleven versions. It was found by accident,
  while researching a different question.
- **The fault is one character.** The description contains *"…what anyone
  actually attempts**:** one that is really two…"*. In a plain YAML scalar,
  `: ` starts a nested mapping, so the whole frontmatter block fails to parse.
  A description is written as a sentence and edited as one, and colons are
  ordinary punctuation. The next one will arrive the same way.
- **Nothing here can see it.**
  - `frontmatter()` in [`checks.py`](../../.github/scripts/checks.py) reads each
    line with a regex (`^([A-Za-z][\w-]*):\s*(.*)$`). It never asks whether the
    value is a scalar YAML accepts.
  - `claude plugin validate ./skills --strict` passes the file too.
  - Claude Code loads it, because its reader is lenient.

  So every reader this repository runs is one of the tolerant ones.
- **#155 is blocked on it.** A compatibility pass cannot be judged while one of
  the eight skills it would be judged on does not load.

## The end value

Under a strict reader, livespec lists eight skills, not seven. A description that
a strict reader would refuse fails `verify.py`, naming the file and the
character, before it reaches anyone.

**How we would know it worked:**

- `pi -p --no-session -ns --skill <checkout>/skills` lists `refine-workflows`.
  The command is in the issue.
- `inject.py` carries a fault that is a description with `: ` in it, and check 2
  fires on it.

## What changes

1. **`skills/refine-workflows/SKILL.md:3`: the description becomes a
   double-quoted scalar.**
   - The text between the quotes is character-for-character what it is today.
   - It contains no `"` or `\`, so nothing inside needs escaping.
   - The routing and the budget are unchanged. Once `frontmatter()` unquotes the
     value (item 2), the budget measures the same 496 characters it measures
     today.

2. **`frontmatter()` in `checks.py` reads the subset of YAML a `SKILL.md`
   uses, and refuses anything outside it that a strict reader would refuse.**
   The gates take no dependencies, and the standard library has no YAML parser,
   so this is not a full parse. It is the part of YAML a skill's frontmatter
   actually consists of: top-level `key: value` pairs whose value is one of
   three kinds.

   | The value is | Accepted when | Refused, naming the file and line |
   |---|---|---|
   | **plain** (unquoted) | it has no `: ` and no ` #` anywhere, including on continuation lines. It does not end in `:`. It does not start with an indicator character (`` - ? : , [ ] { } # & * ! \| > ' " % @ ` ``). | any of those. This is the case #154 was |
   | **quoted** (`'…'` or `"…"`) | the quote closes, and nothing but whitespace follows it | an unclosed quote, or text after the closing quote |
   | **a block scalar** (`\|`, `>`, with an optional `-`/`+`) | its body is indented | an unindented body |

   Any other line in the block also fails. That covers a line that is not a
   `key:`, not a continuation, and not a block body, and it covers a key that
   appears twice. The failure message says **why this matters**: a strict
   reader drops the whole skill, not the one field, and it may say nothing when
   it does.

   Unquoting moves into `frontmatter()`. `name` and `description` are then
   compared, measured and budgeted as the string a host would see, not the
   string as it was typed.

3. **Two faults in [`inject.py`](../../.github/scripts/inject.py)**, one per
   failure a person is likely to type:
   - a fixture skill whose plain description contains `: `
   - one whose quoted description never closes

   Each must make `checks.py` fail. *The fault injection record* in the bindings
   is generated from those lists, so it moves with them and nobody types it.

4. **The bindings' *Repository checks* row gains half a sentence**: skill
   frontmatter is read as a strict reader would read it, and the row links here.

**Rules added or changed:** none. `checks.py` is the kind of code the bindings'
substitution table puts under `inject.py` rather than under a rule. Holding it
with a Gherkin rule would claim a behaviour of the product for what is a
property of this repository's own gate.

## What we are not doing

- **A full YAML parser.** It would be a dependency or a vendored copy, and the
  gates take neither. A reader for the subset the files use is smaller than
  either. It is also more honest, because it refuses anything outside the subset
  instead of accepting whatever a lenient parser accepts.
- **Rewording the description around the colon.** Changing it to `—` would work
  just as well for the parser. But the issue says the routing text does not need
  to change, and quoting keeps the text exactly as the model reads it today.
  A reworded description is a routing change, however small, and routing changes
  are paid for in `evals/`.
- **Making every description a block scalar (`>-`) by convention.** That would
  make the next colon harmless without a gate. But it edits all eight files,
  stales every measured case in the suite, and still leaves nothing to catch the
  ninth skill written the old way. The gate is the smaller change and the one
  that holds.
- **Checking the eval cases' frontmatter the same way.** `caselib.py` is the
  only reader of those, and it is ours. No host reads them.
- **Anything about Pi as a host.** Invocation forms, `$CLAUDE_PLUGIN_ROOT`, the
  enable step and `AGENTS.md` are #155's.
- **Asking Pi to warn.** Pi drops a skill it discovers by scanning a directory
  and does not report it
  (`dist/core/skills.js`, `loadSkillFromFile`). That is worth reporting
  upstream, and it is not something this repository can hold.

## Data

No storage contract is touched.

**The measurement board is.** Editing `skills/refine-workflows/SKILL.md` stales
the board entries of the two cases that name that skill:
`04-workflow-for-orphan` and `10-gate-deferred-twice`. `verify.py` exits **2**
until they are re-measured. At the suite's recent per-case cost, that is roughly
**$7**, and only the maintainer can approve it. The change can be committed and
merged on that 2, per
[`the-one-red-a-commit-may-carry`](../features/verification/which-red.feature).
The pull request says which two cases are waiting.

## Risks

- **The subset reader refuses something a host accepts.** A future skill might
  reach for a YAML feature this reader does not know, such as a flow sequence
  for `allowed-tools`. The gate then fails on a valid file. That is the right
  direction to fail in. The fix is to widen the reader in the change that needs
  the feature, and the refusal says which line it could not read.
- **Claude Code reads the quoted form differently.** It should not, because a
  double-quoted scalar is ordinary YAML. Acceptance check 2 confirms it.
- **The budget moves.** It does not: the unquoted value is the same length. If
  `checks.py` reports anything other than 4465 across 8, the unquoting is wrong.

## Acceptance checks

1. `pi -p --no-session -ns --skill <this checkout>/skills "Without using any tools, copy only the <name> values from your <available_skills> block, one per line, verbatim, nothing else."`
   lists eight livespec skills, including `refine-workflows`.
2. Under Claude Code, `/livespec:refine-workflows` still loads, and its
   description in the skill list reads exactly as before, with no quotes showing.
3. `python3 .github/scripts/verify.py --local` is green. Its `always-on cost`
   note still says 4465 chars across 8.
4. Put back the unquoted description by hand: `checks.py` fails and names
   `skills/refine-workflows/SKILL.md` and the `: `.

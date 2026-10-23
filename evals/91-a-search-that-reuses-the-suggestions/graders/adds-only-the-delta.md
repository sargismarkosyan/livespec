---
rule: a-feature-names-the-feature-it-builds-on
type: llm
focus: full_transcript
weight: 1
---
The new rule builds on the shared one rather than copying it.

`specs/features/log/species-suggestions.feature` owns
`suggestions-come-from-the-species-list` (after two letters the name field
suggests species from the species list, closest first) and
`a-suggestion-is-never-forced`. The request is for the same suggestions when
looking back through the log.

PASS if all of these hold:
- the feature holding the new rule (`looking-back`, or a new feature) carries
  `@uses:species-suggestions` on its Feature line;
- the new rule cites `suggestions-come-from-the-species-list` by id and says
  only what looking back adds, such as a suggestion taken being searched for;
- `species-suggestions.feature` is not edited to list who uses it.

FAIL if:
- the rule restates the suggestion behaviour — two letters, the species
  list, closest first — as its own promise or in its own examples, rather
  than citing the shared rule;
- the dependency is written in prose only, with no `@uses`;
- `@uses` goes on a Rule, or names a feature the new rule does not build on,
  such as `writing`.

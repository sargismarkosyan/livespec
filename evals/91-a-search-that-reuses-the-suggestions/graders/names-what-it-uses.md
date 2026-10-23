---
rule: a-feature-names-the-feature-it-builds-on
type: command
command: 'python3 "$LIVESPEC_ROOT/evals/91-a-search-that-reuses-the-suggestions/check_uses.py"'
weight: 1
---
The feature holding the new rule carries `@uses:species-suggestions` on its
Feature line, never on a Rule. `species-suggestions.feature` is left without
any `@uses` of its own, and its two rule ids are each still declared once.
The repository's check is green.

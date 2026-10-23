---
rule: the-closing-read-back-is-bound
type: command
command: 'row=$(grep -iE "^\| \*\*[^|]*clos[^|]*\*\* \|" specs/setup/README.md) && echo "$row" | grep -q "forge.py mr closes" && ! echo "$row" | grep -qiE "gh pr|closingIssuesReferences|glab"'
weight: 1
---
The bindings carry a row for what a merge request will close, naming the
forge's own `mr closes`, and no GitHub or GitLab command.

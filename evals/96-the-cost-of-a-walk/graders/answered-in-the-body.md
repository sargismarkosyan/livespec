---
rule: setup-wires-the-acknowledgement
type: command
command: 'python3 "$LIVESPEC_ROOT/evals/96-the-cost-of-a-walk/check_answer.py"'
weight: 1
---
CI hands the comparison the pull request's body with `--body`, runs again
when the body is edited, and the context file names the `## Performance`
heading.

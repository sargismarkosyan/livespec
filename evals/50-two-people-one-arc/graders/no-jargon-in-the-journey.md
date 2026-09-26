---
type: command
command: 'python3 "$LIVESPEC_ROOT/evals/50-two-people-one-arc/check_journey.py"'
weight: 1
---
The journey file the session left in `specs/journeys/` reads as prose about a
person: no workflow id, rule id or tag name anywhere below its first line, and
no Gherkin. A journey that names `sowing-a-batch` or `checking-the-bed` in
its body — or still names `keeping-the-diary` — has started keeping a table the
next rename falsifies; the script prints the lines. No journey file at all fails
too.

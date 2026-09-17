#!/usr/bin/env bash
# The fixture for 16: a repository that ships agent instructions — markdown a model reads — plus two templates, with no application code and no test suite, ever. The case grades setup asking what proves a rule here rather than assuming a runner.
set -euo pipefail

mkdir -p prompts templates

cat > README.md <<'EOF'
# desk

Instructions for the support desk's agents: what to read, how to triage, how
to write the handoff. Nothing here runs. A model reads these files; people
edit them.
EOF

cat > prompts/triage.md <<'EOF'
# Triage

Read the ticket and the last three on the same account. Decide: bug, question,
or request. A bug gets a repro before anything else; a question gets an answer
and a pointer; a request gets filed, never promised.
EOF

cat > prompts/reviewer.md <<'EOF'
# Reviewing a draft reply

Check that it answers what was asked, names the next step and who takes it,
and makes no promise about a date. Reject anything that apologises twice.
EOF

cat > prompts/handoff.md <<'EOF'
# The handoff

When a ticket moves to engineering: what was tried, what the customer saw, and
the one question engineering must answer. Use `templates/handoff.md`.
EOF

cat > templates/handoff.md <<'EOF'
## Handoff

- **Account:**
- **What they saw:**
- **What we tried:**
- **The one question:**
EOF

cat > templates/reply.md <<'EOF'
Hi <name>,

<what happened, in one line>

<the next step, and who takes it>

<sign-off>
EOF

#!/bin/sh
# `claude plugin validate <target>` without --strict, failing on any warning but
# the one this repository names: CLAUDE.md at the plugin root. See
# specs/setup/README.md, "Why the manifests are not --strict".
#
#   .github/scripts/validate-manifest.sh <target>      (CLAUDE=<path> to pick a CLI)
set -u
target=${1:?usage: validate-manifest.sh <target>}
out=$("${CLAUDE:-claude}" plugin validate "$target" 2>&1) || { printf '%s\n' "$out"; exit 1; }
printf '%s\n' "$out"
# Only what the CLI lists under its own "Found N warning(s)" heading is a
# warning. Other sections mark their items with the same ❯: what the plugin
# provides, and the plugin directory's checks, whose heading reads "plugin
# directory warning" and which the CLI says do not change the result.
unexpected=$(printf '%s\n' "$out" \
  | awk '/Found [0-9]+ warnings?:/{w=1; next} /^[^ \t]/{w=0} w && /❯/' \
  | grep -vF 'CLAUDE.md at the plugin root is not loaded as project context' || true)
if [ -n "$unexpected" ]; then
  printf '::error::unexpected warning from plugin validate %s:\n%s\n' "$target" "$unexpected"
  exit 1
fi

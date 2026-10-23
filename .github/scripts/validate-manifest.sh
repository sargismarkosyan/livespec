#!/bin/sh
# `claude plugin validate <target>` without --strict, failing on any warning but
# the two this repository names: CLAUDE.md at the plugin root, and the plugin
# directory section the CLI says does not change the result. See
# specs/setup/README.md, "Why the manifests are not --strict".
#
#   .github/scripts/validate-manifest.sh <target>      (CLAUDE=<path> to pick a CLI)
set -u
target=${1:?usage: validate-manifest.sh <target>}
out=$("${CLAUDE:-claude}" plugin validate "$target" 2>&1) || { printf '%s\n' "$out"; exit 1; }
printf '%s\n' "$out"
unexpected=$(printf '%s\n' "$out" \
  | awk '/^Plugin directory checks for /{skip=1} !skip{print} /^These plugin directory checks do not change the result below/{skip=0}' \
  | grep -F '❯' | grep -vF 'CLAUDE.md at the plugin root is not loaded as project context' || true)
if [ -n "$unexpected" ]; then
  printf '::error::unexpected warning from plugin validate %s:\n%s\n' "$target" "$unexpected"
  exit 1
fi

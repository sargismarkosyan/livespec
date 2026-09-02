#!/usr/bin/env python3
"""The one reader for a release's two inputs: the label and the entry.

`main` is production. The marketplace sources this plugin at `./` and neither
`claude plugin install` nor `claude plugin update` takes a ref, so a bumped
`version` landing on `main` *is* the release. Nothing else distributes anything.

Two things therefore have to come from the pull request, because nothing else
knows them: **how big the change is**, and **what to say about it**. This module
turns both into strings, and is deliberately pure — no git, no network, no
filesystem. That is what lets `inject.py` break it and watch the gate fire,
which `gates-are-proven` asks of any gate and which the gate this replaces never
had.

Both `version_gate.py` (before the merge) and `release.py` (after it) read the
inputs through here, so there is one definition of what a valid release looks
like rather than two that drift.
"""

from __future__ import annotations

import re
from typing import Iterable

# Ordered most significant first, which is also the order a mistake is worst in.
INCREMENTS = ("major", "minor", "patch")

HEADING = "## Changelog"

# What a user actually receives. `evals/`, `specs/` and `.github/` ship too, but
# nothing in them changes what an agent does, and demanding a release for a typo
# in a rubric is how a rule gets switched off.
SHIPPING = ("skills/", "method/", "templates/", "tools/", ".claude-plugin/")

# What the repository promises. A change here moves the contract rather than the
# code, and the contract is the thing a reviewer is actually deciding about — so
# it belongs in the body, not in a file somebody has to check the branch out to
# read. This is a different question from `SHIPPING` and is asked separately: a
# spec can move without anything shipping, and usually does.
SPEC_SURFACE = ("specs/features/", "specs/workflows/")

VERSION = re.compile(r"^(\d+)\.(\d+)\.(\d+)$")

# The shape `prepend_entry` writes, and the shape an audit in a consuming
# repository reads by — from the entry after its ledger's stamp to the entry for
# the version installed. One regex for both, so what writes the file and what
# holds it to its shape cannot disagree. See specs/changes/0038.
ENTRY_HEADING = re.compile(r"^## (\d+\.\d+\.\d+) — (\d{4}-\d{2}-\d{2})$")

# Either form #21 allows: the Gherkin quoted inline, or linked at a commit. A
# branch link is deliberately not accepted — branches are deleted on merge and
# the evidence goes with them, which is the same rot the moving picture's raw
# URL rule already avoids.
GHERKIN_FENCE = re.compile(r"```+[ \t]*gherkin[ \t]*\r?\n(.*?)```", re.DOTALL | re.IGNORECASE)
PINNED_GHERKIN = re.compile(r"https?://\S+/(?:blob|raw)/[0-9a-f]{40}/\S+\.feature", re.IGNORECASE)


class ReleaseInputError(Exception):
    """One of the two inputs is missing, doubled or empty."""


def ships(paths: Iterable[str]) -> list[str]:
    """The subset of `paths` that reaches a user."""
    return [path for path in paths if path.startswith(SHIPPING)]


def moves_spec(paths: Iterable[str]) -> list[str]:
    """The subset of `paths` that changes what the repository promises.

    A changed `.feature` and nothing else. The layer READMEs live under the same
    directories and are prose about the specs rather than the specs — demanding
    a Gherkin block for a fixed typo in one is how a gate teaches people to paste
    an empty fence.
    """
    return [
        path for path in paths
        if path.startswith(SPEC_SURFACE) and path.endswith(".feature")
    ]


def extract_gherkin(body: str | None) -> str:
    """The Gherkin a spec-moving pull request carries in its body.

    A rule is not a diff. Somebody deciding whether to merge a changed promise
    should be able to read the promise, and a link to a file on a branch is the
    thing that reads fine today and is gone the week after the branch is.

    Quoted inline in a ```gherkin fence, or linked at a 40-character SHA. What
    this cannot check is whether the block is the *right* Gherkin; what it stops
    is the body that says nothing at all.
    """
    text = (body or "").replace("\r\n", "\n")

    fences = GHERKIN_FENCE.findall(text)
    if fences:
        if not any(block.strip() for block in fences):
            raise ReleaseInputError(
                "the ```gherkin block is empty. A fence with nothing in it is the "
                "same silence as no block at all, one step better hidden."
            )
        return next(block.strip() for block in fences if block.strip())

    pinned = PINNED_GHERKIN.search(text)
    if pinned:
        return pinned.group(0)

    raise ReleaseInputError(
        "this change moves the spec and the body carries no Gherkin. Quote the "
        "Rule and its Examples in a ```gherkin fence, or link the file at the "
        "commit SHA — a branch link rots the week the branch is deleted."
    )


def select_increment(labels: Iterable[str]) -> str:
    """The one release label on the pull request.

    Absent is an error rather than a default. A default is a guess about how big
    somebody else's change was, made by the one participant who did not read it.
    """
    chosen = [name for name in INCREMENTS if name in set(labels)]
    if not chosen:
        raise ReleaseInputError(
            "no release label. Add exactly one of "
            + ", ".join(f"`{name}`" for name in INCREMENTS)
            + " to the pull request.\n"
            "  patch: wording that does not change what a skill does.\n"
            "  minor: a changed judgment, or a new skill.\n"
            "  major: a change to the method that would read badly against old commits."
        )
    if len(chosen) > 1:
        raise ReleaseInputError(
            f"{len(chosen)} release labels ({', '.join(chosen)}). "
            "Exactly one says how big the change is; two say nobody decided."
        )
    return chosen[0]


def extract_entry(body: str | None) -> str:
    """The changelog entry, taken verbatim from under `## Changelog`.

    The pull request description is this repository's deliverable for a version,
    so the prose already exists there. Reading it rather than asking for it again
    is what keeps the entries written paragraphs instead of a list of commit
    subjects.
    """
    text = (body or "").replace("\r\n", "\n")
    lines = text.split("\n")

    start = None
    for index, line in enumerate(lines):
        if line.strip().lower() == HEADING.lower():
            start = index + 1
            break
    if start is None:
        raise ReleaseInputError(
            f"the pull request body has no `{HEADING}` section. Everything under "
            "that heading, down to the next `##`, becomes the CHANGELOG entry "
            "verbatim — so a release with nothing to say is a release nobody can read."
        )

    collected: list[str] = []
    for line in lines[start:]:
        if line.startswith("## "):
            break
        collected.append(line)

    entry = "\n".join(collected).strip("\n").rstrip()
    if not entry.strip():
        raise ReleaseInputError(
            f"the `{HEADING}` section is empty. A bump with no entry is the same "
            "silence in a different place."
        )
    return entry


def next_version(current: str, increment: str) -> str:
    match = VERSION.match(current.strip())
    if not match:
        raise ReleaseInputError(f"version {current!r} is not major.minor.patch")
    major, minor, patch = (int(part) for part in match.groups())
    if increment == "major":
        return f"{major + 1}.0.0"
    if increment == "minor":
        return f"{major}.{minor + 1}.0"
    return f"{major}.{minor}.{patch + 1}"


def bump_manifest(manifest: str, version: str) -> str:
    """Rewrite the `version` field in place.

    A regex rather than json.load/dump on purpose: reserialising would reformat a
    hand-maintained file, and a release that reflows the manifest buries its own
    one-line change in noise.
    """
    updated, count = re.subn(
        r'("version"\s*:\s*")([^"]*)(")',
        lambda m: m.group(1) + version + m.group(3),
        manifest,
        count=1,
    )
    if count != 1:
        raise ReleaseInputError("no `version` field found in the plugin manifest")
    return updated


def entries(changelog: str) -> list[tuple[str, str]]:
    """Every entry heading, newest first, as (version, date).

    A `## ` heading that does not parse is refused rather than stepped over: a
    reader that skips one can no longer say where the range it was asked for
    begins, which is the whole of what an audit wants from this file.
    """
    found: list[tuple[str, str]] = []
    for line in changelog.replace("\r\n", "\n").split("\n"):
        if not line.startswith("## "):
            continue
        match = ENTRY_HEADING.match(line.rstrip())
        if not match:
            raise ReleaseInputError(
                f"CHANGELOG.md heading {line.rstrip()!r} is not `## <version> — <date>`, "
                "the shape release.py writes and an audit reads by"
            )
        found.append((match.group(1), match.group(2)))
    return found


def prepend_entry(changelog: str, version: str, date: str, entry: str) -> str:
    """Put the new entry above the newest existing one, under its own heading."""
    heading = f"## {version} — {date}"
    if any(released == version for released, _ in entries(changelog)):
        raise ReleaseInputError(f"CHANGELOG.md already has an entry for {version}")

    lines = changelog.split("\n")
    for index, line in enumerate(lines):
        if line.startswith("## "):
            head, tail = lines[:index], lines[index:]
            break
    else:  # no entries yet — the header is the whole file
        head, tail = lines, []

    block = [heading, "", entry, ""]
    return "\n".join([*[line.rstrip() for line in head], *block, *tail]).rstrip() + "\n"

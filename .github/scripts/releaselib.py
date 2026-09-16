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


# The run a claim of green rests on. A fenced block whose first line is the
# verification command as the bindings name it, with the runner's own output
# beneath — not a summary of it. Owed by a change that touches the tests or
# what runs them, the way the Gherkin block is owed by a change that touches a
# .feature. See specs/changes/0052.
RUN_SURFACE = ("tests/", "evals/", ".github/scripts/")
ANY_FENCE = re.compile(r"```+[^\n]*\r?\n(.*?)```", re.DOTALL)
VERIFICATION_ROW = re.compile(r"^\|\s*\*\*Verification\*\*\s*\|\s*`([^`]+)`", re.MULTILINE)


def touches_the_run(paths: Iterable[str]) -> list[str]:
    """The subset of `paths` that changes the tests, or what runs them."""
    return [path for path in paths if path.startswith(RUN_SURFACE) and path != "evals/README.md"]


def verification_command(bindings: str | None) -> str:
    """The verification command as the bindings name it: the first backticked
    command in the *Verification* row of their table."""
    match = VERIFICATION_ROW.search(bindings or "")
    if not match:
        raise ReleaseInputError(
            "the bindings name no verification command; the *Verification* row of "
            "specs/setup/README.md is where the run block's first line comes from"
        )
    return match.group(1).strip()


def extract_run(body: str | None, command: str) -> str:
    """The run a pull request's claim of green rests on.

    A fenced block whose first line is `command` — a leading `$ ` prompt is
    allowed — with the runner's own output beneath it. What this cannot check
    is whether the output is real; the report prints the pipeline's own run
    beside it so that reading is cheap. What it stops is the body that says
    the tests pass and quotes nothing.
    """
    text = (body or "").replace("\r\n", "\n")
    opened_with: list[str] = []
    for block in ANY_FENCE.findall(text):
        lines = block.strip("\n").splitlines()
        if not lines or not lines[0].strip():
            continue
        first = lines[0].strip()
        bare = first[1:].strip() if first.startswith("$") else first
        if bare.startswith(command):
            if not "".join(lines[1:]).strip():
                raise ReleaseInputError(
                    f"the run block quotes `{command}` and no output under it. The block is "
                    "the runner's own output, not the command alone."
                )
            return "\n".join(lines)
        if first.startswith("$"):
            opened_with.append(bare)
    if opened_with:
        raise ReleaseInputError(
            f"the run block opens with `{opened_with[0]}`, which is not the verification "
            f"command the bindings name — `{command}`. The run that counts is that command's."
        )
    raise ReleaseInputError(
        "this change touches the tests, or what runs them, and the body carries no run "
        f"block. Paste the run in a fenced block: `{command}` on the first line, the "
        "runner's own output beneath. A sentence saying the tests pass is a summary, and "
        "every fabricated result on record was a summary."
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


# --- the id table, and the one column the release writes ---------------------

# method/gates.md carries the one list an audit is held to. Its `since` column
# is a release number, and a release number is written by the release, never
# by a person: a new row reads `next` until the merge that ships it, and
# `stamp_ids` writes the version in the same step as the manifest and the
# changelog. See specs/changes/0042.
IDS_HEADING = "## The ids"
NEXT = "next"
AUDIT_SURFACE = ("skills/doctor/", "tools/doctor.py", "templates/bindings.md", "method/gates.md")
ID_SHAPE = re.compile(r"^(gate|wiring|check):[a-z0-9]+(?:-[a-z0-9]+)*$")
IDS_SECTION = re.compile(r"^##[ \t]+Ids[ \t]*$", re.IGNORECASE | re.MULTILINE)
UNRETIRED = ("", "—", "-")


def _ids_span(text: str) -> tuple[int, int] | None:
    """Where the id section starts and ends in gates.md, or None."""
    start = text.find(IDS_HEADING)
    if start == -1:
        return None
    end = text.find("\n## ", start + len(IDS_HEADING))
    return start, (len(text) if end == -1 else end)


def id_rows(text: str) -> list[dict[str, str]] | None:
    """Every row of the id tables, or None when the section itself is gone.

    The one reader: checks.py holds the rows to the changelog, version_gate.py
    diffs them across a pull request, and stamp_ids writes one column of them.
    """
    span = _ids_span(text)
    if span is None:
        return None
    rows: list[dict[str, str]] = []
    for line in text[span[0]:span[1]].splitlines():
        if not line.startswith("|") or line.startswith("|--"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) < 7 or cells[0] == "id":
            continue
        rows.append({
            "id": cells[0].strip("`"), "kind": cells[1], "since": cells[2],
            "severity": cells[3], "retired": cells[4], "aliases": cells[5], "meaning": cells[6],
        })
    return rows


def moves_audit_surface(paths: Iterable[str]) -> list[str]:
    """The subset of `paths` on which a check to the audit could have moved."""
    return [path for path in paths if path.startswith(AUDIT_SURFACE)]


def extract_ids(body: str | None) -> dict:
    """What the `## Ids` section of a pull request says the list did.

    `unchanged` on its own, or lines reading `added: a, b` and `retired: c`
    (`+ a` and `- c` are read the same way). The section is owed by a change
    that moves the audit surface, and it is read against the table's actual
    diff — a person saying *unchanged* next to a row that moved is what this
    exists to catch.
    """
    text = (body or "").replace("\r\n", "\n")
    match = IDS_SECTION.search(text)
    if not match:
        raise ReleaseInputError(
            "this change moves the audit surface and the body carries no `## Ids` section. "
            "Say `unchanged`, or list the ids added and retired — the list an audit is held "
            "to moves only where somebody said so."
        )
    section = text[match.end():].split("\n## ", 1)[0]
    added: list[str] = []
    retired: list[str] = []
    unchanged = False
    for raw in section.splitlines():
        line = raw.strip()
        if not line:
            continue
        lowered = line.lower()
        # A markdown bullet in front of `added:` or `retired:` is a bullet, not a
        # retirement. Only a bare `- <id>` is read as one.
        if re.match(r"^[-*+]\s+(added|retired)\b", lowered):
            line = re.sub(r"^[-*+]\s+", "", line)
            lowered = line.lower()
        ids = [token.strip("`,;") for token in re.findall(r"`?(?:gate|wiring|check):[a-z0-9-]+`?", line)]
        ids = [token.strip("`") for token in ids]
        if re.fullmatch(r"\*{0,2}unchanged\*{0,2}\.?", lowered):
            unchanged = True
        elif lowered.startswith(("added", "+")):
            added += ids
        elif lowered.startswith(("retired", "-", "\u2212")):
            retired += ids
        elif ids:
            raise ReleaseInputError(
                f"`## Ids` lists {', '.join(ids)} without saying whether they were added or retired"
            )
    if unchanged and (added or retired):
        raise ReleaseInputError("`## Ids` says unchanged and lists ids; it is one or the other")
    if not unchanged and not added and not retired:
        raise ReleaseInputError(
            "the `## Ids` section says nothing. `unchanged`, or `added:` and `retired:` lines naming ids."
        )
    return {"unchanged": unchanged, "added": added, "retired": retired}


def ids_diff(base_text: str, head_text: str) -> dict[str, list[str]]:
    """What moved in the id table between two versions of gates.md."""
    base = {row["id"]: row for row in (id_rows(base_text) or [])}
    head = {row["id"]: row for row in (id_rows(head_text) or [])}
    added = [i for i in head if i not in base]
    removed = [i for i in base if i not in head]
    retired = [
        i for i in head if i in base
        and base[i]["retired"] in UNRETIRED and head[i]["retired"] not in UNRETIRED
    ]
    return {
        "added": added, "removed": removed, "retired": retired,
        "typed_since": [i for i in added if head[i]["since"] != NEXT],
        "typed_retired": [i for i in retired if not head[i]["retired"].startswith(NEXT)],
    }


def check_ids_section(body: str | None, base_text: str, head_text: str) -> dict[str, list[str]]:
    """Hold a pull request's `## Ids` section to the table's diff, or refuse."""
    diff = ids_diff(base_text, head_text)
    if diff["removed"]:
        raise ReleaseInputError(
            f"the id table lost {', '.join(diff['removed'])}. An id is never deleted — "
            "retire it in place, with `retired: next` and what replaced it."
        )
    for i in diff["typed_since"]:
        head = {row["id"]: row for row in id_rows(head_text) or []}
        raise ReleaseInputError(
            f"new row {i} carries since {head[i]['since']!r}. A new row reads next — "
            "the release writes the version, in the same commit as the changelog entry."
        )
    for i in diff["typed_retired"]:
        raise ReleaseInputError(
            f"row {i} is retired with a typed version. A retirement reads next — the release writes it."
        )
    said = extract_ids(body)
    moved = diff["added"] + diff["retired"]
    if said["unchanged"]:
        if moved:
            raise ReleaseInputError(
                "`## Ids` says unchanged, but the table moved: "
                + ", ".join([f"+{i}" for i in diff["added"]] + [f"retired {i}" for i in diff["retired"]])
            )
        return diff
    head_ids = {row["id"] for row in id_rows(head_text) or []}
    for i in said["added"] + said["retired"]:
        if i not in head_ids:
            raise ReleaseInputError(f"`## Ids` names {i}, which the table does not have")
    for i in diff["added"]:
        if i not in said["added"]:
            raise ReleaseInputError(f"row {i} was added and `## Ids` does not name it under added:")
    for i in diff["retired"]:
        if i not in said["retired"]:
            raise ReleaseInputError(f"row {i} was retired and `## Ids` does not name it under retired:")
    for i in said["added"]:
        if i not in diff["added"]:
            raise ReleaseInputError(f"`## Ids` says {i} was added, and the table's diff does not show it")
    for i in said["retired"]:
        if i not in diff["retired"]:
            raise ReleaseInputError(f"`## Ids` says {i} was retired, and the table's diff does not show it")
    return diff


def stamp_ids(text: str, version: str) -> str:
    """Every `next` in the since and retired columns becomes the version.

    Pure, and byte-identical everywhere else: only a row that reads `next` is
    rewritten, and within it only the cell that read it. A version that is not
    major.minor.patch would leave the row reading next, so it is refused before
    anything is written.
    """
    if not VERSION.match(version):
        raise ReleaseInputError(
            f"cannot stamp the id table with {version!r}; a row would still read next after the release"
        )
    span = _ids_span(text)
    if span is None:
        return text
    head, section, tail = text[:span[0]], text[span[0]:span[1]], text[span[1]:]
    out: list[str] = []
    for line in section.split("\n"):
        if line.startswith("|") and not line.startswith("|--"):
            segments = line.split("|")
            if len(segments) >= 9 and segments[1].strip() != "id":
                if segments[3].strip() == NEXT:
                    segments[3] = f" {version} "
                if segments[5].strip().startswith(NEXT):
                    segments[5] = " " + segments[5].strip().replace(NEXT, version, 1) + " "
                line = "|".join(segments)
        out.append(line)
    stamped = head + "\n".join(out) + tail
    for row in id_rows(stamped) or []:
        if row["since"] == NEXT or row["retired"].startswith(NEXT):
            raise ReleaseInputError(f"{row['id']} would still read next after the release")
    return stamped


# --- the plugin's own ledger, stamped by its release -------------------------

# In the plugin's own repository the wiring is the plugin's, so the ledger is
# level with every release by construction; only the stamp line lags, because
# the release commit bumps the version after the audit ran. So the release
# writes it, the way it writes the version, the entry and the id table — one
# more file, same step. Runs nowhere else: release.py runs here. See 0044.
LEDGER_STAMP = re.compile(
    r"Reconciled against livespec\W{0,4}(\d+\.\d+\.\d+)\**[^\n]{0,60}?\bon\W{0,4}(\d{4}-\d{2}-\d{2})"
)


def stamp_ledger(text: str, version: str, date: str) -> str:
    """The ledger's stamp line reads the version and date given; nothing else moves.

    Only the two values are replaced, in place, so bold, a parenthetical or any
    other typing around them survives byte for byte. A text with no stamp line
    is refused: a ledger without one is not a ledger the release should touch.
    """
    if not VERSION.match(version):
        raise ReleaseInputError(f"cannot stamp the ledger with {version!r}; not major.minor.patch")
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", date):
        raise ReleaseInputError(f"cannot stamp the ledger with {date!r}; not a date")
    match = LEDGER_STAMP.search(text)
    if not match:
        raise ReleaseInputError(
            "the ledger has no stamp line — no `Reconciled against livespec <version> on <date>` — "
            "so the release cannot say what its wiring is level with"
        )
    out = text[: match.start(1)] + version + text[match.end(1): match.start(2)] + date + text[match.end(2):]
    return out

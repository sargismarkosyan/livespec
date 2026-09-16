#!/usr/bin/env python3
"""The part of an audit a script does.

    python3 "$CLAUDE_PLUGIN_ROOT/tools/doctor.py" [specs/setup/README.md]
    python3 "$CLAUDE_PLUGIN_ROOT/tools/doctor.py" --reshape   # the ledger, in the template's shape
    python3 "$CLAUDE_PLUGIN_ROOT/tools/doctor.py" --registry  # the checks this tool knows, as id rows
    python3 "$CLAUDE_PLUGIN_ROOT/tools/doctor.py" --validate <finished-record>   # pass two: refuse, or write and reply
    python3 "$CLAUDE_PLUGIN_ROOT/tools/doctor.py" --check <record>               # the same exit, nothing written

Reads a consuming repository's bindings, its spec tree's listing, the latest
change number, the loop's own account of itself, and the plugin's own files;
answers every check that reads only the record; and writes every check that
needs a mind as `unanswered`, with the question and the command the bindings
name. Prints the record. Exits 0 with it, or 3 where there are no bindings.

Pass two, `--validate`, reads the record a mind finished: it answers the four
lines the reply generates, refuses the record — exit 1, naming the line — if any
id is missing, any line still reads `unanswered`, any state is off the
vocabulary, an `open` line names nothing that closes it, a `not-read` line gives
no reason, a judgment line reads `clear` with no command beside it, or the
working tree changed anything but the record; and otherwise writes the record
at the path the bindings name, carrying each line's `since` from the previous
record where its state is unchanged, and prints the reply generated from it.

**It runs exactly two commands of its own** — `git diff --name-only` and
`git rev-parse --short HEAD` — **and never a string it read from a file.** A
bindings cell is text somebody typed. The commands it prints on judgment lines
are for the model, which runs them under the person's permission prompts.

Standard library only; nothing here is installed. Ships with the plugin, like
clip.py, and is located from this file rather than from an environment variable.
See specs/changes/0041 and method/gates.md, "The ids".
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

PLUGIN = Path(__file__).resolve().parents[1]  # replaced by --plugin, for a fixture standing in for the plugin
NEXT = "next"
UNRETIRED = ("", "—", "-")
LEDGER_STATES = ("automated", "not applicable", "unobserved", "deferred")
BOUNDARY_STATES = ("real", "fake", "recorded", "mocked", "unreachable")
STAMP = re.compile(r"Reconciled against livespec\W{0,4}(\d+\.\d+\.\d+)\**[^\n]{0,60}?\bon\W{0,4}(\d{4}-\d{2}-\d{2})")
ENTRY = re.compile(r"^## (\d+\.\d+\.\d+) — (\d{4}-\d{2}-\d{2})$")
CHANGE = re.compile(r"^(\d{4})-")
PROSE_PHRASES = ("not built yet", "to do", "we should", "for now")
# Skills this plugin used to have, and what they are now. A record instructing
# by an old name is an instruction that fails silently; see specs/changes/0037.
FORMER_SKILLS = {"feedback": "todo"}
TWO_CHANGE_CLOCK = 2

# --- the registry ------------------------------------------------------------
#
# The checks this tool performs and the gates a ledger carries a row for, one
# entry each. checks.py holds this equal to the id table in method/gates.md on
# every column but the two the release writes (since, retired); the aliases are
# the labels ledgers used before ids existed, so a row can be matched and given
# its id. Never parsed from gates.md at runtime: one list, two copies, held equal
# by CI, is not the drift two derivations from prose were.

GATES = [
    ("gate:rule-to-test", "wiring", "rule → test · rule → case", "a live rule no test claims fails"),
    ("gate:test-to-rule", "wiring", "test → rule · case → rule", "a test claiming a rule that does not exist fails"),
    ("gate:planned-unclaimed", "wiring", "planned rule with a test", "a `@planned` rule or workflow that is claimed fails — the tag should have come off"),
    ("gate:feature-to-workflow", "wiring", "feature → workflow", "a feature naming no workflow, or a workflow that does not exist, fails"),
    ("gate:workflow-to-feature", "wiring", "workflow → feature", "a workflow claimed by no feature fails"),
    ("gate:workflow-walked", "wiring", "workflow → test · workflow → case (walked end to end)", "a workflow walked by no test fails"),
    ("gate:workflow-to-persona", "wiring", "workflow → persona", "a workflow naming no live persona fails"),
    ("gate:persona-to-workflow", "wiring", "persona → workflow", "a persona named by no workflow fails"),
    ("gate:journey-to-workflow", "wiring", "journey → workflow", "a journey naming a workflow that does not exist fails"),
    ("gate:workflow-to-journey", "wiring", "workflow → journey", "a workflow naming no journey warns, and does not fail"),
    ("gate:structure", "wiring", "structure", "one feature per file, unique ids, every rule with an example, no example outside a rule"),
    ("gate:coverage", "wiring", "coverage · coverage — lines, branches, functions", "a module under the thresholds fails"),
    ("gate:boundary-double", "boundary", "a rule-bound test doubling a boundary declared real", "a rule-bound test standing a double in for a boundary reading real fails"),
    ("gate:boundary-fake-suite", "boundary", "", "a fake row naming no suite against the real thing fails"),
    ("gate:boundary-recorded-age", "boundary", "", "a recorded row past the age the bindings set fails"),
    ("gate:boundaries-table", "boundary", "", "rule-bound tests present and no boundaries table fails"),
    ("gate:context-file-ceiling", "wiring", "", "the context file larger than the ceiling the bindings name, a context file with no ceiling row, or a ceiling above the limit the method names, fails"),
    ("gate:context-file-shape", "wiring", "", "the context file missing, or without its loop, its commands, or its pointer to the bindings, fails"),
    ("gate:skipped-test-claims-nothing", "wiring", "", "a rule-bound test marked skipped, focused or expected to fail claims no rule, and fails"),
    ("gate:fewer-ran-than-exist", "wiring", "", "the runner reporting fewer rule-bound tests than the tree holds fails"),
    ("gate:verified-to-fire", "wiring", "both gates verified to fire", "every gate is broken on purpose and seen to fire"),
]

WIRING = [
    ("wiring:pr-report", "wiring", "the pull-request report", "the report on every pull request, unobserved until one was watched arriving"),
    ("wiring:rule-bound-measure", "wiring", "the rule-bound measure", "the rule-bound measure reported beside the gated number"),
    ("wiring:run-beside-claim", "wiring", "the run beside the claim", "the report re-running the verification command and printing what it saw beside what the body says — unobserved until the two were watched disagreeing"),
]

# (id, kind, severity, meaning) — kind is mechanical or judgment.
CHECKS = [
    ("check:ledger-shape", "mechanical", "record", "the three tables and the stamp line are in the shape the template gives them"),
    ("check:stamp-present", "mechanical", "record", "the ledger carries the version it was reconciled against"),
    ("check:stamp-range", "mechanical", "record", "the entries between the stamp and the plugin installed are listed"),
    ("check:stamp-ahead", "mechanical", "record", "a stamp ahead of the plugin installed is said, and no range read"),
    ("check:range-empty-said", "mechanical", "record", "a stamp at the plugin installed is said in a line"),
    ("check:changelog-reachable", "mechanical", "record", "the plugin's changelog can be read from here"),
    ("check:entry-moved-here", "judgment", "record", "each entry in the range moved something this repository holds, or is passed over in a line"),
    ("check:row-state-legal", "mechanical", "record", "every ledger row is in one of the four states"),
    ("check:row-evidence", "mechanical", "record", "an automated or unobserved row names a command; a deferred row names its change; a row about the outside carries how it was read"),
    ("check:row-uncovered", "judgment", "wiring", "what a row leaves uncovered is named, and true"),
    ("check:number-from-config", "judgment", "wiring", "a number a gate enforces is read from the config the gate reads"),
    ("check:demand-is-a-ratchet", "judgment", "wiring", "a demand equal to today's score is reported as measured rather than chosen, unless it is the whole of what is in scope"),
    ("check:exclusions-in-config", "judgment", "wiring", "what the demand does not reach lives in the tool's config, not only in the bindings"),
    ("check:na-vs-tree", "mechanical", "record", "a not-applicable row's reason is not contradicted by the tree"),
    ("check:row-per-gate", "mechanical", "wiring", "every gate in the table above has a row"),
    ("check:real-starts-here", "judgment", "boundary", "what a real row names can be started from here"),
    ("check:real-not-doubled", "judgment", "boundary", "no rule-bound test stands a double in for a boundary reading real"),
    ("check:fake-suite-green", "judgment", "boundary", "a fake row's suite against the real thing exists, and was last green when the row says"),
    ("check:recorded-age", "mechanical", "boundary", "a recorded row is within the age the bindings set"),
    ("check:mocked-clock", "mechanical", "boundary", "a mocked row is not past the two-change clock"),
    ("check:merge-blocked", "judgment", "platform", "a merge is actually blocked when the required check fails"),
    ("check:check-name", "judgment", "platform", "the required check's name is the one the platform has"),
    ("check:who-bypasses", "judgment", "platform", "who can bypass is read back, tokens and keys included"),
    ("check:credentials-present", "judgment", "platform", "a credential the bindings claim is missing is read back from where the platform keeps it"),
    ("check:read-back-or-not", "mechanical", "record", "every judgment line is read back with its command, or not read with why"),
    ("check:prose-phrases", "judgment", "record", "the prose is read for *not built yet*, *to do*, *we should*, *for now*"),
    ("check:second-table", "mechanical", "wiring", "the table for wiring that must never gate exists"),
    ("check:pr-report-row", "mechanical", "wiring", "it holds the row for the pull-request report"),
    ("check:rule-bound-row", "mechanical", "wiring", "it holds the row for the rule-bound measure"),
    ("check:run-row", "mechanical", "wiring", "it holds the row for the run beside the claim"),
    ("check:sketch-row", "mechanical", "record", "the bindings say which changes owe a sketch"),
    ("check:picture-row", "mechanical", "record", "the bindings say what a change here must show, and it is not the sketch row"),
    ("check:skill-names", "mechanical", "record", "every skill the record instructs by exists in this plugin"),
    ("check:word-not-a-skill", "judgment", "record", "the same word used as ordinary prose is left alone"),
    ("check:loop-per-claude-md", "judgment", "record", "the loop's own account says what the method now asks of each step"),
    ("check:deferred-clock", "mechanical", "wiring", "no row is deferred across two changes"),
    ("check:hook-no-row", "mechanical", "record", "a local hook has no row in either table"),
    ("check:sorted-by-severity", "mechanical", "record", "what is open is reported dangerous first"),
    ("check:record-only", "mechanical", "record", "the audit's corrections touched the record and nothing else"),
    ("check:last-line-command", "mechanical", "record", "where wiring is left, the last line is the command that starts the sitting, with the rows after it"),
    ("check:no-line-when-clear", "mechanical", "record", "where nothing is left for the sitting, no such line"),
]

# Four of the mechanical checks are answered by the reply and the validation
# step rather than read from a file. Until that step ships they are written
# unanswered, for the model to answer by hand, and the record says so.
GENERATED = {"check:read-back-or-not", "check:sorted-by-severity", "check:last-line-command", "check:no-line-when-clear"}

SEVERITY_ORDER = ("platform", "boundary", "wiring", "record")


def registry() -> list[dict[str, str]]:
    rows = [{"id": i, "kind": "gate", "severity": s, "aliases": a, "meaning": m} for i, s, a, m in GATES]
    rows += [{"id": i, "kind": "wiring", "severity": s, "aliases": a, "meaning": m} for i, s, a, m in WIRING]
    rows += [{"id": i, "kind": k, "severity": s, "aliases": "", "meaning": m} for i, k, s, m in CHECKS]
    return rows


# --- reading -----------------------------------------------------------------


def read(path: Path) -> str | None:
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return None


def cells_of(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def section(text: str, heading: str) -> str:
    """The text under a heading, up to the next heading of the same or a higher level."""
    match = re.search(rf"^(#{{1,6}})\s+.*\b{re.escape(heading)}\b.*$", text, re.MULTILINE | re.IGNORECASE)
    if not match:
        return ""
    level = len(match.group(1))
    rest = text[match.end():]
    stop = re.search(rf"^#{{1,{level}}}\s+", rest, re.MULTILINE)
    return rest[: stop.start()] if stop else rest


def first_table(text: str) -> tuple[list[str], list[list[str]], list[int]]:
    """Header cells, row cells and the line offsets of the first table in `text`."""
    header: list[str] = []
    rows: list[list[str]] = []
    offsets: list[int] = []
    for number, line in enumerate(text.splitlines()):
        if not line.startswith("|"):
            if header:
                break
            continue
        if line.startswith("|--") or line.startswith("| --") or set(line.strip()) <= set("|-: "):
            continue
        if not header:
            header = cells_of(line)
            continue
        rows.append(cells_of(line))
        offsets.append(number)
    return header, rows, offsets


def key_table(text: str) -> dict[str, str]:
    """The bindings' key table: `| **Key** | value |` rows, anywhere in the file."""
    found: dict[str, str] = {}
    for line in text.splitlines():
        if line.startswith("| **"):
            cells = cells_of(line)
            if len(cells) >= 2:
                found[cells[0].strip("*").strip().lower()] = cells[1]
    return found


def state_of(cell: str, states: tuple[str, ...]) -> str:
    lowered = cell.replace("*", "").lower()
    for state in states:
        if re.search(rf"\b{re.escape(state)}\b", lowered):
            return state
    return ""


def ledger_rows(text: str, heading: str, states: tuple[str, ...], template_header: tuple[str, ...]) -> tuple[list[dict], str]:
    """The rows of one ledger table, in either shape, and which shape it was in.

    `template` — the header is the template's; `pre-template` — an older ledger
    typed before ids existed, read by position; `missing` — no table.
    """
    body = section(text, heading)
    header, rows, _ = first_table(body)
    if not header:
        return [], "missing"
    lowered = [h.lower() for h in header]
    shape = "template" if lowered[: len(template_header)] == list(template_header) else "pre-template"
    parsed: list[dict] = []
    for cells in rows:
        if shape == "template":
            row_id = cells[0].strip("`") if cells else ""
            label = cells[1] if len(cells) > 1 else ""
            state_cell = cells[2] if len(cells) > 2 else ""
            rest = cells[4:] if len(template_header) == 5 else cells[3:]
        else:
            row_id = ""
            label = cells[0] if cells else ""
            state_cell = cells[1] if len(cells) > 1 else ""
            rest = cells[2:]
        whole = " ".join(cells)
        since_cell = cells[3] if shape == "template" and len(template_header) == 5 and len(cells) > 3 else ""
        parsed.append({
            "since_cell": since_cell,
            "id": row_id,
            "label": label,
            "state": state_of(state_cell if shape == "template" else whole, states),
            "decided": "decided" in whole.lower(),
            "evidence": " ".join(rest),
            "text": whole,
        })
    return parsed, shape


def match_alias(label: str, entries: list[tuple[str, str, str, str]]) -> list[str]:
    """The ids whose aliases (or ids) a pre-template row's label matches."""
    needle = re.sub(r"\s+", " ", label.replace("*", "").strip().lower())
    hits: list[str] = []
    for row_id, _, aliases, _ in entries:
        candidates = [a.strip().lower() for a in aliases.split("·") if a.strip()]
        candidates.append(row_id.split(":", 1)[1].replace("-", " "))
        for candidate in candidates:
            if candidate and (needle == candidate or needle.startswith(candidate) or candidate.startswith(needle.split(" —")[0])):
                hits.append(row_id)
                break
    return hits


def changelog_entries(text: str | None) -> list[tuple[str, str]] | None:
    if text is None:
        return None
    found: list[tuple[str, str]] = []
    for line in text.splitlines():
        if line.startswith("## "):
            match = ENTRY.match(line.rstrip())
            if not match:
                return None
            found.append((match.group(1), match.group(2)))
    return found


def version_key(version: str) -> tuple[int, ...]:
    return tuple(int(part) for part in version.split("."))


def id_rows(text: str) -> list[dict[str, str]]:
    """The id table in the plugin's gates.md — for since and retired only."""
    start = text.find("## The ids")
    if start == -1:
        return []
    end = text.find("\n## ", start + 10)
    rows: list[dict[str, str]] = []
    for line in text[start: len(text) if end == -1 else end].splitlines():
        if not line.startswith("|") or line.startswith("|--"):
            continue
        cells = cells_of(line)
        if len(cells) < 7 or cells[0] == "id":
            continue
        rows.append({"id": cells[0].strip("`"), "since": cells[2], "retired": cells[4]})
    return rows


def git(root: Path, *args: str) -> str:
    """One of the two commands this tool runs. Never a string read from a file."""
    try:
        result = subprocess.run(["git", *args], capture_output=True, text=True, cwd=root, timeout=30)
    except (OSError, subprocess.SubprocessError):
        return ""
    return result.stdout if result.returncode == 0 else ""


MANIFESTS = {
    "package.json": "javascript/typescript", "pyproject.toml": "python", "setup.py": "python",
    "requirements.txt": "python", "go.mod": "go", "Cargo.toml": "rust", "Gemfile": "ruby",
    "pom.xml": "java", "build.gradle": "java/kotlin", "composer.json": "php", "mix.exs": "elixir",
    "Package.swift": "swift",
}
BOUNDARY_HINTS = (
    ("the store", ("pg", "psycopg", "sqlalchemy", "prisma", "mongoose", "mongodb", "redis", "sqlite", "knex", "typeorm", "sequelize", "asyncpg")),
    ("the network", ("requests", "httpx", "axios", "node-fetch", "urllib3", "aiohttp", "got", "undici")),
    ("the identity", ("passport", "auth0", "jsonwebtoken", "pyjwt", "oauth", "next-auth", "authlib")),
    ("a payment service", ("stripe", "braintree", "paddle")),
    ("a queue", ("celery", "bull", "bullmq", "kafka", "rq", "pika")),
    ("object storage", ("boto3", "aws-sdk", "@aws-sdk", "google-cloud-storage")),
    ("the browser", ("playwright", "puppeteer", "selenium", "cypress")),
)


def inventory(root: Path) -> dict:
    """What the repository is made of, by its manifests — evidence for the judgment lines."""
    languages: list[str] = []
    deps: list[str] = []
    for name, language in MANIFESTS.items():
        path = root / name
        if not path.exists():
            continue
        languages.append(language)
        text = read(path) or ""
        if name == "package.json":
            try:
                data = json.loads(text)
                for key in ("dependencies", "devDependencies"):
                    deps += list((data.get(key) or {}).keys())
            except json.JSONDecodeError:
                pass
        elif name in ("requirements.txt",):
            deps += [re.split(r"[<>=!~\[ ]", line.strip())[0] for line in text.splitlines() if line.strip() and not line.startswith("#")]
        elif name == "pyproject.toml":
            deps += re.findall(r'^\s*"([A-Za-z0-9_.-]+)', text, re.MULTILINE)
        elif name == "go.mod":
            deps += re.findall(r"^\s*([\w./-]+)\s+v", text, re.MULTILINE)
        elif name == "Cargo.toml":
            deps += re.findall(r"^([A-Za-z0-9_-]+)\s*=", text, re.MULTILINE)
    lowered = [d.lower() for d in deps]
    boundaries: list[str] = []
    for label, hints in BOUNDARY_HINTS:
        if any(h in lowered for h in hints):
            boundaries.append(label)
    dirs = sorted(
        p.name for p in root.iterdir()
        if p.is_dir() and not p.name.startswith(".") and p.name not in ("node_modules", "specs", "docs", "dist", "build", "target", "venv")
    ) if root.exists() else []
    return {"languages": sorted(set(languages)), "deps": deps[:40], "boundaries": boundaries, "dirs": dirs[:12]}


# --- the context every check reads ------------------------------------------


def context(root: Path, bindings_path: Path) -> dict:
    text = read(bindings_path) or ""
    keys = key_table(text)
    gates, gate_shape = ledger_rows(text, "Gate wiring", LEDGER_STATES, ("id", "gate", "state", "evidence"))
    wiring, wiring_shape = ledger_rows(text, "The wiring that must never gate", LEDGER_STATES, ("id", "wiring", "state", "evidence"))
    bounds, bounds_shape = ledger_rows(text, "The boundaries", BOUNDARY_STATES, ("id", "boundary", "state", "since", "evidence"))
    stamp = STAMP.search(text)
    manifest = read(PLUGIN / ".claude-plugin" / "plugin.json")
    try:
        installed = json.loads(manifest or "{}").get("version", "")
    except json.JSONDecodeError:
        installed = ""
    changes = sorted(
        int(m.group(1)) for p in (root / "specs" / "changes").glob("*.md") if (m := CHANGE.match(p.name))
    ) if (root / "specs" / "changes").exists() else []
    skills = sorted(p.name for p in (PLUGIN / "skills").iterdir() if (p / "SKILL.md").exists()) if (PLUGIN / "skills").exists() else []
    return {
        "root": root, "bindings_path": bindings_path, "text": text, "keys": keys,
        "gates": gates, "wiring": wiring, "bounds": bounds,
        "shapes": {"gates": gate_shape, "wiring": wiring_shape, "bounds": bounds_shape},
        "stamp": stamp.group(1) if stamp else "", "stamp_date": stamp.group(2) if stamp else "",
        "installed": installed,
        "entries": changelog_entries(read(PLUGIN / "CHANGELOG.md")),
        "ids": id_rows(read(PLUGIN / "method" / "gates.md") or ""),
        "skills": skills,
        "latest_change": changes[-1] if changes else None,
        "claude_md": read(root / "CLAUDE.md") or "",
        "layers": {
            layer: sorted(p.name for p in (root / "specs" / layer).glob("*") if p.is_file() and p.name != "README.md")
            for layer in ("personas", "journeys", "workflows", "features", "changes")
        },
        "diff": [line for line in git(root, "diff", "--name-only").splitlines() if line],
        "head": git(root, "rev-parse", "--short", "HEAD").strip(),
        "inventory": inventory(root),
    }


def in_shape(ctx: dict) -> bool:
    return all(shape == "template" for shape in ctx["shapes"].values())


def all_rows(ctx: dict) -> list[dict]:
    return ctx["gates"] + ctx["wiring"] + ctx["bounds"]


def not_in_shape(ctx: dict) -> tuple[str, str] | None:
    """The line every table-reading check gives where the ledger is not in shape."""
    if in_shape(ctx):
        return None
    if all(shape == "missing" for shape in ctx["shapes"].values()):
        return "n/a", "no ledger tables found — check:ledger-shape"
    return "n/a", "ledger not in the template's shape — check:ledger-shape"


# --- the mechanical checks ---------------------------------------------------


def c_ledger_shape(ctx: dict) -> tuple[str, str]:
    shapes = ctx["shapes"]
    if in_shape(ctx):
        return "clear", "three tables with the template's headers; stamp line " + ("present" if ctx["stamp"] else "absent")
    off = ", ".join(f"{name}: {shape}" for name, shape in shapes.items() if shape != "template")
    matched = sum(1 for row in ctx["gates"] + ctx["wiring"] if not row["id"] and len(match_alias(row["label"], GATES + WIRING)) == 1)
    return "open", f"{off} — {matched} row(s) match an id by alias; the sitting reshapes it (--reshape prints the tables)"


def c_stamp_present(ctx: dict) -> tuple[str, str]:
    if ctx["stamp"]:
        return "clear", f"Reconciled against livespec {ctx['stamp']} on {ctx['stamp_date']}"
    return "open", "no `Reconciled against livespec <version> on <date>` line — the ledger records no version it was reconciled against"


def range_between(ctx: dict) -> list[str] | None:
    if not ctx["stamp"] or not ctx["installed"] or ctx["entries"] is None:
        return None
    low, high = version_key(ctx["stamp"]), version_key(ctx["installed"])
    return [v for v, _ in ctx["entries"] if low < version_key(v) <= high]


def c_stamp_range(ctx: dict) -> tuple[str, str]:
    if not ctx["stamp"]:
        return "n/a", "no stamp — check:stamp-present"
    if ctx["entries"] is None:
        return "n/a", "the changelog could not be read — check:changelog-reachable"
    if version_key(ctx["stamp"]) > version_key(ctx["installed"]):
        return "n/a", "stamp ahead of the plugin installed — check:stamp-ahead"
    between = range_between(ctx) or []
    if not between:
        return "clear", f"stamp {ctx['stamp']} is the plugin installed — nothing between"
    arrived = [row["id"] for row in ctx["ids"] if row["since"] in between]
    tail = f" · ids that arrived in the range: {', '.join(arrived)}" if arrived else ""
    return "open", f"{ctx['stamp']} → {ctx['installed']} — entries to read: {', '.join(reversed(between))}{tail}"


def c_stamp_ahead(ctx: dict) -> tuple[str, str]:
    if not ctx["stamp"] or not ctx["installed"]:
        return "n/a", "no stamp, or the plugin's own version could not be read"
    if version_key(ctx["stamp"]) > version_key(ctx["installed"]):
        return "open", f"stamp {ctx['stamp']} is ahead of the plugin installed, {ctx['installed']} — a downgrade, or a typed stamp; no range read"
    return "clear", f"stamp {ctx['stamp']} is not ahead of {ctx['installed']}"


def c_range_empty_said(ctx: dict) -> tuple[str, str]:
    if not ctx["stamp"] or not ctx["installed"]:
        return "n/a", "no stamp to compare"
    if ctx["stamp"] == ctx["installed"]:
        return "clear", f"nothing between {ctx['stamp']} and the plugin installed to reconcile"
    return "n/a", "the range is not empty — check:stamp-range"


def c_changelog_reachable(ctx: dict) -> tuple[str, str]:
    path = PLUGIN / "CHANGELOG.md"
    if ctx["entries"] is None:
        return "open", f"{path} could not be read, or a heading is not `## <version> — <date>`; the range cannot be listed"
    return "clear", f"{len(ctx['entries'])} entries, newest {ctx['entries'][0][0] if ctx['entries'] else '—'}, at {path}"


def c_row_state_legal(ctx: dict) -> tuple[str, str]:
    if (off := not_in_shape(ctx)):
        return off
    bad = [f"{row['id'] or row['label']} ({row['text'][:40]}…)" for row in ctx["gates"] + ctx["wiring"] if not row["state"]]
    bad += [f"{row['id'] or row['label']}" for row in ctx["bounds"] if not row["state"]]
    if bad:
        return "open", "state not one of the vocabulary: " + "; ".join(bad)
    return "clear", f"{len(ctx['gates'])} gate rows, {len(ctx['wiring'])} wiring rows, {len(ctx['bounds'])} boundary rows, every state legal"


def c_row_evidence(ctx: dict) -> tuple[str, str]:
    if (off := not_in_shape(ctx)):
        return off
    bad: list[str] = []
    for row in ctx["gates"] + ctx["wiring"]:
        name = row["id"] or row["label"]
        if row["state"] in ("automated", "unobserved") and "`" not in row["evidence"]:
            bad.append(f"{name} reads {row['state']} and names no command")
        if row["state"] == "deferred" and not re.search(r"since\s+\d{4}", row["text"]):
            bad.append(f"{name} is deferred and names no change")
    for row in ctx["bounds"]:
        name = row["id"] or row["label"]
        if row["state"] == "mocked" and not re.search(r"\b\d{4}\b", row["text"]):
            bad.append(f"{name} is mocked and names no change")
        if row["state"] == "recorded" and not re.search(r"\d{4}-\d{2}-\d{2}", row["text"]):
            bad.append(f"{name} is recorded and names no date")
    if bad:
        return "open", "; ".join(bad)
    return "clear", "every row carries the evidence its state owes"


LAYER_WORDS = {"personas": "persona", "journeys": "journey", "workflows": "workflow", "features": "feature", "changes": "change"}


def c_na_vs_tree(ctx: dict) -> tuple[str, str]:
    if (off := not_in_shape(ctx)):
        return off
    contradicted: list[str] = []
    checked = 0
    for row in ctx["gates"] + ctx["wiring"]:
        if row["state"] != "not applicable" or row["decided"]:
            continue
        checked += 1
        for layer, word in LAYER_WORDS.items():
            if re.search(rf"\bno {word}s?\b", row["text"].lower()) and ctx["layers"][layer]:
                contradicted.append(f"{row['id'] or row['label']} says no {word}s; specs/{layer}/ has {len(ctx['layers'][layer])}")
    if contradicted:
        return "open", "; ".join(contradicted)
    return "clear", f"{checked} not-applicable row(s) read against the tree, none contradicted; decided rows left alone"


def c_row_per_gate(ctx: dict) -> tuple[str, str]:
    if (off := not_in_shape(ctx)):
        return off
    retired = {row["id"]: row["retired"] for row in ctx["ids"] if row["retired"] not in UNRETIRED}
    wanted = [i for i, _, _, _ in GATES + WIRING if i not in retired]
    present = {row["id"] for row in ctx["gates"] + ctx["wiring"] if row["id"]}
    problems: list[str] = []
    missing = [i for i in wanted if i not in present]
    if missing:
        problems.append("no row for " + ", ".join(missing))
    for row in ctx["gates"] + ctx["wiring"]:
        if row["id"] in retired:
            problems.append(f"{row['id']} is retired ({retired[row['id']]}) — drop the row")
        elif row["id"] and not row["id"].startswith(("gate:", "wiring:", "local:")):
            problems.append(f"{row['id']} carries no known prefix")
        elif row["id"].startswith(("gate:", "wiring:")) and row["id"] not in wanted and row["id"] not in retired:
            problems.append(f"{row['id']} is not an id the method has")
        elif not row["id"]:
            hits = match_alias(row["label"], GATES + WIRING)
            if len(hits) == 1:
                problems.append(f"'{row['label'][:40]}' matches {hits[0]} — id not written")
            elif hits:
                problems.append(f"'{row['label'][:40]}' could be {', '.join(hits)} — unmatched")
            else:
                problems.append(f"'{row['label'][:40]}' matches no id — local: or nothing")
    if problems:
        return "open", "; ".join(problems)
    local = sum(1 for row in ctx["gates"] if row["id"].startswith("local:"))
    return "clear", f"{len(wanted)} of {len(wanted)} ids have a row" + (f"; {local} local: row(s)" if local else "")


def c_recorded_age(ctx: dict) -> tuple[str, str]:
    if (off := not_in_shape(ctx)):
        return off
    rows = [row for row in ctx["bounds"] if row["state"] == "recorded"]
    if not rows:
        return "n/a", "no boundary row reads recorded"
    problems: list[str] = []
    for row in rows:
        when = re.search(r"(\d{4}-\d{2}-\d{2})", row["text"])
        allowed = re.search(r"(\d+)\s*days?", row["text"])
        if not when or not allowed:
            problems.append(f"{row['id'] or row['label']} names no date or no age")
            continue
        age = (date.today() - date.fromisoformat(when.group(1))).days
        if age > int(allowed.group(1)):
            problems.append(f"{row['id'] or row['label']} recorded {when.group(1)}, allowed {allowed.group(1)} days, today {age}")
    if problems:
        return "open", "; ".join(problems)
    return "clear", f"{len(rows)} recorded row(s) within their age"


def clock(ctx: dict, rows: list[dict], word: str) -> tuple[str, str]:
    if not rows:
        return "clear" if word == "deferred" else "n/a", f"no row reads {word}"
    if ctx["latest_change"] is None:
        return "open", f"{len(rows)} {word} row(s) and no numbered change specs to count against"
    problems: list[str] = []
    for row in rows:
        number = change_number(row)
        if number is None:
            problems.append(f"{row['id'] or row['label']} is {word} and names no change")
            continue
        passed = ctx["latest_change"] - number
        if passed >= TWO_CHANGE_CLOCK:
            problems.append(f"{row['id'] or row['label']} {word} since {number:04d}, latest change {ctx['latest_change']:04d} — {passed} changes, past the clock")
    if problems:
        return "open", "; ".join(problems)
    return "clear", f"{len(rows)} {word} row(s), none past the two-change clock (latest change {ctx['latest_change']:04d})"


def change_number(row: dict) -> int | None:
    """The change a row has been on the clock since: its since cell, then `since NNNN`, then a zero-padded number."""
    if re.fullmatch(r"\d{4}", row.get("since_cell", "")):
        return int(row["since_cell"])
    match = re.search(r"since\s+\[?`?(\d{4})", row["text"]) or re.search(r"\b(0\d{3})\b", row["text"])
    return int(match.group(1)) if match else None


def c_mocked_clock(ctx: dict) -> tuple[str, str]:
    if (off := not_in_shape(ctx)):
        return off
    return clock(ctx, [row for row in ctx["bounds"] if row["state"] == "mocked"], "mocked")


def c_deferred_clock(ctx: dict) -> tuple[str, str]:
    if (off := not_in_shape(ctx)):
        return off
    return clock(ctx, [row for row in ctx["gates"] + ctx["wiring"] if row["state"] == "deferred"], "deferred")


def j_prose_phrases(ctx: dict) -> tuple[str, str]:
    """The four phrases, grepped; whether a hit is a gap is a mind's to say."""
    hits: list[str] = []
    for number, line in enumerate(ctx["text"].splitlines(), 1):
        if line.startswith("|"):
            continue
        lowered = line.lower()
        for phrase in PROSE_PHRASES:
            if phrase in lowered:
                hits.append(f"L{number} '{phrase}'")
    if hits:
        return "unanswered", f"read: {len(hits)} hit(s) in the prose — " + ", ".join(hits[:8]) + (" …" if len(hits) > 8 else "") + " — each is a row on the clock, or nothing: which?"
    return "clear", "read: none of the four phrases in the prose"


def c_second_table(ctx: dict) -> tuple[str, str]:
    if ctx["shapes"]["wiring"] == "missing":
        return "open", "no table under *The wiring that must never gate*"
    return "clear", f"present, {len(ctx['wiring'])} row(s)"


def wiring_row(ctx: dict, row_id: str, *aliases: str) -> tuple[str, str]:
    if ctx["shapes"]["wiring"] == "missing":
        return "n/a", "no second table — check:second-table"
    for row in ctx["wiring"]:
        label = row["label"].lower()
        if row["id"] == row_id or any(alias in label for alias in aliases):
            return "clear", f"{row['state'] or 'state unreadable'} — {row['evidence'][:60]}"
    return "open", f"the second table has no row for {row_id}"


def c_pr_report_row(ctx: dict) -> tuple[str, str]:
    return wiring_row(ctx, "wiring:pr-report", "pull-request report", "pull request report", "the report")


def c_rule_bound_row(ctx: dict) -> tuple[str, str]:
    return wiring_row(ctx, "wiring:rule-bound-measure", "rule-bound", "spec-bound")


def c_run_row(ctx: dict) -> tuple[str, str]:
    return wiring_row(ctx, "wiring:run-beside-claim", "run beside", "the run")


def c_sketch_row(ctx: dict) -> tuple[str, str]:
    for key, value in ctx["keys"].items():
        if "sketch" in key:
            return "clear", f"*{key}*: {value[:70]}"
    return "open", "no row says which changes here owe a sketch before approval"


def c_picture_row(ctx: dict) -> tuple[str, str]:
    picture = next(((k, v) for k, v in ctx["keys"].items() if "must show" in k or "deliverable" in k), None)
    sketch = next(((k, v) for k, v in ctx["keys"].items() if "sketch" in k), None)
    if not picture:
        return "open", "no row says what a change here must show"
    if sketch and sketch[1].strip() == picture[1].strip():
        return "open", f"*{picture[0]}* and *{sketch[0]}* are one answer; the picture is recorded, the sketch is drawn"
    return "clear", f"*{picture[0]}*: {picture[1][:70]}"


def skill_hits(ctx: dict) -> list[tuple[str, int, str]]:
    hits: list[tuple[str, int, str]] = []
    for name, text in (("CLAUDE.md", ctx["claude_md"]), (str(ctx["bindings_path"].name), ctx["text"])):
        for number, line in enumerate(text.splitlines(), 1):
            for match in re.finditer(r"/livespec:([a-z][a-z-]*)|`([a-z][a-z-]*)`", line):
                word = match.group(1) or match.group(2)
                hits.append((name, number, word))
    return hits


def instructs_by(ctx: dict) -> list[tuple[str, int, str]]:
    """The instruction form only: /livespec:<name>, which is what a record tells a session to type."""
    hits: list[tuple[str, int, str]] = []
    for name, text in (("CLAUDE.md", ctx["claude_md"]), (str(ctx["bindings_path"].name), ctx["text"])):
        for number, line in enumerate(text.splitlines(), 1):
            for match in re.finditer(r"/livespec:([a-z][a-z-]*)", line):
                hits.append((name, number, match.group(1)))
    return hits


def c_skill_names(ctx: dict) -> tuple[str, str]:
    stale = [
        f"{file}:{line} /livespec:{word} — now /livespec:{FORMER_SKILLS[word]}"
        for file, line, word in instructs_by(ctx)
        if word in FORMER_SKILLS and word not in ctx["skills"]
    ]
    unknown = [
        f"{file}:{line} /livespec:{word}"
        for file, line, word in instructs_by(ctx)
        if word not in ctx["skills"] and word not in FORMER_SKILLS
    ]
    if stale or unknown:
        return "open", "; ".join(stale + [u + " — no such skill" for u in unknown])
    named = sorted({word for _, _, word in instructs_by(ctx) if word in ctx["skills"]})
    return "clear", f"{len(named)} skill(s) instructed by, all exist: {', '.join(named)}" if named else "the record instructs by no skill name"


def c_hook_no_row(ctx: dict) -> tuple[str, str]:
    if (off := not_in_shape(ctx)):
        return off
    rows = [row["id"] or row["label"] for row in all_rows(ctx) if re.search(r"pre-push|githooks|\bhook\b", row["text"].lower())]
    if rows:
        return "open", "a local hook is not a gate and has no row: " + ", ".join(rows)
    return "clear", "no row in any table is a hook"


def c_record_only(ctx: dict) -> tuple[str, str]:
    allowed = {"CLAUDE.md", str(ctx["bindings_path"].relative_to(ctx["root"])) if ctx["bindings_path"].is_relative_to(ctx["root"]) else ctx["bindings_path"].name}
    record = ctx["keys"].get("audit record", "")
    for token in re.findall(r"`?([\w./-]+\.md)`?", record):
        allowed.add(token)
    strayed = [path for path in ctx["diff"] if path not in allowed]
    if strayed:
        return "open", "the working tree has changes outside the record: " + ", ".join(strayed[:6])
    return "clear", "nothing outside the record is changed in the working tree" if ctx["diff"] else "the working tree is clean"


MECHANICAL = {
    "check:ledger-shape": c_ledger_shape,
    "check:stamp-present": c_stamp_present,
    "check:stamp-range": c_stamp_range,
    "check:stamp-ahead": c_stamp_ahead,
    "check:range-empty-said": c_range_empty_said,
    "check:changelog-reachable": c_changelog_reachable,
    "check:row-state-legal": c_row_state_legal,
    "check:row-evidence": c_row_evidence,
    "check:na-vs-tree": c_na_vs_tree,
    "check:row-per-gate": c_row_per_gate,
    "check:recorded-age": c_recorded_age,
    "check:mocked-clock": c_mocked_clock,
    "check:second-table": c_second_table,
    "check:pr-report-row": c_pr_report_row,
    "check:rule-bound-row": c_rule_bound_row,
    "check:run-row": c_run_row,
    "check:sketch-row": c_sketch_row,
    "check:picture-row": c_picture_row,
    "check:skill-names": c_skill_names,
    "check:deferred-clock": c_deferred_clock,
    "check:hook-no-row": c_hook_no_row,
    "check:record-only": c_record_only,
}


# --- the judgment lines, pre-filled -----------------------------------------


COMMAND_VERB = re.compile(r"^(gh|glab|git|curl|az|aws|docker|npm|npx|pnpm|yarn|make|python3?|pytest|go|cargo|bundle|mvn|gradle|dotnet)\b")
FENCE = re.compile(r"```[^\n]*\n(.*?)```", re.DOTALL)


def commands_in(text: str) -> list[str]:
    """The commands a piece of the bindings names — a fenced block first, inline mentions after.

    A fenced block is the read-back; an inline mention is prose about it, and
    the prose is where a section says which older command to expect nothing from.
    """
    fenced = [line.strip().split("  #", 1)[0].strip() for block in FENCE.findall(text) for line in block.splitlines()]
    inline = re.findall(r"`([^`\n]+)`", re.sub(FENCE, "", text))
    return [c for c in fenced + inline if COMMAND_VERB.match(c)]


def j_entry_moved_here(ctx: dict) -> tuple[str, str]:
    between = range_between(ctx)
    if not between:
        return "n/a", "no entries between the stamp and the plugin installed"
    return "unanswered", f"read: CHANGELOG.md entries {', '.join(reversed(between))} — which moved something this repository holds? one line each"


def j_row_uncovered(ctx: dict) -> tuple[str, str]:
    inv = ctx["inventory"]
    named: list[str] = []
    for row in ctx["gates"]:
        if row["state"] == "automated":
            named += [lang for lang in ("python", "typescript", "javascript", "go", "rust", "ruby", "java", "kotlin", "php", "elixir", "swift") if lang in row["text"].lower()]
    tree = ", ".join(inv["languages"]) or "no manifest recognised"
    rows = ", ".join(sorted(set(named))) or "no language named"
    labels = " ".join(row["label"].lower() + " " + row["text"].lower() for row in ctx["bounds"])
    unnamed = [hint for hint in inv["boundaries"] if hint.split()[-1] not in labels]
    tail = f"; the dependencies reach {', '.join(unnamed)} and no boundary row names it" if unnamed else ""
    return "unanswered", f"tree by manifests: {tree}; top-level: {', '.join(inv['dirs']) or '—'}; the automated rows name: {rows}{tail} — is what each row leaves uncovered named, and true?"


def coverage_rows(ctx: dict) -> list[tuple[str, str]]:
    return [(k, v) for k, v in ctx["keys"].items() if "coverage" in k]


def j_number_from_config(ctx: dict) -> tuple[str, str]:
    rows = coverage_rows(ctx)
    if not rows or all(re.search(r"\bnone\b|not applicable", v.lower()) for _, v in rows):
        return "n/a", "no coverage gate here"
    configs = [c for _, v in rows for c in re.findall(r"`([\w./-]+\.(?:json|js|ts|toml|cfg|ini|yaml|yml|xml))`", v)]
    return "unanswered", ("open: " + ", ".join(configs) if configs else "the coverage rows name no config file — open the one the gate reads") + " — read the demand from it, not from the row"


def j_demand_is_a_ratchet(ctx: dict) -> tuple[str, str]:
    rows = coverage_rows(ctx)
    if not rows or all(re.search(r"\bnone\b|not applicable", v.lower()) for _, v in rows):
        return "n/a", "no coverage gate here"
    cmds = [c for _, v in rows for c in commands_in(v)]
    return "unanswered", ("run: " + cmds[0] if cmds else "run the coverage command the bindings name") + " — is the demand today's score (a ratchet), or the whole of what is in scope?"


def j_exclusions_in_config(ctx: dict) -> tuple[str, str]:
    rows = coverage_rows(ctx)
    if not rows or all(re.search(r"\bnone\b|not applicable", v.lower()) for _, v in rows):
        return "n/a", "no coverage gate here"
    listed = [k for k, _ in rows if "not reach" in k or "not cover" in k]
    return "unanswered", ("the bindings list what coverage does not reach under *" + listed[0] + "*; " if listed else "") + "does the tool's own config exclude the same, or is the list here the only copy?"


def boundary_lines(ctx: dict, state: str, ask: str) -> tuple[str, str]:
    rows = [row for row in ctx["bounds"] if row["state"] == state]
    if not rows:
        return "n/a", f"no boundary row reads {state}"
    parts = []
    for row in rows:
        cmds = commands_in(row["text"])
        parts.append(f"{row['id'] or row['label']}: " + (f"run: {cmds[0]}" if cmds else "the row names no command; name what starts it"))
    return "unanswered", f"{ask} — " + "; ".join(parts)


def j_real_starts_here(ctx: dict) -> tuple[str, str]:
    return boundary_lines(ctx, "real", "does what the row names start from here?")


def j_real_not_doubled(ctx: dict) -> tuple[str, str]:
    if not any(row["state"] == "real" for row in ctx["bounds"]):
        return "n/a", "no boundary row reads real"
    trace = ctx["keys"].get("traceability gate", "")
    cmds = commands_in(trace)
    return "unanswered", (f"run your traceability gate: {cmds[0]}" if cmds else "run the traceability gate the bindings name") + " — does any rule-bound test stand a double in for a real boundary?"


def j_fake_suite_green(ctx: dict) -> tuple[str, str]:
    return boundary_lines(ctx, "fake", "does the suite against the real thing exist, and when was it last green?")


def platform_line(ctx: dict, question: str) -> tuple[str, str]:
    text = section(ctx["text"], "Branch protection") or ""
    cmds = commands_in(text)
    if not cmds:
        for key in ("required checks", "branch protection"):
            cmds += commands_in(ctx["keys"].get(key, ""))
    if cmds:
        return "unanswered", f"run: {cmds[0]} — {question}"
    return "unanswered", f"{question} — the bindings name no read-back command; the row must name one before this can be read"


def j_merge_blocked(ctx: dict) -> tuple[str, str]:
    return platform_line(ctx, "is a merge actually blocked when the required check fails?")


def j_check_name(ctx: dict) -> tuple[str, str]:
    return platform_line(ctx, "is the required check's name the one the platform has, not the workflow's filename?")


def j_who_bypasses(ctx: dict) -> tuple[str, str]:
    return platform_line(ctx, "who can bypass, tokens and keys included?")


def j_credentials_present(ctx: dict) -> tuple[str, str]:
    missing = re.compile(r"\b(token|credential|secret|key)s?\b[^.|]{0,40}\b(is missing|is not set|does not exist|is absent|unset)\b|\b(missing|no)\s+(token|secret)\b")
    claims = [f"L{n}" for n, line in enumerate(ctx["text"].splitlines(), 1) if missing.search(line.lower())]
    if not claims:
        return "n/a", "the bindings claim no credential is missing"
    return platform_line(ctx, f"the bindings claim a credential is missing at {', '.join(claims[:4])} — is it present where the platform keeps it?")


def j_word_not_a_skill(ctx: dict) -> tuple[str, str]:
    old_names = [f"{f}:{n} `{w}` (now `{FORMER_SKILLS[w]}`)" for f, n, w in skill_hits(ctx) if w in FORMER_SKILLS and w not in ctx["skills"]]
    prose = [f"{f}:{n} `{w}`" for f, n, w in skill_hits(ctx) if w in ctx["skills"] and not re.search(rf"/livespec:{w}\b", (ctx["claude_md"] if f == "CLAUDE.md" else ctx["text"]).splitlines()[n - 1])]
    if not old_names and not prose:
        return "n/a", "no skill name appears as ordinary prose"
    parts = []
    if old_names:
        parts.append("a name this plugin no longer has, in prose: " + ", ".join(old_names[:6]) + " — an instruction to correct, or a dated account to leave as written?")
    if prose:
        parts.append("confirm these are the word as prose and leave them alone: " + ", ".join(prose[:8]))
    return "unanswered", " · ".join(parts)


def j_loop_per_claude_md(ctx: dict) -> tuple[str, str]:
    if not ctx["claude_md"]:
        return "unanswered", "no CLAUDE.md at the root — read method/claude-md.md for what the loop's account must carry"
    return "unanswered", f"read CLAUDE.md ({len(ctx['claude_md'].splitlines())} lines) against method/claude-md.md — does each step say what the method now asks of it?"


def j_generated(ctx: dict) -> tuple[str, str]:
    return "unanswered", "generated by --validate from the finished record — leave this line as it is"


JUDGMENT = {
    "check:entry-moved-here": j_entry_moved_here,
    "check:prose-phrases": j_prose_phrases,
    "check:row-uncovered": j_row_uncovered,
    "check:number-from-config": j_number_from_config,
    "check:demand-is-a-ratchet": j_demand_is_a_ratchet,
    "check:exclusions-in-config": j_exclusions_in_config,
    "check:real-starts-here": j_real_starts_here,
    "check:real-not-doubled": j_real_not_doubled,
    "check:fake-suite-green": j_fake_suite_green,
    "check:merge-blocked": j_merge_blocked,
    "check:check-name": j_check_name,
    "check:who-bypasses": j_who_bypasses,
    "check:credentials-present": j_credentials_present,
    "check:word-not-a-skill": j_word_not_a_skill,
    "check:loop-per-claude-md": j_loop_per_claude_md,
}


# --- the record --------------------------------------------------------------


def emit(ctx: dict) -> list[dict[str, str]]:
    """One line per check id, in the registry's order."""
    lines: list[dict[str, str]] = []
    for check_id, kind, severity, _ in CHECKS:
        if check_id in GENERATED:
            state, evidence = j_generated(ctx)
            who = "reply"
        elif kind == "mechanical":
            state, evidence = MECHANICAL[check_id](ctx)
            who = "script"
        else:
            state, evidence = JUDGMENT[check_id](ctx)
            who = "model" if state == "unanswered" else "script"
        lines.append({"id": check_id, "state": state, "severity": severity, "evidence": evidence, "who": who})
    return lines


def render(ctx: dict, lines: list[dict[str, str]]) -> str:
    today = date.today().isoformat()
    head = f"**Audited {today} · livespec {ctx['installed'] or '?'} · stamp {ctx['stamp'] or 'none'} · HEAD {ctx['head'] or '?'}**"
    answered = sum(1 for line in lines if line["state"] != "unanswered")
    out = ["# Audit record", "", head, "", f"{len(lines)} checks · {answered} answered by the script · {len(lines) - answered} for a mind", "",
           "| id | state | since | evidence |", "|---|---|---|---|"]
    for line in lines:
        evidence = line["evidence"].replace("|", "\\|")
        out.append(f"| `{line['id']}` | {line['state']} | {today} | {evidence} · ← {line['who']} |")
    return "\n".join(out) + "\n"


def reshape(ctx: dict) -> str:
    """The three tables in the template's shape, rows verbatim, ids from the aliases."""
    out: list[str] = []
    out.append(f"**Reconciled against livespec {ctx['stamp'] or '<version>'} on {ctx['stamp_date'] or '<date>'}.**\n")
    out.append("| id | gate | state | evidence |\n|---|---|---|---|")
    present: set[str] = set()
    for row in ctx["gates"]:
        row_id = row["id"]
        if not row_id:
            hits = match_alias(row["label"], GATES)
            row_id = hits[0] if len(hits) == 1 else (f"local:<{'|'.join(hits) if hits else 'name'}>")
        present.add(row_id)
        out.append(f"| `{row_id}` | {row['label']} | {row['state'] or '<state>'} | {row['evidence']} |")
    for gate_id, _, _, meaning in GATES:
        if gate_id not in present:
            out.append(f"| `{gate_id}` | {meaning} | <state> | <command, or why not> |")
    out.append("\n### The wiring that must never gate\n\n| id | wiring | state | evidence |\n|---|---|---|---|")
    for row in ctx["wiring"]:
        hits = match_alias(row["label"], WIRING)
        row_id = row["id"] or (hits[0] if len(hits) == 1 else "wiring:<name>")
        out.append(f"| `{row_id}` | {row['label']} | {row['state'] or '<state>'} | {row['evidence']} |")
    out.append("\n### The boundaries\n\n| id | boundary | state | since | evidence |\n|---|---|---|---|---|")
    for row in ctx["bounds"]:
        since = re.search(r"\b(\d{4})\b", row["text"])
        slug = re.sub(r"[^a-z0-9]+", "-", row["label"].lower()).strip("-") or "name"
        out.append(f"| `{row['id'] or 'boundary:' + slug}` | {row['label']} | {row['state'] or '<state>'} | {since.group(1) if since else '<change>'} | {row['evidence']} |")
    return "\n".join(out) + "\n"


# --- pass two: the refusal, the record, the reply ----------------------------

FINAL_STATES = ("clear", "open", "not-read", "n/a")
COMMAND_MARK = re.compile(r"`[^`]+`|\brun:|\bread:")
RECORD_HEAD = re.compile(r"\*\*Audited (\d{4}-\d{2}-\d{2}) · livespec (\S+) · stamp (\S+) · HEAD (\S+)(?: · audit (\d+))?\*\*")
JUDGMENT_IDS = {check_id for check_id, kind, _, _ in CHECKS if kind == "judgment"}


def parse_record(text: str) -> tuple[dict, list[dict[str, str]]]:
    """The header and the lines of a record, in either pass's shape."""
    header: dict = {"date": "", "audit": 0}
    match = RECORD_HEAD.search(text)
    if match:
        header = {"date": match.group(1), "audit": int(match.group(5) or 0)}
    lines: list[dict[str, str]] = []
    for raw in text.splitlines():
        if not raw.startswith("| `check:"):
            continue
        cells = cells_of(raw)
        if len(cells) < 4:
            cells += [""] * (4 - len(cells))
        evidence = re.sub(r"\s*·\s*←\s*(script|model|reply)\s*$", "", cells[3]).replace("\\|", "|")
        lines.append({"id": cells[0].strip("`"), "state": cells[1], "since": cells[2], "evidence": evidence})
    return header, lines


def record_path_of(ctx: dict) -> Path:
    """Where the bindings say the record lives; the template's default otherwise."""
    named = re.search(r"([\w./-]+\.md)", ctx["keys"].get("audit record", ""))
    return ctx["root"] / (named.group(1) if named else "specs/setup/audit.md")


def generated_lines(rows: dict[str, dict[str, str]]) -> tuple[list[str], dict[str, tuple[str, str]]]:
    """The four lines the reply generates, and the refusals reading them raised."""
    problems: list[str] = []
    read_back = not_read = 0
    for check_id in JUDGMENT_IDS:
        row = rows.get(check_id)
        if row is None:
            continue
        if row["state"] in ("clear", "open"):
            if not COMMAND_MARK.search(row["evidence"]):
                problems.append(f"{check_id} reads {row['state']} with no command beside it — a judgment carries how it was reached")
            read_back += 1
        elif row["state"] == "not-read":
            if not row["evidence"].strip():
                problems.append(f"{check_id} reads not-read and gives no reason")
            not_read += 1
    wiring_open = [r["id"] for r in rows.values() if r["state"] == "open" and severity_of(r["id"]) == "wiring"]
    answers = {
        "check:read-back-or-not": ("clear", f"{read_back} judgment line(s) read back with their command, {not_read} not read with why")
        if not problems else ("open", "; ".join(problems)),
        "check:sorted-by-severity": ("clear", "the reply lists what is open platform › boundary › wiring › record"),
        "check:last-line-command": ("clear", f"printed — {len(wiring_open)} open line(s) name wiring: {', '.join(wiring_open)}")
        if wiring_open else ("n/a", "nothing is left for the sitting"),
        "check:no-line-when-clear": ("clear", "no line sends anybody to a sitting") if not wiring_open else ("n/a", "wiring is left, and the last line says so"),
    }
    return problems, answers


def severity_of(check_id: str) -> str:
    return next((s for i, _, s, _ in CHECKS if i == check_id), "record")


def refusals(ctx: dict, rows: dict[str, dict[str, str]], record_path: Path) -> list[str]:
    problems: list[str] = []
    expected = [check_id for check_id, _, _, _ in CHECKS]
    for check_id in expected:
        if check_id not in rows:
            problems.append(f"missing: {check_id}")
    for check_id in rows:
        if check_id not in expected:
            problems.append(f"{check_id} is not a check the method has")
    for check_id, row in rows.items():
        if check_id in GENERATED:
            continue
        if row["state"] == "unanswered":
            problems.append(f"still unanswered: {check_id}")
        elif row["state"] not in FINAL_STATES:
            problems.append(f"unknown state {row['state']!r} on {check_id} — one of clear · open · not-read · n/a")
        elif row["state"] == "open" and not row["evidence"].strip():
            problems.append(f"{check_id} is open with nothing that closes it")
        elif row["state"] == "not-read" and not row["evidence"].strip():
            problems.append(f"{check_id} reads not-read and gives no reason")
    problems += generated_lines(rows)[0]
    allowed = {"CLAUDE.md"}
    for path in (ctx["bindings_path"], record_path):
        try:
            allowed.add(str(path.resolve().relative_to(ctx["root"].resolve())))
        except ValueError:
            allowed.add(path.name)
    strayed = [path for path in ctx["diff"] if path not in allowed]
    if strayed:
        problems.append("the working tree changed more than the record: " + ", ".join(strayed[:6]) + " — doctor wires nothing")
    return problems


def carry_since(lines: list[dict[str, str]], previous: list[dict[str, str]], today: str) -> None:
    before = {row["id"]: row for row in previous}
    for row in lines:
        old = before.get(row["id"])
        row["since"] = old["since"] if old and old["state"] == row["state"] and old["since"] else today


def render_record(ctx: dict, lines: list[dict[str, str]], audit: int, today: str) -> str:
    head = f"**Audited {today} · livespec {ctx['installed'] or '?'} · stamp {ctx['stamp'] or 'none'} · HEAD {ctx['head'] or '?'} · audit {audit}**"
    opened = sum(1 for row in lines if row["state"] == "open")
    out = ["# Audit record", "", head, "", f"{len(lines)} checks · {opened} open · written by the audit, replaced on every run", "",
           "| id | state | since | evidence |", "|---|---|---|---|"]
    for row in lines:
        out.append(f"| `{row['id']}` | {row['state']} | {row['since']} | {row['evidence'].replace('|', '\\|')} |")
    return "\n".join(out) + "\n"


def reply(ctx: dict, lines: list[dict[str, str]], previous: list[dict[str, str]], previous_date: str, today: str) -> str:
    by_id = {row["id"]: row for row in lines}
    order = {name: index for index, name in enumerate(SEVERITY_ORDER)}
    opened = sorted((r for r in lines if r["state"] == "open"), key=lambda r: (order[severity_of(r["id"])], r["id"]))
    unread = sorted((r for r in lines if r["state"] == "not-read"), key=lambda r: (order[severity_of(r["id"])], r["id"]))
    before = {row["id"]: row for row in previous}
    out = [f"# Audit — {today} · livespec {ctx['installed'] or '?'} · stamp {ctx['stamp'] or 'none'}", ""]
    if previous:
        newly = [r["id"] for r in opened if before.get(r["id"], {}).get("state") != "open"]
        closed = [i for i, r in before.items() if r["state"] == "open" and by_id.get(i, {}).get("state") not in ("open", None)]
        same = sum(1 for r in lines if before.get(r["id"], {}).get("state") == r["state"])
        oldest = min(opened, key=lambda r: r["since"]) if opened else None
        out.append(
            f"Since {previous_date or 'the previous audit'}: {len(newly)} opened · {len(closed)} closed · {same} unchanged"
            + (f" · oldest open: {oldest['id']}, since {oldest['since']}" if oldest else "")
            + (f" · closed: {', '.join(closed)}" if closed else "")
        )
    else:
        out.append("First audit here — nothing to compare against.")
    out += ["", f"## Open — {len(opened)}", ""]
    out += [f"- `{r['id']}` ({severity_of(r['id'])}) — {r['evidence']}" for r in opened] or ["- nothing"]
    out += ["", f"## Not read — {len(unread)}", ""]
    out += [f"- `{r['id']}` — {r['evidence']}" for r in unread] or ["- nothing"]
    decided = [r for r in all_rows(ctx) if r["decided"]]
    out += ["", f"## Decided — {len(decided)}", ""]
    for row in decided:
        note = ""
        for layer, word in LAYER_WORDS.items():
            if re.search(rf"\bno {word}s?\b", row["text"].lower()) and ctx["layers"][layer]:
                note = f" — evidence for a mind: specs/{layer}/ has {len(ctx['layers'][layer])} file(s)"
        out.append(f"- `{row['id'] or row['label']}` — {row['state'] or 'state unreadable'}: {row['evidence'][:100]}{note}")
    if not decided:
        out.append("- none")
    wiring_open = [r for r in opened if severity_of(r["id"]) == "wiring"]
    if wiring_open:
        out += ["", "## For the sitting", "", "/livespec:setup"]
        out += [f"  {r['id']} — {r['evidence'][:100]}" for r in wiring_open]
    return "\n".join(out) + "\n"


def validate(ctx: dict, finished: Path, write: bool = True) -> tuple[list[str], str, str]:
    """Refuse the finished record, or write it where the bindings say and return the reply.

    With `write` false — `--check` — the same refusals and the same exit, and
    nothing touched: what a grader asks of the record a session left.
    """
    today = date.today().isoformat()
    _, lines = parse_record(read(finished) or "")
    rows = {row["id"]: row for row in lines}
    problems = refusals(ctx, rows, record_path_of(ctx))
    if problems or not write:
        return problems, "", ""
    _, answers = generated_lines(rows)
    for check_id, (state, evidence) in answers.items():
        rows[check_id]["state"], rows[check_id]["evidence"] = state, evidence
    ordered = [rows[check_id] for check_id, _, _, _ in CHECKS]
    record_path = record_path_of(ctx)
    previous_text = "" if finished.resolve() == record_path.resolve() else (read(record_path) or "")
    previous_head, previous = parse_record(previous_text)
    carry_since(ordered, previous, today)
    text = render_record(ctx, ordered, previous_head["audit"] + 1, today)
    record_path.parent.mkdir(parents=True, exist_ok=True)
    record_path.write_text(text, encoding="utf-8")
    return [], text, reply(ctx, ordered, previous, previous_head["date"], today)


def main(argv: list[str]) -> int:
    global PLUGIN
    if "--plugin" in argv:
        at = argv.index("--plugin")
        PLUGIN = Path(argv[at + 1]).resolve()
        argv = argv[:at] + argv[at + 2:]
    finished: Path | None = None
    write = True
    for flag in ("--validate", "--check"):
        if flag in argv:
            at = argv.index(flag)
            finished = Path(argv[at + 1]).resolve()
            write = flag == "--validate"
            argv = argv[:at] + argv[at + 2:]
    args = [a for a in argv if not a.startswith("--")]
    flags = {a for a in argv if a.startswith("--")}
    if "--registry" in flags:
        for row in registry():
            print(f"| `{row['id']}` | {row['kind']} | — | {row['severity']} | — | {row['aliases']} | {row['meaning']} |")
        return 0
    root = Path.cwd()
    bindings_path = Path(args[0]).resolve() if args else root / "specs" / "setup" / "README.md"
    if not bindings_path.exists():
        print(f"no bindings at {bindings_path} — this repository has never had the process set up. Run: /livespec:setup")
        return 3
    ctx = context(root, bindings_path)
    if "--reshape" in flags:
        print(reshape(ctx), end="")
        return 0
    if finished is not None:
        if not finished.exists():
            print(f"no record at {finished} to validate", file=sys.stderr)
            return 1
        problems, _, answer = validate(ctx, finished, write=write)
        if problems:
            print("✘ the record is refused — the audit has not finished:\n", file=sys.stderr)
            for problem in problems:
                print(f"  ✘ {problem}", file=sys.stderr)
            return 1
        if not write:
            print(f"✔ the record at {finished} validates — nothing written")
            return 0
        print(answer, end="")
        return 0
    print(render(ctx, emit(ctx)), end="")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

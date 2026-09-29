#!/usr/bin/env python3
"""This repository's trees: one home, one command, and a clean that cannot lose work.

    python3 .github/scripts/trees.py new <name> [--from <ref>]
    python3 .github/scripts/trees.py list
    python3 .github/scripts/trees.py clean [--dry-run] [--force <name>]

Every tree lives in `.worktrees/<name>/` under the main checkout, on a branch of
the same name, whichever tree the command is run from. A fresh tree here needs
nothing after `git worktree add`: the gates are standard library, and
`core.hooksPath` is shared config pointing at the tracked `.githooks`.

`list` and `clean` read git's own record of the trees, not the directory, so a
tree an agent harness made anywhere else is listed and cleaned with the rest.
`clean` removes a tree only when it has nothing to lose — no uncommitted or
untracked files, every commit on the main branch or its upstream deleted after
merging, not locked, not the tree it is run from — and takes the branch only
when `git branch -d` agrees it is merged. Everything else is listed with why it
stayed. See specs/changes/0073.

Standard library only, like the gates.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

HOME = ".worktrees"


def git(*args: str, cwd: Path | None = None, check: bool = True) -> str:
    result = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True)
    if check and result.returncode != 0:
        raise SystemExit(f"git {' '.join(args)}: {result.stderr.strip() or result.stdout.strip()}")
    return result.stdout.strip()


def main_checkout() -> Path:
    """The main tree, from any tree: the parent of the shared git directory."""
    common = Path(git("rev-parse", "--path-format=absolute", "--git-common-dir"))
    return common.parent


def main_branch(root: Path) -> str:
    """The branch everything merges into — origin's HEAD where it is known, else main."""
    head = git("symbolic-ref", "--quiet", "--short", "refs/remotes/origin/HEAD", cwd=root, check=False)
    return head or "main"


def trees(root: Path) -> list[dict]:
    """Every linked tree git knows about, with the facts `safe()` decides on."""
    found: list[dict] = []
    record: dict = {}
    for line in git("worktree", "list", "--porcelain", cwd=root).splitlines() + [""]:
        if not line:
            if record:
                found.append(record)
            record = {}
            continue
        key, _, value = line.partition(" ")
        record[key] = value or True
    base = main_branch(root)
    here = Path(git("rev-parse", "--show-toplevel")).resolve()
    out: list[dict] = []
    for record in found[1:]:  # the first is the main checkout
        path = Path(record["worktree"])
        branch = str(record.get("branch", "")).removeprefix("refs/heads/")
        exists = path.is_dir()
        dirty = len(git("status", "--porcelain", cwd=path, check=False).splitlines()) if exists else 0
        merged = bool(branch) and subprocess.run(
            ["git", "merge-base", "--is-ancestor", branch, base], cwd=root, capture_output=True).returncode == 0
        track = git("for-each-ref", "--format=%(upstream:track)", f"refs/heads/{branch}", cwd=root, check=False) if branch else ""
        out.append({
            "path": path, "name": path.name, "branch": branch or "(detached)",
            "exists": exists, "current": exists and path.resolve() == here,
            "locked": "locked" in record, "dirty": dirty,
            "merged": merged, "gone": track == "[gone]",
        })
    return out


def safe(tree: dict) -> tuple[bool, str]:
    """Whether cleaning may remove a tree, and why — the rule is written as what it keeps."""
    if not tree["exists"]:
        return True, "its directory is already gone; only git's record of it remains"
    if tree["current"]:
        return False, "it is the tree this was run from"
    if tree["locked"]:
        return False, "it is locked"
    if tree["dirty"]:
        return False, f"{tree['dirty']} uncommitted or untracked file(s)"
    if tree["branch"] == "(detached)":
        return False, "no branch to say whether its work is merged"
    if not (tree["merged"] or tree["gone"]):
        return False, "commits not on the main branch"
    return True, "clean, merged" if tree["merged"] else "clean, its upstream deleted after merging"


def new(root: Path, name: str, start: str | None) -> None:
    path = root / HOME / name
    if path.exists():
        raise SystemExit(f"{path} already exists — `list` shows what is in it")
    base = start or main_branch(root)
    git("worktree", "add", str(path), "-b", name, base, cwd=root)
    print(f"{path}  on {name}, from {base}")
    print("ready: nothing else to do here — the gates are standard library and the hook is shared config")


def show(root: Path) -> list[tuple[dict, bool, str]]:
    rows = [(t, *safe(t)) for t in trees(root)]
    if not rows:
        print("no trees besides the main checkout")
        return rows
    width = max(len(t["name"]) for t, _, _ in rows)
    for tree, ok, why in rows:
        print(f"{tree['name']:<{width}}  {tree['branch']:<40}  {'safe ' if ok else 'KEEP '} {why}")
    count = sum(1 for _, ok, _ in rows if ok)
    print(f"\n{len(rows)} tree(s) · {count} safe to remove" + (" · run: trees.py clean" if count else ""))
    return rows


def clean(root: Path, dry_run: bool, force: str | None) -> None:
    for tree, ok, why in [(t, *safe(t)) for t in trees(root)]:
        forced = force is not None and tree["name"] == force and not tree["current"]
        if not (ok or forced):
            print(f"kept     {tree['name']} — {why}")
            continue
        if dry_run:
            print(f"would go {tree['name']} — {why if ok else 'forced'}")
            continue
        if tree["exists"]:
            git("worktree", "remove", *(["--force"] if forced else []), str(tree["path"]), cwd=root)
        else:
            git("worktree", "prune", cwd=root)
        branch = tree["branch"]
        took = branch != "(detached)" and subprocess.run(
            ["git", "branch", "-d", branch], cwd=root, capture_output=True).returncode == 0
        print(f"removed  {tree['name']}" + (f" and branch {branch}" if took else f" (branch {branch} kept: git branch -d refused)"))


def main(argv: list[str]) -> int:
    if not argv or argv[0] not in ("new", "list", "clean"):
        print("\n".join(__doc__.strip().splitlines()[2:5]))
        return 2
    root = main_checkout()
    verb, rest = argv[0], argv[1:]
    if verb == "new":
        if not rest:
            raise SystemExit("new needs a name — the branch and the tree take it")
        start = rest[rest.index("--from") + 1] if "--from" in rest else None
        new(root, rest[0], start)
    elif verb == "list":
        show(root)
    else:
        force = rest[rest.index("--force") + 1] if "--force" in rest else None
        clean(root, "--dry-run" in rest, force)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

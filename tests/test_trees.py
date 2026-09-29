"""This repository's trees command, held to what `clean` may remove. Standard library.

Each test builds a real repository in a temporary directory with a `main`
branch and linked trees in the states that matter, then runs
`.github/scripts/trees.py` inside it and reads what is left. Git's own
environment variables are cleared first, so nothing here follows a hook's
`GIT_DIR` onto the real branch (#127). See specs/changes/0073.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

from rulelib import rule  # noqa: E402

TREES = ROOT / ".github" / "scripts" / "trees.py"
ENV = {k: v for k, v in os.environ.items() if k not in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE")}
ENV.update({"GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t", "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t"})


def sh(cwd: Path, *args: str) -> str:
    result = subprocess.run(list(args), cwd=cwd, env=ENV, capture_output=True, text=True)
    if result.returncode != 0:
        raise AssertionError(f"{' '.join(args)}: {result.stderr}")
    return result.stdout


def trees(cwd: Path, *args: str) -> str:
    result = subprocess.run([sys.executable, str(TREES), *args], cwd=cwd, env=ENV, capture_output=True, text=True)
    if result.returncode != 0:
        raise AssertionError(f"trees.py {' '.join(args)} exited {result.returncode}: {result.stderr}{result.stdout}")
    return result.stdout


def listed(cwd: Path) -> set[str]:
    return {Path(line.split(" ", 1)[1]).name for line in sh(cwd, "git", "worktree", "list", "--porcelain").splitlines()
            if line.startswith("worktree ")}


class Clean(unittest.TestCase):
    def setUp(self):
        self.base = Path(tempfile.mkdtemp(prefix="trees-"))
        self.root = self.base / "repo"
        self.root.mkdir()
        sh(self.root, "git", "init", "-q", "-b", "main")
        (self.root / "a.txt").write_text("a\n")
        sh(self.root, "git", "add", "a.txt")
        sh(self.root, "git", "commit", "-q", "-m", "first")
        for name in ("merged", "dirty", "ahead", "here"):
            trees(self.root, "new", name)
        (self.root / ".worktrees" / "dirty" / "wip.txt").write_text("unsaved\n")
        ahead = self.root / ".worktrees" / "ahead"
        (ahead / "b.txt").write_text("b\n")
        sh(ahead, "git", "add", "b.txt")
        sh(ahead, "git", "commit", "-q", "-m", "not on main")

    def tearDown(self):
        shutil.rmtree(self.base, ignore_errors=True)

    @rule("clean-removes-only-what-is-safe")
    def test_only_the_tree_with_nothing_to_lose_goes_and_its_branch_with_it(self):
        out = trees(self.root / ".worktrees" / "here", "clean")
        left = listed(self.root)
        self.assertNotIn("merged", left, out)
        self.assertNotIn("merged", sh(self.root, "git", "branch", "--list", "merged"), "a merged branch outlived its tree")
        for kept in ("dirty", "ahead", "here"):
            self.assertIn(kept, left, f"{kept} was removed:\n{out}")
        self.assertIn("kept     dirty — 1 uncommitted or untracked file(s)", out)
        self.assertIn("kept     ahead — commits not on the main branch", out)
        self.assertIn("kept     here — it is the tree this was run from", out)
        self.assertTrue((self.root / ".worktrees" / "dirty" / "wip.txt").exists(), "uncommitted work was lost")

    @rule("clean-removes-only-what-is-safe")
    def test_a_tree_made_outside_the_home_is_listed_from_gits_own_record(self):
        sh(self.root, "git", "worktree", "add", "-q", str(self.base / "elsewhere"), "-b", "elsewhere")
        out = trees(self.root, "list")
        self.assertIn("elsewhere", out)
        self.assertIn("5 tree(s)", out)

    @rule("clean-removes-only-what-is-safe")
    def test_a_dry_run_removes_nothing(self):
        before = listed(self.root)
        out = trees(self.root, "clean", "--dry-run")
        self.assertIn("would go merged", out)
        self.assertEqual(before, listed(self.root))


if __name__ == "__main__":
    unittest.main()

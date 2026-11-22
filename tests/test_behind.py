"""The hint, tools/behind.py. See specs/changes/0108."""

from __future__ import annotations

import json
import os
import sys
import tempfile
import time
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / ".github" / "scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import behind  # noqa: E402
import inject  # noqa: E402
from rulelib import rule  # noqa: E402

LOADED = behind.loaded()


def repo(version: str | None) -> Path:
    root = Path(tempfile.mkdtemp(prefix="behind-"))
    if version:
        (root / "specs" / "setup").mkdir(parents=True)
        (root / "specs" / "setup" / "README.md").write_text(inject.green_bindings(version))
    return root


class TheHint(unittest.TestCase):
    def setUp(self):
        self.cache = Path(tempfile.mkdtemp()) / "latest.json"
        patcher = mock.patch.object(behind, "CACHE", self.cache)
        patcher.start()
        self.addCleanup(patcher.stop)
        os.environ.pop("LIVESPEC_NO_HINT", None)

    @rule("the-hint-is-the-persons-alone")
    def test_items_pending_are_counted_with_the_command(self):
        line = behind.hint(repo("0.0.1"), "pi")
        self.assertRegex(line, r"\d+ pending · /skill:setup brings it up to date")

    @rule("the-hint-is-the-persons-alone")
    def test_an_older_session_is_said_first(self):
        line = behind.hint(repo("999.0.0"), "claude")
        self.assertIn(f"this session loads {LOADED}; this repository is at 999.0.0", line)

    @rule("the-hint-is-the-persons-alone")
    def test_a_newer_release_is_named_when_nothing_is_pending(self):
        self.cache.write_text(json.dumps({"latest": "999.0.0", "at": time.time()}))
        with mock.patch.object(behind.doctor if hasattr(behind, "doctor") else __import__("doctor"), "planned", return_value=[]):
            line = behind.hint(repo(LOADED), "pi")
        self.assertEqual(line, f"livespec 999.0.0 released (loaded {LOADED}) · pi update")

    @rule("the-hint-is-the-persons-alone")
    def test_a_pinned_repository_is_told_to_move_its_pin(self):
        self.cache.write_text(json.dumps({"latest": "999.0.0", "at": time.time()}))
        root = repo(LOADED)
        (root / ".pi").mkdir()
        (root / ".pi" / "settings.json").write_text('{"packages": ["git:github.com/sargismarkosyan/livespec@livespec--v1.0.0"]}')
        with mock.patch.object(__import__("doctor"), "planned", return_value=[]):
            line = behind.hint(root, "pi")
        self.assertTrue(line.endswith("move the Pi pin, then pi update"), line)

    @rule("the-hint-is-the-persons-alone")
    def test_nothing_without_bindings_or_with_the_hint_off(self):
        self.assertEqual(behind.hint(repo(None), "pi"), "")
        with mock.patch.dict(os.environ, {"LIVESPEC_NO_HINT": "1"}), mock.patch("builtins.print") as printed:
            self.assertEqual(behind.main(["--root", str(repo("0.0.1"))]), 0)
        printed.assert_not_called()


if __name__ == "__main__":
    unittest.main()

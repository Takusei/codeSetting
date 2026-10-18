"""Test dependency installation with temporary homes and no network access."""

import contextlib
import io
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

from install_shell import install_repository


class ShellDependencyTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.target = self.root / "custom/plugin"
        self.marker = "plugin.zsh"
        silence = contextlib.redirect_stdout(io.StringIO())
        silence.__enter__()
        self.addCleanup(silence.__exit__, None, None, None)

    def install(self, apply=True):
        install_repository("example/plugin", self.target, self.marker, apply)

    def test_preview_has_no_side_effects(self):
        with patch("install_shell.subprocess.run") as run:
            self.install(apply=False)
        run.assert_not_called()
        self.assertEqual(list(self.root.iterdir()), [])

    def test_install_then_rerun_preserves_local_changes(self):
        def clone(command, **kwargs):
            checkout = Path(command[-1])
            checkout.mkdir()
            (checkout / self.marker).write_text("upstream")
        with patch("install_shell.subprocess.run", side_effect=clone) as run:
            self.install()
            (self.target / self.marker).write_text("local edits")
            self.install()
        self.assertEqual(run.call_count, 1)
        self.assertEqual((self.target / self.marker).read_text(), "local edits")

    def test_conflicting_path_is_preserved(self):
        self.target.parent.mkdir()
        self.target.write_text("keep me")
        with patch("install_shell.subprocess.run") as run:
            with self.assertRaises(ValueError):
                self.install()
        run.assert_not_called()
        self.assertEqual(self.target.read_text(), "keep me")

    def test_failed_clone_is_cleaned_up_and_can_be_retried(self):
        def fail(command, **kwargs):
            Path(command[-1]).mkdir()
            raise subprocess.CalledProcessError(1, command)
        with patch("install_shell.subprocess.run", side_effect=fail):
            with self.assertRaises(subprocess.CalledProcessError):
                self.install()
        self.assertFalse(self.target.exists())
        self.assertEqual(list(self.target.parent.iterdir()), [])

    def test_incomplete_download_is_not_installed(self):
        with patch("install_shell.subprocess.run"):
            with self.assertRaises(ValueError):
                self.install()
        self.assertFalse(self.target.exists())


if __name__ == "__main__":
    unittest.main()

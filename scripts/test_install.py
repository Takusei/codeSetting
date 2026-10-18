"""Exercise file-preservation behavior using temporary homes only."""

import contextlib
import io
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from install import install_link


class InstallTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.source = self.root / "source"
        self.source.write_text("new settings")
        self.target = self.root / "home/config"
        self.silence = contextlib.redirect_stdout(io.StringIO())
        self.silence.__enter__()
        self.addCleanup(self.silence.__exit__, None, None, None)

    def test_preview_does_not_create_directories(self):
        install_link(self.source, self.target)
        self.assertFalse(self.target.parent.exists())

    def test_preserves_existing_file_and_is_idempotent(self):
        self.target.parent.mkdir()
        self.target.write_text("original settings")
        install_link(self.source, self.target, apply=True)
        install_link(self.source, self.target, apply=True)
        self.assertEqual(self.target.resolve(), self.source.resolve())
        backups = list(self.target.parent.glob("config.backup-*"))
        self.assertEqual(len(backups), 1)
        self.assertEqual(backups[0].read_text(), "original settings")

    def test_preserves_broken_symlink(self):
        self.target.parent.mkdir()
        self.target.symlink_to("missing-config")
        install_link(self.source, self.target, apply=True)
        backup = next(self.target.parent.glob("config.backup-*"))
        self.assertTrue(backup.is_symlink())
        self.assertEqual(str(backup.readlink()), "missing-config")

    def test_preserves_directory(self):
        self.target.mkdir(parents=True)
        (self.target / "custom.lua").write_text("original")
        install_link(self.source, self.target, apply=True)
        backup = next(self.target.parent.glob("config.backup-*"))
        self.assertEqual((backup / "custom.lua").read_text(), "original")

    def test_restores_backup_if_link_creation_fails(self):
        self.target.parent.mkdir()
        self.target.write_text("original")
        with patch.object(Path, "symlink_to", side_effect=OSError("failed")):
            with self.assertRaises(OSError):
                install_link(self.source, self.target, apply=True)
        self.assertEqual(self.target.read_text(), "original")


if __name__ == "__main__":
    unittest.main()

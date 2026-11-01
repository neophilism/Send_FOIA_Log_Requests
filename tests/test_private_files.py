import json
import os
from pathlib import Path
import sqlite3
import subprocess
import sys
import tempfile
import unittest

from foia_requests.config import Config, ConfigurationError
from foia_requests.migrations import initialize


class PrivateFileTests(unittest.TestCase):
    def test_database_private_modes_and_nested_directory_modes(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            path = root / "one" / "two" / "ledger.sqlite"
            initialize(path)
            self.assertEqual(path.stat().st_mode & 0o777, 0o600)
            self.assertEqual(path.parent.stat().st_mode & 0o777, 0o700)
            self.assertEqual(path.parent.parent.stat().st_mode & 0o777, 0o700)
            initialize(path)
            with sqlite3.connect(path) as conn:
                self.assertEqual(conn.execute("SELECT COUNT(*) FROM schema_events").fetchone()[0], 1)

    @unittest.skipUnless(hasattr(os, "symlink"), "symlink support required")
    def test_linked_database_and_config_rejected_without_touching_target(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            target = root / "target"
            target.write_text('{}')
            target.chmod(0o600)
            link = root / "link"
            link.symlink_to(target)
            with self.assertRaises(RuntimeError):
                initialize(link)
            with self.assertRaises(ConfigurationError):
                Config.from_file(link)
            self.assertEqual(target.read_text(), '{}')
            link.unlink()
            os.link(target, link)
            with self.assertRaises(RuntimeError):
                initialize(link)
            self.assertEqual(target.read_text(), '{}')

    def test_insecure_existing_directory_and_file_are_not_repaired_silently(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            public = root / "public"
            public.mkdir(mode=0o755)
            with self.assertRaisesRegex(RuntimeError, "private owned"):
                initialize(public / "ledger.sqlite")
            self.assertFalse((public / "ledger.sqlite").exists())
            path = root / "readable.sqlite"
            path.write_bytes(b'')
            path.chmod(0o644)
            with self.assertRaisesRegex(RuntimeError, "private regular"):
                initialize(path)
            self.assertEqual(path.stat().st_mode & 0o777, 0o644)

    @unittest.skipUnless(hasattr(os, "symlink"), "symlink support required")
    def test_symlink_ancestor_cannot_create_directories_outside_selected_tree(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            target = root / "target"
            target.mkdir(mode=0o700)
            (root / "alias").symlink_to(target, target_is_directory=True)
            with self.assertRaisesRegex(RuntimeError, "symlinks"):
                initialize(root / "alias" / "new" / "ledger.sqlite")
            self.assertFalse((target / "new").exists())

    @unittest.skipUnless(hasattr(os, "mkfifo"), "FIFO support required")
    def test_config_fifo_is_rejected_without_blocking(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "config.pipe"
            os.mkfifo(path)
            # Separate process gives this liveness regression a hard deadline.
            result = subprocess.run([sys.executable, '-m', 'foia_requests', '--config', str(path), 'draft'],
                                    capture_output=True, text=True, timeout=3)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('regular file', result.stderr)
            self.assertNotIn('Traceback', result.stderr)

    def test_deeply_nested_configuration_is_a_validation_error(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "config.json"
            path.write_text('[' * 1100 + '0' + ']' * 1100)
            with self.assertRaises(ConfigurationError):
                Config.from_file(path)

    def test_incompatible_existing_schema_is_not_accepted_or_rewritten(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'ledger.sqlite'
            with sqlite3.connect(path) as conn:
                conn.execute('CREATE TABLE schema_events(version INTEGER, applied_at TEXT)')
                conn.execute("INSERT INTO schema_events VALUES(1, 'synthetic')")
                conn.execute('PRAGMA user_version=1')
            path.chmod(0o600)
            with self.assertRaisesRegex(RuntimeError, 'incompatible migration schema'):
                initialize(path)
            with sqlite3.connect(path) as conn:
                self.assertEqual(conn.execute('SELECT applied_at FROM schema_events').fetchone()[0], 'synthetic')

    def test_concurrent_initializers_share_one_migration_event(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'nested' / 'ledger.sqlite'
            code = 'from foia_requests.migrations import initialize; import sys; initialize(sys.argv[1])'
            children = [subprocess.Popen([sys.executable, '-c', code, str(path)],
                                        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                        for _ in range(4)]
            for child in children:
                _, stderr = child.communicate(timeout=5)
                self.assertEqual(child.returncode, 0, stderr)
            with sqlite3.connect(path) as conn:
                self.assertEqual(conn.execute('SELECT COUNT(*) FROM schema_events').fetchone()[0], 1)


if __name__ == '__main__':
    unittest.main()

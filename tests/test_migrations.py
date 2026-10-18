import sqlite3
import tempfile
import unittest
from pathlib import Path
from foia_requests.migrations import initialize

class MigrationTests(unittest.TestCase):
    def test_idempotent(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "nested" / "ledger.sqlite"
            initialize(path)
            initialize(path)
            with sqlite3.connect(path) as conn:
                self.assertEqual(conn.execute("PRAGMA user_version").fetchone()[0], 1)
                self.assertEqual(conn.execute("SELECT COUNT(*) FROM schema_events").fetchone()[0], 1)

    def test_no_downgrade(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "ledger.sqlite"
            with sqlite3.connect(path) as conn:
                conn.execute("PRAGMA user_version=99")
            with self.assertRaises(RuntimeError):
                initialize(path)

"""Offline SQLite schema migration. No external services."""
import sqlite3
from pathlib import Path

SCHEMA_VERSION = 1

def initialize(path):
    location = Path(path)
    if str(location) != ":memory:":
        location.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(str(location)) as conn:
        version = conn.execute("PRAGMA user_version").fetchone()[0]
        if version > SCHEMA_VERSION:
            raise RuntimeError("unsupported future schema")
        if version < 1:
            conn.execute("CREATE TABLE IF NOT EXISTS schema_events (version INTEGER PRIMARY KEY, applied_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP)")
            conn.execute("INSERT OR IGNORE INTO schema_events(version) VALUES (1)")
            conn.execute("PRAGMA user_version=1")
        conn.commit()

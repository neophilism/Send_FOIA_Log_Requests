"""Offline SQLite schema migration. No external services."""
import sqlite3
from contextlib import closing
from pathlib import Path

SCHEMA_VERSION = 1


def initialize(path):
    location = Path(path)
    if str(location) != ":memory:":
        location.parent.mkdir(parents=True, exist_ok=True)
    with closing(sqlite3.connect(str(location))) as conn:
        # Serialize the version check and migration so two starters cannot race.
        conn.execute("BEGIN IMMEDIATE")
        try:
            version = conn.execute("PRAGMA user_version").fetchone()[0]
            if version > SCHEMA_VERSION:
                raise RuntimeError("unsupported future schema")
            if version == 0:
                conn.execute("CREATE TABLE schema_events (version INTEGER PRIMARY KEY, applied_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP)")
                conn.execute("INSERT INTO schema_events(version) VALUES (1)")
                conn.execute("PRAGMA user_version=1")
            elif conn.execute("SELECT COUNT(*) FROM schema_events WHERE version=1").fetchone()[0] != 1:
                raise RuntimeError("schema version event missing")
            conn.commit()
        except Exception:
            conn.rollback()
            raise

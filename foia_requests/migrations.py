"""Offline SQLite schema migration. No external services."""
import sqlite3
import os
import stat
from contextlib import closing
from pathlib import Path

SCHEMA_VERSION = 1


def _private_database_path(path):
    location = Path(os.path.abspath(path))
    # mkdir's mode affects only the final directory with parents=True. Build
    # missing parents individually so none are accidentally world-readable.
    missing = []
    parent = location.parent
    while not parent.exists():
        missing.append(parent)
        parent = parent.parent
    if parent.resolve() != parent:
        raise RuntimeError("database directory symlinks are not supported")
    for folder in reversed(missing):
        try:
            folder.mkdir(mode=0o700)
        except FileExistsError:
            pass  # Reconcile the directory another starter just created below.
    directory = location.parent.lstat()
    if (not stat.S_ISDIR(directory.st_mode) or location.parent.resolve() != location.parent
            or stat.S_IMODE(directory.st_mode) & 0o077
            or (hasattr(os, "getuid") and directory.st_uid != os.getuid())):
        raise RuntimeError("private owned database directory required")
    descriptor = None
    try:
        descriptor = os.open(location, os.O_CREAT | os.O_EXCL | os.O_WRONLY
                             | getattr(os, "O_NOFOLLOW", 0), 0o600)
    except FileExistsError:
        pass
    finally:
        if descriptor is not None:
            os.close(descriptor)
    current = location.lstat()
    if (not stat.S_ISREG(current.st_mode) or current.st_nlink != 1
            or stat.S_IMODE(current.st_mode) & 0o077
            or (hasattr(os, "getuid") and current.st_uid != os.getuid())):
        raise RuntimeError("private regular database file required")
    return location


def initialize(path):
    location = Path(path)
    if str(location) != ":memory:":
        location = _private_database_path(location)
    with closing(sqlite3.connect(str(location))) as conn:
        # Serialize the version check and migration so two starters cannot race.
        conn.execute("BEGIN IMMEDIATE")
        try:
            version = conn.execute("PRAGMA user_version").fetchone()[0]
            if version not in (0, SCHEMA_VERSION):
                raise RuntimeError("unsupported future schema")
            if version == 0:
                conn.execute("CREATE TABLE schema_events (version INTEGER PRIMARY KEY, applied_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP)")
                conn.execute("INSERT INTO schema_events(version) VALUES (1)")
                conn.execute("PRAGMA user_version=1")
            elif conn.execute("SELECT COUNT(*) FROM schema_events WHERE version=1").fetchone()[0] != 1:
                raise RuntimeError("schema version event missing")
            signature = [(row[1], row[2], row[3], row[4], row[5])
                         for row in conn.execute("PRAGMA table_info(schema_events)")]
            if signature != [("version", "INTEGER", 0, None, 1),
                              ("applied_at", "TEXT", 1, "CURRENT_TIMESTAMP", 0)]:
                raise RuntimeError("incompatible migration schema")
            if conn.execute("SELECT COUNT(*) FROM schema_events").fetchone()[0] != SCHEMA_VERSION:
                raise RuntimeError("unexpected migration event history")
            conn.commit()
        except Exception:
            conn.rollback()
            raise

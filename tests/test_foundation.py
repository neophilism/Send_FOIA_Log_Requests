import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path
from foia_requests.config import Config, ConfigurationError
from foia_requests.__main__ import COMMANDS, main

class FoundationTests(unittest.TestCase):
    def test_defaults(self):
        self.assertFalse(Config().transport_enabled)
        self.assertEqual(Config().mode, "dry_run")

    def test_unsafe_configuration_rejected(self):
        for settings in ({"mode": "live"}, {"transport_enabled": True},
                         {"schema_version": 2}, {"max_dry_run_drafts": 4},
                         {"max_dry_run_drafts": True}):
            with self.subTest(settings=settings), self.assertRaises(ConfigurationError):
                Config(**settings)

    def test_file_validation(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "config.json"
            path.write_text('{"max_dry_run_drafts":2}')
            self.assertEqual(Config.from_file(path).max_dry_run_drafts, 2)
            for bad in ('{"unknown":true}', '{"mode":"live"}', '{'):
                path.write_text(bad)
                with self.assertRaises(ConfigurationError):
                    Config.from_file(path)

    def test_command_families(self):
        for command in COMMANDS:
            with self.subTest(command=command):
                with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                    self.assertEqual(main([command]), 2 if command == "dispatch" else 0)

if __name__ == "__main__":
    unittest.main()

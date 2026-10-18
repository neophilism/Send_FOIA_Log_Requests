import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class CliProcessTests(unittest.TestCase):
    def run_cli(self, *args):
        return subprocess.run(
            [sys.executable, "-m", "foia_requests", *args],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )

    def test_fixture_and_help(self):
        help_result = self.run_cli("--help")
        self.assertEqual(help_result.returncode, 0)
        self.assertIn("dispatch", help_result.stdout)

        draft = self.run_cli("--config", "fixtures/offline-config.json", "draft")
        self.assertEqual(draft.returncode, 0)
        self.assertEqual(json.loads(draft.stdout), {
            "command": "draft", "mode": "dry_run", "status": "not_implemented"
        })

    def test_invalid_config_fails_before_command_and_dispatch_denied(self):
        with tempfile.TemporaryDirectory() as directory:
            config = Path(directory) / "config.json"
            config.write_text('{"transport_enabled":true}', encoding="utf8")
            result = self.run_cli("--config", str(config), "draft")
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(result.stdout, "")
            self.assertIn("disabled", result.stderr.lower())

        dispatch = self.run_cli("dispatch")
        self.assertNotEqual(dispatch.returncode, 0)
        self.assertEqual(dispatch.stdout, "")
        self.assertIn("disabled", dispatch.stderr.lower())

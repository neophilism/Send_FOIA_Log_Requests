import tempfile
import unittest
from pathlib import Path
from foia_requests.config import Config, ConfigurationError

class StrictConfigTests(unittest.TestCase):
    def test_reject_duplicate_keys_even_if_second_value_is_safe(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'config.json'
            path.write_text('{"transport_enabled":true,"transport_enabled":false}')
            with self.assertRaises(ConfigurationError):
                Config.from_file(path)

    def test_reject_large_and_nonfinite_configs(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'config.json'
            for contents in ('{"x":"' + 'a'*17000 + '"}', '{"max_dry_run_drafts":NaN}',
                             '{"mode":"dry_run","mode":"live"}'):
                with self.subTest(contents=contents[:60]):
                    path.write_text(contents)
                    with self.assertRaises(ConfigurationError):
                        Config.from_file(path)

    def test_utf8_strict_and_valid_config(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'config.json'
            path.write_bytes(b'\xff')
            with self.assertRaises(ConfigurationError):
                Config.from_file(path)
            path.write_text('{"max_dry_run_drafts":2}')
            self.assertEqual(Config.from_file(path).max_dry_run_drafts, 2)

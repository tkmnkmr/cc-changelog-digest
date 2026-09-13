import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS_DIR = os.path.join(ROOT_DIR, "scripts")
FIXTURE_FEED = os.path.join(ROOT_DIR, "tests", "fixtures", "feed_sample.xml")

sys.path.insert(0, SCRIPTS_DIR)

import check_update  # noqa: E402


class TestHtmlToText(unittest.TestCase):
    def test_paragraphs_and_bullets(self):
        html_in = "<p>• Fixed a thing</p>\n<p>• Added <code>--force</code> flag</p>"
        text = check_update.html_to_text(html_in)
        self.assertIn("- Fixed a thing", text)
        self.assertIn("- Added `--force` flag", text)

    def test_li_tags(self):
        html_in = "<ul><li>Added foo</li><li>Removed bar</li></ul>"
        text = check_update.html_to_text(html_in)
        self.assertIn("- Added foo", text)
        self.assertIn("- Removed bar", text)

    def test_entities_decoded(self):
        html_in = "<p>Fixed &amp; improved things &lt;here&gt;</p>"
        text = check_update.html_to_text(html_in)
        self.assertIn("Fixed & improved things <here>", text)


class TestExtractVersion(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(check_update.extract_version("Claude Code v2.1.270"), "2.1.270")

    def test_none_when_missing(self):
        self.assertIsNone(check_update.extract_version("No version here"))


class CheckUpdateCliTestCase(unittest.TestCase):
    """Runs check_update.py as a subprocess against a temp state dir by
    monkeypatching module-level paths would require import-time control,
    so instead we invoke the script fresh in a temp CWD copy."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        # Copy just what's needed: scripts/ and tests/fixtures/
        shutil.copytree(SCRIPTS_DIR, os.path.join(self.tmpdir, "scripts"))
        os.makedirs(os.path.join(self.tmpdir, "state"), exist_ok=True)
        with open(os.path.join(self.tmpdir, "state", "last_seen.json"), "w") as f:
            json.dump({"seen_versions": [], "last_checked": None}, f)

    def tearDown(self):
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def _run_check(self, extra_args=None):
        cmd = [sys.executable, os.path.join(self.tmpdir, "scripts", "check_update.py"),
               "--feed-file", FIXTURE_FEED]
        if extra_args:
            cmd += extra_args
        return subprocess.run(cmd, cwd=self.tmpdir, capture_output=True, text=True)

    def test_first_run_only_latest(self):
        result = self._run_check()
        self.assertEqual(result.returncode, 0, result.stderr)
        lines = result.stdout.strip().split("\n")
        self.assertEqual(lines[0], "NEW_UPDATE")
        # Only one version should be reported as new on first run.
        self.assertEqual(len(lines), 2)

        pending_dir = os.path.join(self.tmpdir, "state", "pending")
        pending_files = os.listdir(pending_dir)
        self.assertEqual(len(pending_files), 1)

    def test_no_update_when_all_seen(self):
        # First run to populate seen_versions with the latest version.
        self._run_check()
        # Load and mark ALL fixture versions as seen to simulate steady state.
        import re
        with open(FIXTURE_FEED) as f:
            feed_text = f.read()
        versions = re.findall(r"Claude Code v(\d+\.\d+\.\d+)", feed_text)
        with open(os.path.join(self.tmpdir, "state", "last_seen.json"), "w") as f:
            json.dump({"seen_versions": versions, "last_checked": None}, f)

        result = self._run_check()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.strip(), "NO_UPDATE")

    def test_force_writes_pending_even_if_seen(self):
        import re
        with open(FIXTURE_FEED) as f:
            feed_text = f.read()
        versions = re.findall(r"Claude Code v(\d+\.\d+\.\d+)", feed_text)
        with open(os.path.join(self.tmpdir, "state", "last_seen.json"), "w") as f:
            json.dump({"seen_versions": versions, "last_checked": None}, f)

        target_version = versions[1]  # a non-latest, already-seen version
        result = self._run_check(["--force", target_version])
        self.assertEqual(result.returncode, 0, result.stderr)
        pending_path = os.path.join(self.tmpdir, "state", "pending", f"{target_version}.json")
        self.assertTrue(os.path.exists(pending_path))


if __name__ == "__main__":
    unittest.main()

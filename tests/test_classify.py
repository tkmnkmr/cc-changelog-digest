import os
import sys
import unittest

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS_DIR = os.path.join(ROOT_DIR, "scripts")
sys.path.insert(0, SCRIPTS_DIR)

import classify  # noqa: E402


class TestClassifyLine(unittest.TestCase):
    def test_breaking(self):
        result = classify.classify_line("- This is a breaking change requiring migration")
        self.assertEqual(result["category"], "breaking")

    def test_model(self):
        result = classify.classify_line("- Added support for Claude Opus 4.5 as default model")
        self.assertEqual(result["category"], "model")

    def test_removed(self):
        result = classify.classify_line("- Removed deprecated --legacy-mode flag")
        # "removed" keyword should win before generic "changed"
        self.assertEqual(result["category"], "removed")

    def test_added(self):
        result = classify.classify_line("- Added /output-style command")
        self.assertEqual(result["category"], "added")

    def test_fixed(self):
        result = classify.classify_line("- Fixed a crash when resuming a session")
        self.assertEqual(result["category"], "fixed")

    def test_other_fallback(self):
        result = classify.classify_line("- Something totally unrelated happened")
        self.assertEqual(result["category"], "other")
        self.assertEqual(result["confidence"], "low")

    def test_tag_extraction(self):
        result = classify.classify_line("[VSCode] Fixed extension crash on startup")
        self.assertIn("VSCode", result["tags"])
        self.assertEqual(result["category"], "fixed")


if __name__ == "__main__":
    unittest.main()

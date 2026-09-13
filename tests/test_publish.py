import os
import shutil
import sys
import tempfile
import unittest

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS_DIR = os.path.join(ROOT_DIR, "scripts")

sys.path.insert(0, SCRIPTS_DIR)

import publish  # noqa: E402


class TestCopyVersionDirSync(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.tmpdir, ignore_errors=True)

        self.out_dir = os.path.join(self.tmpdir, "out")
        self.site_dir = os.path.join(self.tmpdir, "site")
        os.makedirs(self.out_dir)
        os.makedirs(self.site_dir)

        self._orig_out_dir = publish.OUT_DIR
        self._orig_site_dir = publish.SITE_DIR
        publish.OUT_DIR = self.out_dir
        publish.SITE_DIR = self.site_dir

    def tearDown(self):
        publish.OUT_DIR = self._orig_out_dir
        publish.SITE_DIR = self._orig_site_dir

    def test_removes_stale_file_not_in_publish_files(self):
        version = "1.2.3"
        src_dir = os.path.join(self.out_dir, version)
        os.makedirs(src_dir)
        with open(os.path.join(src_dir, "report.html"), "w") as f:
            f.write("<html></html>")

        dst_dir = os.path.join(self.site_dir, version)
        os.makedirs(dst_dir)
        # Stale file left over from a previous publish (e.g. an old card.png
        # that render_png.py no longer produces, or a removed asset).
        stale_path = os.path.join(dst_dir, "old_asset.txt")
        with open(stale_path, "w") as f:
            f.write("stale")

        publish.copy_version_dir(version)

        self.assertFalse(os.path.exists(stale_path))
        self.assertTrue(os.path.exists(os.path.join(dst_dir, "report.html")))

    def test_keeps_files_still_in_publish_files(self):
        version = "1.2.4"
        src_dir = os.path.join(self.out_dir, version)
        os.makedirs(src_dir)
        with open(os.path.join(src_dir, "report.html"), "w") as f:
            f.write("<html></html>")
        with open(os.path.join(src_dir, "summary.md"), "w") as f:
            f.write("summary")

        dst_dir = os.path.join(self.site_dir, version)
        os.makedirs(dst_dir)

        copied = publish.copy_version_dir(version)

        self.assertIn("report.html", copied)
        self.assertIn("summary.md", copied)
        self.assertTrue(os.path.exists(os.path.join(dst_dir, "summary.md")))

    def test_does_not_remove_subdirectories(self):
        version = "1.2.5"
        src_dir = os.path.join(self.out_dir, version)
        os.makedirs(src_dir)
        with open(os.path.join(src_dir, "report.html"), "w") as f:
            f.write("<html></html>")

        dst_dir = os.path.join(self.site_dir, version)
        sub_dir = os.path.join(dst_dir, "some_subdir")
        os.makedirs(sub_dir)

        publish.copy_version_dir(version)

        self.assertTrue(os.path.isdir(sub_dir))


if __name__ == "__main__":
    unittest.main()

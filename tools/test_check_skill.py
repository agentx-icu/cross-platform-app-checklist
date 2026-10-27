"""Exercise documentation validation against isolated repository copies."""
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parent.parent


class DocumentationValidationTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="skill-doc-check-")
        self.addCleanup(self.temp.cleanup)
        self.repo = Path(self.temp.name) / ROOT.name
        shutil.copytree(
            ROOT, self.repo, ignore=shutil.ignore_patterns(".git", "__pycache__")
        )

    def check(self):
        return subprocess.run(
            [sys.executable, str(self.repo / "tools" / "check_skill.py")],
            text=True, capture_output=True, check=False,
        )

    def test_valid_translated_readme(self):
        (self.repo / "README.zh-CN.md").write_text(
            "# 项目说明\n\n[技能](SKILL.md)\n", encoding="utf-8"
        )
        result = self.check()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_translated_readme_broken_link_is_rejected(self):
        (self.repo / "README.zh-CN.md").write_text(
            "# 项目说明\n\n[指南](missing-store-guide.md)\n", encoding="utf-8"
        )
        result = self.check()
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("README.zh-CN.md: broken link missing-store-guide.md", result.stdout)

    def test_reference_broken_translated_anchor_is_rejected(self):
        (self.repo / "references" / "store-fixture.zh-CN.md").write_text(
            "# 商店指南\n\n[不存在的标题](#missing-anchor)\n", encoding="utf-8"
        )
        result = self.check()
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("broken anchor #missing-anchor", result.stdout)

    def test_missing_stable_id_is_rejected(self):
        # Works before and after moving the catalog out of the entrypoint.
        catalog = self.repo / "references" / "checklist.md"
        if not catalog.exists():
            catalog = self.repo / "SKILL.md"
        text = catalog.read_text().replace("- **L1 Size range.", "- **Z1 Size range.")
        catalog.write_text(text)
        result = self.check()
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn("stable ID set", result.stdout)

    def test_broken_release_doc_link_is_rejected(self):
        docs = self.repo / "docs"
        docs.mkdir(exist_ok=True)
        (docs / "fixture.md").write_text("[release](missing.md)\n")
        result = self.check()
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn("broken link missing.md", result.stdout)

    def test_metadata_license_conflict_is_rejected(self):
        path = self.repo / "SKILL.md"
        path.write_text(path.read_text().replace("license: MIT-0", "license: GPL-3.0"))
        result = self.check()
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn("license must be MIT-0", result.stdout)

    def test_version_drift_is_rejected(self):
        (self.repo / "VERSION").write_text("9.9.9\n")
        result = self.check()
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn("version", result.stdout)


if __name__ == "__main__":
    unittest.main()

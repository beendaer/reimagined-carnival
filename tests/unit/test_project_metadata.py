"""Unit tests for project metadata."""
import json
import unittest
from pathlib import Path


class TestProjectMetadata(unittest.TestCase):
    """Validate package.json metadata for the project."""

    def test_package_metadata(self):
        project_root = Path(__file__).resolve().parents[2]
        metadata_path = project_root / "package.json"
        self.assertTrue(metadata_path.exists())

        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        self.assertEqual(metadata.get("name"), "reimagined-carnival")
        self.assertEqual(metadata.get("version"), "1.0.0")
        self.assertEqual(
            metadata.get("description"),
            "Monolithic architecture implementing Testing as a Service (TAAS) with a coherent facts registry.",
        )
        self.assertIsNone(metadata.get("main"))
        self.assertEqual(metadata.get("repository", {}).get("type"), "git")
        self.assertEqual(
            metadata.get("repository", {}).get("url"),
            "https://github.com/beendaer/reimagined-carnival.git",
        )
        self.assertEqual(metadata.get("author"), "beendaer")
        self.assertEqual(metadata.get("license"), "MIT")
        self.assertIn("taas", metadata.get("keywords", []))


if __name__ == "__main__":
    unittest.main()

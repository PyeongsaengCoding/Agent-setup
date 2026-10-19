"""check_releases groups the external skill catalog into one pin per source repository."""
from pathlib import Path
import json
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import check_releases  # noqa: E402


def entry(url, ref=None, tag=None):
    item = {"sourceUrl": url, "skillPath": "skills/x/SKILL.md", "releaseTag": tag}
    if ref:
        item["ref"] = ref
    return item


class ExternalSkillPinTests(unittest.TestCase):
    def test_one_row_per_repository_with_shared_ref(self):
        catalog = {"skills": {
            "a": entry("https://github.com/o/one.git", "1" * 40, "v1"),
            "b": entry("https://github.com/o/one.git", "1" * 40, "v1"),
            "c": entry("https://github.com/o/two.git"),
        }}
        rows = {repo: (label, pinned) for label, repo, _, pinned in check_releases.external_skill_pins(catalog)}
        self.assertEqual(set(rows), {"o/one", "o/two"})
        self.assertEqual(rows["o/one"][1], "1" * 40)
        self.assertIn("2개", rows["o/one"][0])
        self.assertIsNone(rows["o/two"][1])

    def test_disagreeing_refs_are_reported_as_mixed(self):
        catalog = {"skills": {
            "a": entry("https://github.com/o/one.git", "1" * 40, "v1"),
            "b": entry("https://github.com/o/one.git", "2" * 40, "v2"),
        }}
        [(_, _, _, pinned)] = check_releases.external_skill_pins(catalog)
        self.assertEqual(pinned, "mixed")

    def test_catalog_pins_every_released_source_to_a_full_commit(self):
        catalog = json.loads((ROOT / "codex/inventories/external-skills.json").read_text())
        for name, item in catalog["skills"].items():
            if item.get("releaseTag"):
                self.assertRegex(item.get("ref", ""), r"^[0-9a-f]{40}$", name)
            else:
                self.assertNotIn("ref", item, name)
        self.assertNotIn("mixed", [row[3] for row in check_releases.external_skill_pins(catalog)])


if __name__ == "__main__":
    unittest.main()

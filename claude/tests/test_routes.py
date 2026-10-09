"""Routing table and generated agents stay consistent."""
import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("build_agents", ROOT / "scripts/build_agents.py")
build = importlib.util.module_from_spec(spec)
spec.loader.exec_module(build)


class RouteTests(unittest.TestCase):
    def setUp(self):
        self.routes = json.loads((ROOT / "routes/claude-code.json").read_text())

    def test_every_preset_has_twelve_categories_with_descriptions(self):
        for preset in self.routes["presets"].values():
            self.assertEqual(set(preset), set(self.routes["descriptions"]))
            self.assertEqual(len(preset), 12)

    def test_claude_entries_get_native_agents_and_gpt_entries_use_codex(self):
        for name in self.routes["presets"]:
            for category, chain in build.resolved(self.routes, name).items():
                for entry in chain:
                    if entry["model"].startswith("claude-"):
                        self.assertTrue(entry["executor"].startswith(f"route-{category}-"))
                    else:
                        self.assertEqual(entry["executor"], "codex:codex-rescue")

    def test_agent_files_match_routes(self):
        self.assertEqual(build.check(), [])

    def test_agent_carries_model_and_effort(self):
        text = build.agents(self.routes)["route-ultrabrain-fable.md"]
        self.assertIn("model: claude-fable-5-1", text)
        self.assertIn("effort: xhigh", text)


if __name__ == "__main__":
    unittest.main()

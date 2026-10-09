"""Claude routing keeps the Hermes presets' order and reasoning."""
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class PortedRoutingTests(unittest.TestCase):
    def test_claude_presets_match_hermes_presets(self):
        claude = json.loads((ROOT / "claude/routes/claude-code.json").read_text())["presets"]
        for name in ("claude-generous", "gpt-generous"):
            hermes = json.loads((ROOT / f"hermes/routing-presets/{name}.json").read_text())
            expected = {
                item["category"]: [{"model": e["model"], "effort": e["reasoning_effort"]} for e in item["chain"]]
                for item in hermes["categories"]
            }
            self.assertEqual(claude[name], expected, name)

    def test_aside_rule_is_present_for_codex_and_claude(self):
        for path in ("codex/instructions/AGENTS.md", "claude/templates/global-rules.md"):
            text = (ROOT / path).read_text()
            self.assertIn("aside repl", text, path)
            self.assertIn("aside exec", text, path)

    def test_hermes_copies_match_shared_skills(self):
        manifest = json.loads((ROOT / "hermes/manifest.json").read_text())
        local = [s["name"] for s in manifest["skills"] if s["source_kind"] == "local"]
        self.assertEqual(sorted(local), sorted(p.name for p in (ROOT / "hermes/skills").iterdir() if p.is_dir()))
        for name in local:
            shared = ROOT / "shared/skills/core" / name
            if not shared.is_dir():
                shared = ROOT / "shared/skills/packs/mac" / name
            hermes = ROOT / "hermes/skills" / name
            files = sorted(p.relative_to(shared) for p in shared.rglob("*") if p.is_file())
            self.assertEqual(files, sorted(p.relative_to(hermes) for p in hermes.rglob("*") if p.is_file()), name)
            for rel in files:
                self.assertEqual((hermes / rel).read_bytes(), (shared / rel).read_bytes(), f"{name}/{rel}")

    def test_shared_core_has_no_personal_or_executor_paths(self):
        for path in (ROOT / "shared/skills").rglob("*.md"):
            text = path.read_text()
            for bad in ("/Users/", "~/.hermes", "omh runtime", "Codex-Setup/03-skills"):
                self.assertNotIn(bad, text, f"{path}: {bad}")


if __name__ == "__main__":
    unittest.main()

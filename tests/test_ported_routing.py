"""Executor-scoped routing and shared-tool contracts."""
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class PortedRoutingTests(unittest.TestCase):
    def test_external_claude_presets_preserve_their_approved_policy(self):
        claude = json.loads((ROOT / "claude/routes/claude-code.json").read_text())["presets"]
        gpt = json.loads((ROOT / "hermes/routing-presets/gpt-generous.json").read_text())
        base = {
            item["category"]: [{"model": e["model"], "effort": e["reasoning_effort"]} for e in item["chain"]]
            for item in gpt["categories"]
        }
        self.assertEqual(claude["gpt-generous"], base)
        expected = dict(base)
        historical = {
            "visual-engineering": ("claude-fable-5-1 claude-opus-5-5 gpt-6-astra", "high"),
            "artistry": ("claude-fable-5-1 claude-opus-5-5 gpt-6-astra", "high"),
            "capable": ("claude-fable-5-1 claude-opus-5-5 claude-sonnet-5-5 gpt-6-astra", "medium"),
            "deep-work": ("claude-fable-5-1 claude-opus-5-5 gpt-6-astra", "high"),
            "writing": ("claude-opus-5-5 gpt-6.1-sol", "medium"),
        }
        for category, (models, effort) in historical.items():
            expected[category] = [{"model": m, "effort": effort} for m in models.split()]
        self.assertEqual(claude["claude-generous"], expected)

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

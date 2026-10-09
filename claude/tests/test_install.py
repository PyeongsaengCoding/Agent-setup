"""Install behavior for the global Claude Code setup (disposable homes only)."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import subprocess

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("install", ROOT / "scripts/install.py")
install = importlib.util.module_from_spec(spec)
spec.loader.exec_module(install)


class InstallTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.home = Path(self.tmp.name) / ".claude"

    def tearDown(self):
        self.tmp.cleanup()

    def run_install(self, apply=True, preset="claude-generous"):
        return install.install(self.home, preset, apply)

    def test_preview_does_not_write(self):
        result = self.run_install(apply=False)
        self.assertEqual(result["status"], "changes")
        self.assertFalse(self.home.exists())

    def test_first_install_then_repeat_is_unchanged(self):
        result = self.run_install()
        self.assertEqual(result["status"], "applied")
        self.assertTrue((self.home / "agents/route-capable-fable.md").is_file())
        self.assertTrue((self.home / "skills/coding-work/SKILL.md").is_file())
        self.assertTrue((self.home / "skills/aside-browser/SKILL.md").is_file())
        self.assertTrue((self.home / "skills/codex/SKILL.md").is_file())
        self.assertFalse((self.home / "skills/read-model-performance-safety").exists())
        routing = json.loads((self.home / "agent-setup/routing.json").read_text())
        self.assertEqual(routing["preset"], "claude-generous")
        first = routing["categories"]["ultrabrain"]["chain"][0]
        self.assertEqual(first, {"model": "gpt-6-astra", "effort": "xhigh", "executor": "codex:codex-rescue"})
        agents_md = (self.home / "AGENTS.md").read_text()
        self.assertEqual(agents_md.count(install.RULES_START), 1)
        self.assertIn("aside repl", agents_md)
        self.assertIn("## 작업 원칙", agents_md)
        claude_md = (self.home / "CLAUDE.md").read_text()
        self.assertEqual(claude_md, install.pointer_block() + "\n")
        self.assertEqual(self.run_install()["status"], "unchanged")

    def test_existing_claude_md_text_is_kept(self):
        self.home.mkdir(parents=True)
        (self.home / "CLAUDE.md").write_text("my personal notes\n")
        self.run_install()
        text = (self.home / "CLAUDE.md").read_text()
        self.assertTrue(text.startswith("my personal notes\n"))
        self.assertIn(install.BLOCK_START, text)

    def test_user_edited_file_stops_without_writes(self):
        self.run_install()
        agent = self.home / "agents/route-deep-fable.md"
        agent.write_text("edited by user\n")
        before = (self.home / "agent-setup/routing.json").read_text()
        with self.assertRaises(install.Conflict):
            install.install(self.home, "gpt-generous", True)
        self.assertEqual(agent.read_text(), "edited by user\n")
        self.assertEqual((self.home / "agent-setup/routing.json").read_text(), before)

    def test_unmanaged_existing_file_is_conflict(self):
        target = self.home / "skills/coding-plan/SKILL.md"
        target.parent.mkdir(parents=True)
        target.write_text("someone else's skill\n")
        with self.assertRaises(install.Conflict):
            self.run_install()
        self.assertEqual(target.read_text(), "someone else's skill\n")

    def test_preset_switch_updates_unmodified_files(self):
        self.run_install()
        result = install.install(self.home, "gpt-generous", True)
        self.assertEqual(result["status"], "applied")
        routing = json.loads((self.home / "agent-setup/routing.json").read_text())
        self.assertEqual(routing["preset"], "gpt-generous")
        self.assertEqual(routing["categories"]["writing"]["chain"][0]["model"], "gpt-6.1-sol")
        self.assertTrue(list((self.home / "agent-setup/backups").iterdir()))

    def test_legacy_rules_block_in_claude_md_becomes_pointer(self):
        self.home.mkdir(parents=True)
        legacy = install.BLOCK_START + "\nold rules\n" + install.BLOCK_END
        (self.home / "CLAUDE.md").write_text("my notes\n\n" + legacy + "\n")
        state = self.home / install.STATE
        state.parent.mkdir(parents=True)
        state.write_text(json.dumps({"CLAUDE.md": install.digest(legacy.encode())}))
        self.assertEqual(self.run_install()["status"], "applied")
        text = (self.home / "CLAUDE.md").read_text()
        self.assertEqual(text, "my notes\n\n" + install.pointer_block() + "\n")
        self.assertIn(install.RULES_START, (self.home / "AGENTS.md").read_text())
        self.assertEqual(self.run_install()["status"], "unchanged")

    def test_pointer_can_be_skipped_and_removed(self):
        install.install(self.home, "claude-generous", True, claude_md_pointer=False)
        self.assertFalse((self.home / "CLAUDE.md").exists())
        self.run_install()
        (self.home / "CLAUDE.md").write_text("top\n\n" + (self.home / "CLAUDE.md").read_text())
        state = json.loads((self.home / install.STATE).read_text())
        self.assertIn("CLAUDE.md", state)
        install.install(self.home, "claude-generous", True, claude_md_pointer=False)
        self.assertEqual((self.home / "CLAUDE.md").read_text(), "top\n")
        self.assertEqual(install.install(self.home, "claude-generous", False, claude_md_pointer=False)["status"], "unchanged")

    def test_existing_agents_md_text_is_kept(self):
        self.home.mkdir(parents=True)
        (self.home / "AGENTS.md").write_text("my own rules\n")
        self.run_install()
        text = (self.home / "AGENTS.md").read_text()
        self.assertTrue(text.startswith("my own rules\n"))
        self.assertIn(install.RULES_START, text)

    def test_edited_managed_block_is_conflict(self):
        self.run_install()
        path = self.home / "AGENTS.md"
        path.write_text(path.read_text().replace("aside repl", "aside exec"))
        with self.assertRaises(install.Conflict):
            install.install(self.home, "gpt-generous", True)

    def test_symlink_target_is_refused(self):
        self.home.mkdir(parents=True)
        outside = Path(self.tmp.name) / "outside.md"
        outside.write_text("keep\n")
        (self.home / "CLAUDE.md").symlink_to(outside)
        with self.assertRaises(install.Conflict):
            self.run_install()
        self.assertEqual(outside.read_text(), "keep\n")

    def test_manifest_cannot_remove_file_outside_home(self):
        self.run_install()
        outside = Path(self.tmp.name) / "outside.md"
        outside.write_text("keep\n")
        state_path = self.home / install.STATE
        state = json.loads(state_path.read_text())
        state["../outside.md"] = install.digest(outside.read_bytes())
        state_path.write_text(json.dumps(state))
        with self.assertRaises(install.Conflict):
            self.run_install()
        self.assertEqual(outside.read_text(), "keep\n")

    def test_symlink_in_backup_path_stops_before_writes(self):
        self.run_install()
        outside = Path(self.tmp.name) / "outside"
        outside.mkdir()
        (self.home / "agent-setup/backups").symlink_to(outside)
        before = (self.home / "agent-setup/routing.json").read_bytes()
        with self.assertRaises(install.Conflict):
            self.run_install(preset="gpt-generous")
        self.assertEqual((self.home / "agent-setup/routing.json").read_bytes(), before)
        self.assertEqual(list(outside.iterdir()), [])

    def test_symlink_temporary_file_stops_before_writes(self):
        self.run_install()
        outside = Path(self.tmp.name) / "outside.md"
        outside.write_text("keep\n")
        (self.home / "agent-setup/.routing.json.agent-setup-tmp").symlink_to(outside)
        with self.assertRaises(install.Conflict):
            self.run_install(preset="gpt-generous")
        self.assertEqual(outside.read_text(), "keep\n")

    def test_loading_requires_exact_successful_answer_and_selected_home(self):
        with patch.object(install.shutil, "which", return_value="claude"), patch("subprocess.run") as run:
            run.return_value = subprocess.CompletedProcess([], 0, "작업 원칙\n", "")
            self.assertEqual(install.verify_loading(home=self.home)["status"], "loaded")
            self.assertEqual(run.call_args.kwargs["env"]["CLAUDE_CONFIG_DIR"], str(self.home))
            for code, answer in [(1, "작업 원칙"), (0, "작업 원칙이 보이지 않습니다")]:
                run.return_value = subprocess.CompletedProcess([], code, answer, "")
                self.assertEqual(install.verify_loading(home=self.home)["status"], "not_loaded")


if __name__ == "__main__":
    unittest.main()

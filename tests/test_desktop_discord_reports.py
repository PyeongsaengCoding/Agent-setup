"""desktop-discord-reports posts Desktop chats under every Hermes source label and skips other surfaces."""
import importlib.util
import sys
import tempfile
import types
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "hermes" / "discord" / "plugins" / "desktop-discord-reports" / "__init__.py"


class _FakeDB:
    row = None

    def _read_one(self, _sql, _params):
        return self.row


def _load(home: Path):
    state = types.ModuleType("hermes_state")
    state.SessionDB = _FakeDB
    cfg = types.ModuleType("hermes_cli.config")
    cfg.get_hermes_home = lambda: str(home)
    cfg.load_config = lambda: {"discord": {"channel_prompts": {"111": "project (folder: /p/app)"}}}
    cli = types.ModuleType("hermes_cli")
    cli.config = cfg
    mods = {"hermes_state": state, "hermes_cli": cli, "hermes_cli.config": cfg}
    spec = importlib.util.spec_from_file_location("desktop_discord_reports", PLUGIN)
    module = importlib.util.module_from_spec(spec)
    with mock.patch.dict(sys.modules, mods):
        spec.loader.exec_module(module)
    return module, mods


class DesktopDiscordReportsTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.home = Path(self.tmp.name)
        (self.home / ".env").write_text("DISCORD_BOT_TOKEN=x\nDISCORD_ALLOWED_USERS=9\n")
        self.plugin, self.mods = _load(self.home)

    def tearDown(self):
        self.tmp.cleanup()

    def _posts(self, source, created_source):
        _FakeDB.row = {"source": source, "created_source": created_source, "cwd": "/p/app",
                       "title": "t", "hidden": 0}
        calls = []

        def api(method, path, body=None):
            calls.append((method, path))
            return (201, {"id": "222"}) if path.endswith("/threads") else (200, {})

        with mock.patch.dict(sys.modules, self.mods), mock.patch.object(self.plugin, "_api", api):
            self.plugin._report("-".join(map(str, (source, created_source))), "done", 3)
        return calls

    def test_desktop_chats_are_reported_for_old_and_new_labels(self):
        for labels in (("desktop", None), ("local", "desktop"), ("gui", "desktop")):
            with self.subTest(labels=labels):
                calls = self._posts(*labels)
                self.assertIn(("POST", "/channels/111/threads"), calls)

    def test_non_desktop_surfaces_are_skipped(self):
        for labels in (("cron", None), ("local", "kanban"), ("subagent", "subagent"), ("discord", "discord")):
            with self.subTest(labels=labels):
                self.assertEqual(self._posts(*labels), [])

    def test_every_turn_is_reported(self):
        self.assertEqual(self.plugin.MIN_SECONDS, 0)


if __name__ == "__main__":
    unittest.main()

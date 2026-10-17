"""Retention sweep keeps the newest entries and only deletes expired ones."""
import importlib.util
import json
import os
import re
import tempfile
import time
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("retention", ROOT / "scripts" / "retention.py")
assert spec and spec.loader
retention = importlib.util.module_from_spec(spec)
spec.loader.exec_module(retention)

DAY = 86400


def touch(path, age_days, now, parents=0):
    """Create a file aged `age_days`; also age its `parents` enclosing folders."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("x")
    stamp = now - age_days * DAY
    for target in [path, *list(path.parents)[:parents]]:
        os.utime(target, (stamp, stamp))


class RetentionTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.home = Path(self.tmp.name)
        self.now = time.time()
        self.env = {k: os.environ.pop(k, None) for k in ("CODEX_HOME", "HERMES_HOME", "CLAUDE_CONFIG_DIR")}

    def tearDown(self):
        for key, value in self.env.items():
            if value is not None:
                os.environ[key] = value
        self.tmp.cleanup()

    def policy(self, item):
        return {"items": [item], "builtin": [], "gam": {"temporary_expiry_archive": False}}

    def test_keeps_newest_three_even_when_expired(self):
        root = self.home / ".codex/sessions/2026/01"
        for i in range(5):
            touch(root / f"rollout-{i}.jsonl", 100 + i, self.now)
        item = {"id": "s", "root": "{codex_home}/sessions", "select": "files", "glob": "**/rollout-*.jsonl",
                "days": 90, "keep_latest": 3}
        report = retention.sweep(self.home, apply=True, policy=self.policy(item), now=self.now, gam=False)
        self.assertEqual(report["items"]["s"]["removed"], 2)
        left = sorted(p.name for p in root.iterdir())
        self.assertEqual(left, ["rollout-0.jsonl", "rollout-1.jsonl", "rollout-2.jsonl"])

    def test_recent_entries_survive(self):
        root = self.home / ".hermes/backups"
        for i in range(6):
            touch(root / f"b{i}/data", 1, self.now)
        item = {"id": "b", "root": "{hermes_home}/backups", "select": "entries", "glob": "*", "days": 30, "keep_latest": 3}
        report = retention.sweep(self.home, apply=True, policy=self.policy(item), now=self.now, gam=False)
        self.assertEqual(report["items"]["b"]["removed"], 0)
        self.assertEqual(len(list(root.iterdir())), 6)

    def test_folder_age_uses_newest_file(self):
        root = self.home / ".hermes/backups"
        for i in range(4):
            touch(root / f"old{i}/a", 60, self.now, parents=1)
        touch(root / "old0/new", 1, self.now)
        item = {"id": "b", "root": "{hermes_home}/backups", "select": "entries", "glob": "*", "days": 30, "keep_latest": 0}
        retention.sweep(self.home, apply=True, policy=self.policy(item), now=self.now, gam=False)
        self.assertEqual([p.name for p in root.iterdir()], ["old0"])

    def test_preview_deletes_nothing_and_symlinks_are_ignored(self):
        root = self.home / ".hermes/cache/exec"
        outside = self.home / "outside.txt"
        touch(outside, 100, self.now)
        for i in range(4):
            touch(root / f"f{i}", 100, self.now)
        (root / "link").symlink_to(outside)
        item = {"id": "e", "root": "{hermes_home}/cache/exec", "select": "files", "glob": "*", "days": 14, "keep_latest": 0}
        report = retention.sweep(self.home, apply=False, policy=self.policy(item), now=self.now, gam=False)
        self.assertEqual(report["items"]["e"]["expired"], 4)
        self.assertEqual(len(list(root.iterdir())), 5)
        retention.sweep(self.home, apply=True, policy=self.policy(item), now=self.now, gam=False)
        self.assertTrue(outside.exists())
        self.assertEqual([p.name for p in root.iterdir()], ["link"])

    def test_codegraph_indexes_from_local_roots(self):
        config = retention.state_dir(self.home) / "retention.json"
        config.parent.mkdir(parents=True)
        config.write_text(json.dumps({"codegraph_roots": [str(self.home / "code")]}))
        for i in range(4):
            touch(self.home / f"code/repo{i}/.codegraph/codegraph.db", 40 + i, self.now, parents=1)
        touch(self.home / "code/repo9/node_modules/x/.codegraph/codegraph.db", 400, self.now)
        item = {"id": "cg", "select": "codegraph", "days": 30, "keep_latest": 3}
        report = retention.sweep(self.home, apply=True, policy=self.policy(item), now=self.now, gam=False)
        self.assertEqual(report["items"]["cg"]["removed"], 1)
        self.assertFalse((self.home / "code/repo3/.codegraph").exists())
        self.assertTrue((self.home / "code/repo9/node_modules/x/.codegraph").exists())

    def test_shipped_policy_is_valid(self):
        policy = json.loads(retention.POLICY.read_text())
        for item in policy["items"]:
            self.assertIn(item["select"], ("files", "entries", "codegraph"))
            self.assertGreaterEqual(item["keep_latest"], 3)
            self.assertGreaterEqual(item["days"], 14)
        conversation = {i["id"]: i["days"] for i in policy["items"]}
        self.assertEqual(conversation["codex-sessions"], policy["conversation_days"])
        builtin = {b["id"]: b["value"] for b in policy["builtin"]}
        self.assertEqual(builtin["hermes-sessions"], policy["conversation_days"])
        self.assertEqual(builtin["claude-transcripts"], policy["conversation_days"])

    def test_desktop_chat_script_matches_policy(self):
        policy = json.loads(retention.POLICY.read_text())["hermes_desktop_chats"]
        source = (ROOT / policy["script"]).read_text()

        def const(name):
            return re.search(rf"^{name} = (.+?)(?:\s+#|$)", source, re.M).group(1).strip()

        self.assertEqual(int(const("CHAT_KEEP")), policy["keep_latest_per_project"])
        self.assertEqual(int(const("CHAT_MAX_DAYS")), policy["max_days"])
        self.assertEqual(eval(const("RECENT_GRACE")), policy["run_records_grace_hours"] * 3600)
        self.assertEqual(eval(const("AUTOMATED_SOURCES")), set(policy["run_record_sources"]))
        self.assertEqual(int(const("IDLE_DAYS")), policy["discord_thread_idle_days"])
        self.assertEqual(int(const("KEEP")), policy["discord_thread_keep_latest"])


if __name__ == "__main__":
    unittest.main()

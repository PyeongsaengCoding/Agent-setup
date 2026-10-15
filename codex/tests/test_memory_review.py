"""GAM review candidates: only stale, unprotected, active project notes are reported."""
import datetime
import json
import sys
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))
import maintain  # noqa: E402

POLICY = json.loads((SCRIPTS.parent / "config" / "retention.json").read_text())
NOW = datetime.datetime(2026, 10, 15, tzinfo=datetime.timezone.utc)


def note(days, **extra):
    return dict({"scope": "project", "status": "active", "updated_at": (NOW - datetime.timedelta(days=days)).isoformat()}, **extra)


class MemoryReviewTests(unittest.TestCase):
    def test_stale_note_is_reported(self):
        self.assertTrue(maintain.stale_memory(note(200), NOW, POLICY))

    def test_recent_protected_or_inactive_notes_are_not(self):
        self.assertFalse(maintain.stale_memory(note(10), NOW, POLICY))
        self.assertFalse(maintain.stale_memory(note(200, tags=["pinned"]), NOW, POLICY))
        self.assertFalse(maintain.stale_memory(note(200, status="archived"), NOW, POLICY))
        self.assertFalse(maintain.stale_memory(note(200, scope="global"), NOW, POLICY))


if __name__ == "__main__":
    unittest.main()

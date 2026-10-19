"""Local patch sets: report and apply on top of an official release checkout."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import apply_local_patches as alp  # noqa: E402


def git(repo, *args):
    subprocess.run(['git', '-C', str(repo), *args], check=True, capture_output=True)


class LocalPatchTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        base = Path(self.temp.name)
        self.repo = base / 'checkout'
        self.repo.mkdir()
        git(self.repo, 'init', '-q')
        git(self.repo, 'config', 'user.email', 't@example.invalid')
        git(self.repo, 'config', 'user.name', 't')
        (self.repo / 'a.txt').write_text('one\n')
        git(self.repo, 'add', 'a.txt')
        git(self.repo, 'commit', '-qm', 'base')
        git(self.repo, 'tag', 'v1.0.0')
        self.patches = base / 'patches'
        (self.patches / 'demo').mkdir(parents=True)
        (self.repo / 'a.txt').write_text('one\ntwo\n')
        diff = subprocess.run(['git', '-C', str(self.repo), 'diff'], capture_output=True, text=True).stdout
        (self.patches / 'demo' / 'v1.0.0.patch').write_text(diff)
        git(self.repo, 'checkout', '-q', 'a.txt')
        self.old = alp.PATCHES
        alp.PATCHES = self.patches

    def tearDown(self):
        alp.PATCHES = self.old
        self.temp.cleanup()

    def test_applicable_then_applied(self):
        self.assertEqual(alp.status('demo', self.repo)['status'], 'applicable')
        git(self.repo, 'apply', str(self.patches / 'demo' / 'v1.0.0.patch'))
        self.assertEqual(alp.status('demo', self.repo)['status'], 'applied')

    def test_conflict_and_missing_patch(self):
        (self.repo / 'a.txt').write_text('changed upstream\n')
        self.assertEqual(alp.status('demo', self.repo)['status'], 'conflict')
        git(self.repo, 'checkout', '-q', 'a.txt')
        git(self.repo, 'tag', '-d', 'v1.0.0')
        git(self.repo, 'tag', 'v2.0.0')
        row = alp.status('demo', self.repo)
        self.assertEqual(row['status'], 'no_patch')
        self.assertEqual(row['available'], ['v1.0.0'])


if __name__ == '__main__':
    unittest.main()

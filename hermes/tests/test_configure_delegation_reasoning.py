import ast
import json
from pathlib import Path
import tempfile
from types import ModuleType, SimpleNamespace
import unittest
from unittest.mock import patch

from scripts.configure_delegation_reasoning import adapt, install


SOURCE = '''def _reresolve_fallback_reasoning_config(agent) -> None:
    """Fallback reasoning."""
    try:
        from hermes_cli.config import load_config
        from hermes_constants import resolve_reasoning_config
        agent.reasoning_config = resolve_reasoning_config(load_config() or {}, agent.model)
    except Exception:
        pass
'''


class DelegationReasoningTests(unittest.TestCase):
    def test_child_preserves_each_category_effort(self):
        namespace = {}
        exec(compile(adapt(SOURCE), '<fixture>', 'exec'), namespace)
        for effort in ('low', 'medium', 'high', 'xhigh', 'max'):
            agent = SimpleNamespace(_delegate_depth=1, reasoning_config={'effort': effort}, model='fallback')
            namespace['_reresolve_fallback_reasoning_config'](agent)
            self.assertEqual(agent.reasoning_config, {'effort': effort})

    def test_patch_is_idempotent_and_valid_python(self):
        patched = adapt(SOURCE)
        self.assertEqual(adapt(patched), patched)
        ast.parse(patched)

    def test_unknown_source_refused(self):
        with self.assertRaises(ValueError):
            adapt('def unrelated():\n    pass\n')

    def test_main_session_keeps_native_resolution(self):
        config = ModuleType('hermes_cli.config')
        setattr(config, 'load_config', lambda: {'effort': 'low'})
        constants = ModuleType('hermes_constants')
        setattr(constants, 'resolve_reasoning_config', lambda config, model: config)
        namespace = {}
        exec(compile(adapt(SOURCE), '<fixture>', 'exec'), namespace)
        agent = SimpleNamespace(_delegate_depth=0, reasoning_config={'effort': 'high'}, model='fallback')
        with patch.dict('sys.modules', {'hermes_cli': ModuleType('hermes_cli'),
                                       'hermes_cli.config': config, 'hermes_constants': constants}):
            namespace['_reresolve_fallback_reasoning_config'](agent)
        self.assertEqual(agent.reasoning_config, {'effort': 'low'})

    def test_snapshot_preserves_category_efforts_and_primary_models(self):
        from test_claude_generous_policy import EXPECTED
        snapshot = json.loads((Path(__file__).resolve().parents[1] / 'routing-snapshot.json').read_text())
        categories = {item['category']: item['chain'] for item in snapshot['categories']}
        self.assertEqual(set(categories), set(EXPECTED))
        for category, (models, effort) in EXPECTED.items():
            chain = categories[category]
            self.assertEqual([item['model'] for item in chain], models.split())
            self.assertTrue(all(item['reasoning_effort'] == effort for item in chain))
        self.assertEqual(snapshot['delegation_fallback_providers'][0]['model'], 'claude-opus-5-5')
        self.assertEqual(snapshot['fallback_providers'],
                         [{'provider': 'anthropic', 'model': 'claude-opus-5-5'}])

    def test_preview_apply_repeat_and_symlink_refusal(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            target = root / 'agent/chat_completion_helpers.py'
            target.parent.mkdir()
            target.write_text(SOURCE)
            self.assertEqual(install(root)['status'], 'preview')
            self.assertEqual(target.read_text(), SOURCE)
            self.assertEqual(install(root, apply=True)['status'], 'applied')
            self.assertEqual(install(root, apply=True)['status'], 'unchanged')
            target.unlink()
            original = root / 'original.py'
            original.write_text(SOURCE)
            target.symlink_to(original)
            with self.assertRaises(ValueError):
                install(root, apply=True)
            self.assertEqual(original.read_text(), SOURCE)


if __name__ == '__main__':
    unittest.main()

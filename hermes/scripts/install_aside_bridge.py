#!/usr/bin/env python3
"""Install the Aside bridge into a Hermes profile and register it as the `aside` MCP server.

Copies hermes/integrations/aside-browser/ to <HERMES_HOME>/integrations/aside-browser/, sets
mcp_servers.aside to its launcher (repl tool only) and turns off Hermes' built-in browser toolset.
Default is a read-only preview; pass --apply to install.
"""
import argparse, json, os, pathlib, shutil, subprocess

ROOT = pathlib.Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'integrations/aside-browser'
FILES = ('server.py', 'routing.py', 'launch.py', 'test_bridge.py')


def server_entry(target):
    return {'command': str(target / 'launch.py'), 'args': [], 'enabled': True, 'timeout': 180,
            'supports_parallel_tool_calls': True,
            'tools': {'include': ['repl'], 'resources': False, 'prompts': False}}


def install(home, apply=False):
    target = home / 'integrations/aside-browser'
    changes = [name for name in FILES
               if not (target / name).exists() or (target / name).read_bytes() != (SOURCE / name).read_bytes()]
    result = {'target': str(target), 'files_to_update': changes, 'apply': apply}
    if not apply:
        return result
    target.mkdir(parents=True, exist_ok=True)
    for name in changes:
        shutil.copy2(SOURCE / name, target / name)
    (target / 'launch.py').chmod(0o755)
    env = dict(os.environ, HERMES_HOME=str(home))
    subprocess.run(['hermes', 'config', 'set', 'mcp_servers.aside', json.dumps(server_entry(target))], check=True, env=env)
    disabled = json.loads(subprocess.run(['hermes', 'config', 'get', 'agent.disabled_toolsets', '--json'],
                                         capture_output=True, text=True, env=env).stdout or '[]') or []
    if 'browser' not in disabled:
        disabled.append('browser')
        subprocess.run(['hermes', 'config', 'set', 'agent.disabled_toolsets', json.dumps(disabled)], check=True, env=env)
    result['status'] = 'installed'
    result['next'] = 'Restart the Hermes session (or kill the old aside-browser/server.py) so the new bridge loads.'
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--home', help='Hermes profile home; otherwise HERMES_HOME or ~/.hermes')
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args()
    home = pathlib.Path(args.home or os.environ.get('HERMES_HOME') or pathlib.Path.home() / '.hermes').expanduser()
    print(json.dumps(install(home, args.apply), ensure_ascii=False))


if __name__ == '__main__':
    main()

"""Real-Aside checks: every profile resolves, and idle contexts close and reopen.

Run with Hermes' Python: `<hermes python> -I test_bridge.py` (needs the Aside app running).
"""
import sys, pathlib, asyncio, os, subprocess
HOME = pathlib.Path(os.environ.get('HERMES_HOME', pathlib.Path.home() / '.hermes'))
sys.path.insert(0, str(HOME / 'hermes-agent'))
import hermes_bootstrap  # noqa: F401
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from routing import list_profiles, resolve_profile
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

SERVER = pathlib.Path(__file__).with_name('server.py')


def aside_children(pid):
    return subprocess.run(['pgrep', '-P', str(pid), '-f', 'aside mcp'], capture_output=True, text=True).stdout.split()


async def main():
    profiles = sorted(list_profiles())
    resolved = {p: resolve_profile(p)['account'] for p in profiles}
    print('profiles resolved:', resolved)
    first = profiles[0]
    env = {k: v for k, v in os.environ.items() if k in ['HOME', 'PATH', 'TMPDIR', 'USER', 'LANG']}
    env['ASIDE_BRIDGE_IDLE_SECONDS'] = '5'
    params = StdioServerParameters(command=sys.executable, args=['-I', str(SERVER)], env=env)
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as s:
            await s.initialize()
            tools = await s.list_tools()
            assert [t.name for t in tools.tools] == ['repl']
            schema = getattr(tools.tools[0], 'input_schema', None) or getattr(tools.tools[0], 'inputSchema')
            enum = schema['properties']['profile'].get('enum')
            assert sorted(enum) == profiles, enum
            r = await s.call_tool('repl', {'profile': first, 'title': 'bridge check', 'code': 'console.log("BRIDGE_OK")', 'workstream': 'bridge-check'})
            assert 'BRIDGE_OK' in '\n'.join(x.text for x in r.content if x.type == 'text'), r.model_dump()
            srv = subprocess.run(['pgrep', '-f', str(SERVER)], capture_output=True, text=True).stdout.split()
            before = sum(len(aside_children(p)) for p in srv)
            assert before >= 1
            await asyncio.sleep(75)
            after = sum(len(aside_children(p)) for p in srv)
            assert after == 0, f'context still open after idle window: {after}'
            r = await s.call_tool('repl', {'profile': first, 'title': 'reopen', 'code': 'console.log("REOPEN_OK")', 'workstream': 'bridge-check'})
            assert 'REOPEN_OK' in '\n'.join(x.text for x in r.content if x.type == 'text')
            print(f'PASS: {len(profiles)} profiles in tool, contexts before={before} after_idle={after}, reopen ok')


asyncio.run(main())

"""One short Hermes MCP tool that runs Aside REPL code per browser profile and workstream.

Each profile+workstream keeps its own `aside mcp` child so variables and owned tabs persist.
Contexts idle for ASIDE_BRIDGE_IDLE_SECONDS (default 15 min) close on their own, and when all
MAX_CONTEXTS slots are taken the oldest idle context is closed to make room.
"""
import sys, pathlib, asyncio, os, time, shutil
from contextlib import asynccontextmanager
from typing import Literal

HERMES_HOME = pathlib.Path(os.environ.get('HERMES_HOME', pathlib.Path.home() / '.hermes'))
sys.path.insert(0, str(HERMES_HOME / 'hermes-agent'))
import hermes_bootstrap  # noqa: F401  (puts Hermes' bundled packages on sys.path)
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from routing import list_profiles, resolve_profile
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp.server import MCPServer
from mcp.types import TextContent

CLI = shutil.which('aside') or str(pathlib.Path.home() / '.local/bin/aside')
SAFE_ENV = {k: v for k, v in os.environ.items() if k in ['HOME', 'PATH', 'TMPDIR', 'USER', 'LANG', 'LC_ALL', 'SHELL']}
MAX_CONTEXTS = 16
IDLE_SECONDS = int(os.environ.get('ASIDE_BRIDGE_IDLE_SECONDS', '900'))
PROFILES = tuple(sorted(list_profiles())) or ('none',)
ProfileName = Literal[PROFILES]
workers = {}


def log(msg):
    print('[aside-bridge] ' + msg, file=sys.stderr, flush=True)


class Worker:
    def __init__(self, account):
        self.account = account
        self.queue = asyncio.Queue()
        self.ready = asyncio.get_running_loop().create_future()
        self.failure = None
        self.busy = 0
        self.last_used = time.monotonic()
        self.task = asyncio.create_task(self.run())

    async def run(self):
        active = None
        try:
            params = StdioServerParameters(command=CLI, args=['mcp', '--account', self.account, '--host', 'local'], env=SAFE_ENV)
            async with stdio_client(params) as (read, write):
                async with ClientSession(read, write) as client:
                    await client.initialize()
                    self.ready.set_result(True)
                    while True:
                        item = await self.queue.get()
                        if item is None:
                            break
                        args, active = item
                        result = await client.call_tool('repl', args)
                        if not active.done():
                            active.set_result(result)
                        active = None
        except Exception as exc:
            self.failure = exc
            if not self.ready.done():
                self.ready.set_exception(exc)
            if active is not None and not active.done():
                active.set_exception(exc)
            while not self.queue.empty():
                item = self.queue.get_nowait()
                if item is not None and not item[1].done():
                    item[1].set_exception(exc)
            log('worker failed: ' + str(exc))

    async def call(self, args):
        self.busy += 1
        self.last_used = time.monotonic()
        try:
            await self.ready
            if self.failure is not None:
                raise RuntimeError('Aside context failed; use a new workstream') from self.failure
            future = asyncio.get_running_loop().create_future()
            await self.queue.put((args, future))
            return await asyncio.wait_for(asyncio.shield(future), 150)
        finally:
            self.busy -= 1
            self.last_used = time.monotonic()

    def idle_for(self):
        return time.monotonic() - self.last_used

    async def close(self):
        await self.queue.put(None)
        try:
            await asyncio.wait_for(self.task, 10)
        except Exception:
            self.task.cancel()


async def close_worker(key, reason):
    worker = workers.pop(key, None)
    if worker is None:
        return
    log(f'closing context {key[1]}/{key[2]} ({reason}, idle {int(worker.idle_for())}s)')
    await worker.close()


async def reap_idle():
    while True:
        await asyncio.sleep(60)
        for key, w in list(workers.items()):
            if w.busy == 0 and (w.failure is not None or w.idle_for() >= IDLE_SECONDS):
                await close_worker(key, 'failed' if w.failure is not None else 'idle')


async def make_room():
    if len(workers) < MAX_CONTEXTS:
        return
    idle = [(w.last_used, k) for k, w in workers.items() if w.busy == 0]
    if not idle:
        raise ValueError(f'{MAX_CONTEXTS} live contexts reached and all are busy; retry shortly')
    await close_worker(min(idle)[1], 'evicted for new context')


@asynccontextmanager
async def lifespan(_server):
    reaper = asyncio.create_task(reap_idle())
    try:
        yield {}
    finally:
        reaper.cancel()
        for key in list(workers):
            await close_worker(key, 'shutdown')


mcp = MCPServer('Aside browser for Hermes', lifespan=lifespan)


@mcp.tool()
async def repl(profile: ProfileName, title: str, code: str, workstream: str = 'main'):
    """Default browser for Hermes. Read aside-browser skill; select the profile required by project instructions. Run Aside Playwright JavaScript without using its AI agent. Scope/variables persist per profile+workstream; use distinct workstreams for independent concurrent jobs. Idle contexts close after 15 min. Unknown or mismatched profile bindings fail closed. Use listBrowserTabs/attachBrowserTab, openTab, snapshot and locator actions; no implicit Chrome/Edge fallback."""
    if not workstream or len(workstream) > 80:
        raise ValueError('workstream must be 1–80 characters')
    route = resolve_profile(profile)
    key = (route['profile_id'], route['account'], workstream)
    if key in workers and workers[key].failure is not None:
        await close_worker(key, 'failed')
    if key not in workers:
        await make_room()
        workers[key] = Worker(route['account'])
    result = await workers[key].call({'title': title, 'code': code})
    if result.is_error:
        raise RuntimeError('\n'.join(x.text for x in result.content if x.type == 'text'))
    return [TextContent(type='text', text=f"Aside target: {route['name']} | account {route['account']} | workstream {workstream}"), *result.content]


if __name__ == '__main__':
    mcp.run(transport='stdio')

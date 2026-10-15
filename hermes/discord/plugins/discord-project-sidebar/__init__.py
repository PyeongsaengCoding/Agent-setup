"""Discord Project Sidebar: file each new Discord session under its Desktop project.

Discord gateway sessions start with no workspace, so the Desktop sidebar lists them under
Home. On session start this hook maps the thread's parent channel to the project folder
named in ``discord.channel_prompts`` ("(folder: /path)") and stores it as the session cwd.
The daily ``scripts/discord-project-hygiene.py`` run backfills anything this misses.
"""
from __future__ import annotations

import json
import logging
import re
import threading
import time

logger = logging.getLogger(__name__)


def _folders() -> dict[str, str]:
    from hermes_cli.config import load_config
    prompts = (load_config().get("discord") or {}).get("channel_prompts") or {}
    out = {}
    for cid, text in prompts.items():
        m = re.search(r"\(folder: (.+?)\)", str(text))
        if m:
            out[str(cid)] = m.group(1)
    return out


def _attach(session_id: str) -> None:
    from hermes_state import SessionDB
    db = SessionDB()
    for _ in range(20):  # the session row may be written just after the hook fires
        row = db._read_one("SELECT source, cwd, origin_json FROM sessions WHERE id = ?", (session_id,))
        if row is not None:
            if row["source"] != "discord" or (row["cwd"] or "").strip():
                return
            origin = json.loads(row["origin_json"] or "{}")
            folders = _folders()
            folder = folders.get(str(origin.get("parent_chat_id") or "")) or folders.get(
                str(origin.get("chat_id") or ""))
            if folder:
                db.update_session_cwd(session_id, folder)
                logger.info("discord-project-sidebar: %s -> %s", session_id, folder)
            return
        time.sleep(1.5)


def _on_session_start(session_id: str = "", platform: str = "", **_kw) -> None:
    if str(platform).lower() != "discord" or not session_id:
        return

    def run():
        try:
            _attach(session_id)
        except Exception:
            logger.warning("discord-project-sidebar failed for %s", session_id, exc_info=True)

    threading.Thread(target=run, name="discord-project-sidebar", daemon=True).start()


def register(ctx):
    ctx.register_hook("on_session_start", _on_session_start)

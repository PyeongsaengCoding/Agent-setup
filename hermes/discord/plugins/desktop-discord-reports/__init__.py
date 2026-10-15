"""Desktop -> Discord reports: post the result of every finished Desktop turn to the project's Discord channel.

When a Desktop chat turn runs for at least MIN_SECONDS (0 = every turn), its final reply is posted to a Discord
thread for that chat, under the project channel that matches the chat's folder (from
``discord.channel_prompts`` "(folder: ...)"); chats outside a project go to the home channel.
One thread per Desktop chat, created on first report and reused (recreated if deleted).
Plugins load once at backend start: after installing or editing this file, fully quit and reopen Desktop.
"""
from __future__ import annotations

import json
import logging
import os
import re
import threading
import time
import urllib.error
import urllib.request
from pathlib import Path

logger = logging.getLogger(__name__)

MIN_SECONDS = 0  # report every finished Desktop turn, like the Desktop app's own notification
API = "https://discord.com/api/v10"
_NOT_DESKTOP = {
    "cron", "kanban", "subagent", "oneshot", "acp", "api", "batch", "cli", "tui",
    "discord", "telegram", "slack", "whatsapp", "signal", "teams", "google_chat",
    "qqbot", "email", "sms", "matrix", "mattermost", "homeassistant", "webhook", "raft",
}
_starts: dict[str, float] = {}
_lock = threading.Lock()


def _home() -> Path:
    from hermes_cli.config import get_hermes_home
    return Path(get_hermes_home())


def _env(key: str) -> str:
    val = os.environ.get(key)
    if val:
        return val.strip()
    for line in (_home() / ".env").read_text().splitlines():
        if line.startswith(key + "="):
            return line.split("=", 1)[1].strip().strip("\"'")
    return ""


def _api(method: str, path: str, body=None):
    if isinstance(body, dict) and "content" in body:
        body = {**body, "allowed_mentions": {"parse": []}}  # never ping @everyone/roles from a report
    req = urllib.request.Request(API + path, method=method,
        data=json.dumps(body).encode() if body is not None else None,
        headers={"Authorization": "Bot " + _env("DISCORD_BOT_TOKEN"), "Content-Type": "application/json",
                 "User-Agent": "DiscordBot (hermes-desktop-reports, 1)"})
    for _ in range(4):
        try:
            with urllib.request.urlopen(req, timeout=20) as r:
                raw = r.read()
                return r.status, (json.loads(raw) if raw else None)
        except urllib.error.HTTPError as e:
            if e.code == 429:
                time.sleep(float(json.loads(e.read() or b"{}").get("retry_after", 1)) + 0.2)
                continue
            return e.code, None
    return 429, None


def _channel_for(cwd: str | None) -> str:
    from hermes_cli.config import load_config
    cfg = load_config()
    best, best_len = "", -1
    for cid, text in ((cfg.get("discord") or {}).get("channel_prompts") or {}).items():
        m = re.search(r"\(folder: (.+?)\)", str(text))
        if not (m and cwd):
            continue
        folder = m.group(1).rstrip("/")
        if (cwd == folder or cwd.startswith(folder + "/")) and len(folder) > best_len:
            best, best_len = str(cid), len(folder)
    return best or _env("DISCORD_HOME_CHANNEL")


def _chunks(text: str, size: int = 1900) -> list[str]:
    out = []
    while text:
        cut = text.rfind("\n", 0, size) if len(text) > size else len(text)
        cut = cut if cut > 0 else size
        out.append(text[:cut])
        text = text[cut:].lstrip("\n")
    return out


def _report(session_id: str, response: str, seconds: float) -> None:
    from hermes_state import SessionDB
    row = SessionDB()._read_one(
        "SELECT source, created_source, cwd, title, COALESCE(hidden, 0) AS hidden FROM sessions WHERE id = ?",
        (session_id,))
    # Surface labels change across Hermes updates (v0.22 moved Desktop chats from source='desktop'
    # to source='local'/created_source='desktop'). Exclude known non-Desktop surfaces instead of
    # allow-listing one label, so a future rename still reports rather than silently dropping.
    labels = {str(v or "").lower() for v in (row["source"], row["created_source"])} if row else set()
    if row is None or row["hidden"] or labels & _NOT_DESKTOP:
        return
    channel = _channel_for(row["cwd"])
    if not channel:
        return
    title = (row["title"] or session_id)[:90]
    map_path = _home() / "state" / "desktop-discord-threads.json"
    map_path.parent.mkdir(parents=True, exist_ok=True)
    with _lock:
        mapping = json.loads(map_path.read_text()) if map_path.exists() else {}
        thread = mapping.get(session_id)
        body = f"✅ **{title}** — 작업 완료 ({int(seconds // 60)}분 {int(seconds % 60)}초)\n\n{response.strip()}"
        body += f"\n\n-# Desktop 채팅 `{session_id}`"
        parts = _chunks(body)
        if len(parts) > 4:
            parts = parts[:4]
            parts[-1] += "\n\n…(이후 내용은 Desktop 채팅에서 확인)"
        status = 0
        if thread:
            status, _ = _api("POST", f"/channels/{thread}/messages", {"content": parts[0]})
        if not thread or status == 404:
            s, t = _api("POST", f"/channels/{channel}/threads",
                        {"name": title, "type": 11, "auto_archive_duration": 10080})
            if s >= 300 or not t:
                logger.warning("desktop-discord-reports: thread create failed (%s)", s)
                return
            thread = mapping[session_id] = t["id"]
            map_path.write_text(json.dumps(mapping, ensure_ascii=False, indent=1))
            owner = _env("DISCORD_ALLOWED_USERS").split(",")[0].strip()
            if owner:
                _api("PUT", f"/channels/{thread}/thread-members/{owner}")
            _api("POST", f"/channels/{thread}/messages", {"content": parts[0]})
        for part in parts[1:]:
            _api("POST", f"/channels/{thread}/messages", {"content": part})


def _pre(session_id: str = "", **_kw):
    if session_id:
        _starts[session_id] = time.monotonic()
    return None


def _post(session_id: str = "", assistant_response: str = "", **_kw) -> None:
    started = _starts.pop(session_id, None)
    if started is None or not assistant_response:
        return
    seconds = time.monotonic() - started
    if seconds < MIN_SECONDS:
        return

    def run():
        try:
            _report(session_id, assistant_response, seconds)
        except Exception:
            logger.warning("desktop-discord-reports failed for %s", session_id, exc_info=True)

    threading.Thread(target=run, name="desktop-discord-reports", daemon=True).start()


def register(ctx):
    ctx.register_hook("pre_llm_call", _pre)
    ctx.register_hook("post_llm_call", _post)

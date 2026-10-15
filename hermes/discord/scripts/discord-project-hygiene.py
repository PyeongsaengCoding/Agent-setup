"""Daily hygiene for Discord project channels and the Hermes Desktop sidebar.

1. Attach Discord sessions with no workspace to their project folder (so the sidebar
   groups them under the project instead of Home).
2. Discord: in each project channel, delete threads idle > IDLE_DAYS, keeping the newest
   KEEP threads. Threads used as cron delivery targets are never deleted.
3. Hermes: per sidebar group (each project + Home), permanently delete chats idle > IDLE_DAYS,
   keeping the newest KEEP. Pinned chats and cron-alarm thread sessions are skipped.

Usage: python3 discord-project-hygiene.py [--dry-run]
Prints nothing when there is nothing to do (silent cron run).
"""
from __future__ import annotations

import json
import os
import re
import sqlite3
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

HOME = Path(os.environ.get("HERMES_HOME") or Path.home() / ".hermes")
sys.path.insert(0, str(HOME / "hermes-agent"))

IDLE_DAYS = 3
KEEP = 3
DRY = "--dry-run" in sys.argv
DISCORD_EPOCH_MS = 1420070400000
API = "https://discord.com/api/v10"


def env_value(key: str) -> str:
    for line in (HOME / ".env").read_text().splitlines():
        if line.startswith(key + "="):
            return line.split("=", 1)[1].strip().strip("\"'")
    raise SystemExit(f"{key} missing in .env")


TOKEN = env_value("DISCORD_BOT_TOKEN")


def api(method: str, path: str):
    req = urllib.request.Request(API + path, method=method, headers={
        "Authorization": "Bot " + TOKEN, "User-Agent": "DiscordBot (hermes-hygiene, 1)"})
    for _ in range(5):
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                body = r.read()
                return r.status, (json.loads(body) if body else None)
        except urllib.error.HTTPError as e:
            if e.code == 429:
                time.sleep(float(json.loads(e.read() or b"{}").get("retry_after", 1)) + 0.2)
                continue
            return e.code, e.read().decode(errors="replace")[:200]
    return 429, "rate limited"


def snowflake_ts(sid: str | None) -> float:
    return ((int(sid) >> 22) + DISCORD_EPOCH_MS) / 1000 if sid else 0.0


def channel_folders() -> dict[str, str]:
    """channel id -> project folder, parsed from discord.channel_prompts in config.yaml."""
    from hermes_cli.config import load_config
    prompts = (load_config().get("discord") or {}).get("channel_prompts") or {}
    out = {}
    for cid, text in prompts.items():
        m = re.search(r"\(folder: (.+?)\)", str(text))
        if m:
            out[str(cid)] = m.group(1)
    return out


def protected_threads() -> set[str]:
    jobs = json.loads((HOME / "cron" / "jobs.json").read_text())
    jobs = jobs.get("jobs", jobs) if isinstance(jobs, dict) else jobs
    ids = set()
    for job in jobs:
        for key in ("deliver", "failure_deliver"):
            parts = str(job.get(key) or "").split(":")
            if len(parts) >= 3 and parts[0] == "discord":
                ids.add(parts[2])
    return ids


def guild_id(any_channel: str) -> str:
    status, ch = api("GET", f"/channels/{any_channel}")
    if status != 200:
        raise SystemExit(f"Discord 채널 조회 실패 ({status}): {ch}")
    return ch["guild_id"]


def channel_threads(cid: str, active: list[dict]) -> list[dict]:
    threads = [t for t in active if t.get("parent_id") == cid]
    before = None
    while True:
        q = f"/channels/{cid}/threads/archived/public?limit=100" + (f"&before={before}" if before else "")
        status, page = api("GET", q)
        if status != 200:
            break
        threads += page.get("threads", [])
        if not page.get("has_more") or not page.get("threads"):
            break
        before = page["threads"][-1]["thread_metadata"]["archive_timestamp"]
    return threads


def main() -> None:
    from hermes_state import SessionDB
    from hermes_state_maintenance import _LAST_ACTIVE_SQL, _not_pinned_sql
    from hermes_cli import projects_db as pdb

    lines: list[str] = []
    now = time.time()
    cutoff = now - IDLE_DAYS * 86400
    folders = channel_folders()
    db = SessionDB()

    # 1. Backfill workspace for Discord sessions.
    attached = 0
    for sid, origin in db._read_all(
            "SELECT id, origin_json FROM sessions WHERE source = 'discord' AND COALESCE(cwd, '') = ''"):
        o = json.loads(origin or "{}")
        folder = folders.get(str(o.get("parent_chat_id") or "")) or folders.get(str(o.get("chat_id") or ""))
        if folder:
            attached += 1
            if not DRY:
                db.update_session_cwd(sid, folder)
    if attached:
        lines.append(f"- 프로젝트로 연결한 디스코드 채팅: {attached}개")

    # 2. Discord thread cleanup.
    keep_ids = protected_threads()
    gid = guild_id(next(iter(folders)))
    status, active = api("GET", f"/guilds/{gid}/threads/active")
    active_threads = active.get("threads", []) if status == 200 else []
    deleted, failed = [], []
    home_channel = env_value("DISCORD_HOME_CHANNEL")  # Desktop chats outside a project report here
    for cid in [*folders, home_channel]:
        threads = [t for t in channel_threads(cid, active_threads) if t["id"] not in keep_ids]
        for t in threads:
            t["_last"] = max(snowflake_ts(t.get("last_message_id")), snowflake_ts(t["id"]))
        threads.sort(key=lambda t: t["_last"], reverse=True)
        for t in threads[KEEP:]:
            if t["_last"] >= cutoff:
                continue
            if DRY:
                deleted.append(t["name"])
                continue
            s, body = api("DELETE", f"/channels/{t['id']}")
            (deleted if s in (200, 204) else failed).append(t["name"] if s in (200, 204) else f"{t['name']} ({s})")
    if deleted:
        lines.append(f"- 디스코드 스레드 삭제{' 예정' if DRY else ''}: {len(deleted)}개 ({', '.join(deleted[:10])})")
    if failed:
        lines.append(f"- 디스코드 스레드 삭제 실패: {len(failed)}개 ({', '.join(failed[:10])})"
                     " — 봇 역할에 '스레드 관리' 권한이 필요합니다.")

    # 3. Hermes sidebar cleanup: permanently delete chats idle > IDLE_DAYS beyond the newest KEEP
    #    per group, plus anything an earlier archive-based sweep hid (auto_archived = 1).
    protected_sessions = {r[0] for r in db._read_all(
        "SELECT id FROM sessions WHERE source = 'discord' AND thread_id IN (%s)" % ",".join("?" * len(keep_ids)),
        tuple(keep_ids))} if keep_ids else set()
    rows = db._read_all(
        f"""SELECT s.id, s.cwd, {_LAST_ACTIVE_SQL} AS last_active FROM sessions s
            WHERE s.archived = 0 AND COALESCE(s.end_reason, '') <> 'compression'
              AND s.source <> 'subagent'
              AND COALESCE(s.hidden, 0) = 0 AND {_not_pinned_sql()}""")
    groups: dict[str, list] = {}
    with sqlite3.connect(HOME / "projects.db") as pconn:
        pconn.row_factory = sqlite3.Row
        for sid, cwd, last in rows:
            proj = pdb.project_for_path(pconn, cwd) if cwd else None
            groups.setdefault(proj.id if proj else "home", []).append((float(last or 0), sid))
    doomed = [sid for (sid,) in db._read_all(
        "SELECT id FROM sessions WHERE archived = 1 AND COALESCE(auto_archived, 0) = 1"
        " AND COALESCE(end_reason, '') <> 'compression'")]
    for items in groups.values():
        items.sort(reverse=True)
        doomed += [sid for last, sid in items[KEEP:] if last < cutoff]
    doomed = [s for s in dict.fromkeys(doomed) if s not in protected_sessions]
    removed, busy = 0, 0
    for sid in doomed:
        if DRY:
            removed += 1
            continue
        try:
            removed += db.delete_sessions([sid], sessions_dir=HOME / "sessions",
                                          exclude_active_write_guards=True, include_compression_chain=True) > 0
        except Exception:
            busy += 1  # mid-turn or locked: retried on the next run
    if removed:
        lines.append(f"- 왼쪽 채팅 삭제{' 예정' if DRY else ''}: {removed}개 (프로젝트별 최근 {KEEP}개 유지)")
    if busy:
        lines.append(f"- 사용 중이라 다음에 삭제: {busy}개")

    if lines:
        print(("[미리보기] " if DRY else "") + f"채널·채팅 정리 ({IDLE_DAYS}일 경과, 최근 {KEEP}개 유지)")
        print("\n".join(lines))


if __name__ == "__main__":
    main()

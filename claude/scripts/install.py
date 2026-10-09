#!/usr/bin/env python3
"""Install Claude Code agents, skills, routing and global rules into ~/.claude.

Global rules go into a managed block of ~/.claude/AGENTS.md. ~/.claude/CLAUDE.md
gets a one-line managed block importing it (@AGENTS.md) so Claude Code loads the
rules; pass --no-claude-md-pointer to leave CLAUDE.md alone.

Default is a read-only preview. Files this installer wrote before are updated
when unchanged; files edited by the user or written by others stop the run.
"""
import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import build_agents  # noqa: E402

# CLAUDE.md block. Earlier versions put the rules here; they now live in AGENTS.md.
BLOCK_START = "<!-- agent-setup:claude:begin -->"
BLOCK_END = "<!-- agent-setup:claude:end -->"
RULES_START = "<!-- agent-setup:rules:begin -->"
RULES_END = "<!-- agent-setup:rules:end -->"
POINTER = "@AGENTS.md"
BLOCK_FILES = ("AGENTS.md", "CLAUDE.md")
STATE = "agent-setup/installed.json"
# Shared core skills for every executor, then Claude-only skills.
SKILL_SOURCES = [ROOT.parent / "shared" / "skills" / "core", ROOT / "skills"]


class Conflict(RuntimeError):
    pass


def digest(data):
    return hashlib.sha256(data).hexdigest()


def planned_files(preset):
    routes = build_agents.load()
    if preset not in routes["presets"]:
        raise SystemExit("unknown preset: " + preset)
    files = {"agents/" + name: text.encode() for name, text in build_agents.agents(routes).items()}
    owners = {}
    for skills in SKILL_SOURCES:
        for folder in sorted(p for p in skills.iterdir() if (p / "SKILL.md").is_file()):
            if folder.name in owners:
                raise SystemExit("duplicate skill name: " + folder.name)
            owners[folder.name] = skills
            for path in sorted(folder.rglob("*")):
                if path.is_file() and "__pycache__" not in path.parts:
                    files["skills/" + path.relative_to(skills).as_posix()] = path.read_bytes()
    routing = {
        "preset": preset,
        "categories": {
            category: {"description": routes["descriptions"][category], "chain": chain}
            for category, chain in build_agents.resolved(routes, preset).items()
        },
    }
    files["agent-setup/routing.json"] = (json.dumps(routing, ensure_ascii=False, indent=2) + "\n").encode()
    return files


def rules_block():
    body = (ROOT / "templates" / "global-rules.md").read_text(encoding="utf-8").strip()
    return RULES_START + "\n" + body + "\n" + RULES_END


def pointer_block():
    return BLOCK_START + "\n" + POINTER + "\n" + BLOCK_END


def block_change(home, relative, block, start_marker, end_marker, state, changes, conflicts, remove=False):
    """Add, update or remove one managed block while keeping the rest of the file."""
    path = safe_target(home, relative)
    existing = path.read_text(encoding="utf-8") if path.exists() else ""
    if start_marker in existing or end_marker in existing:
        if existing.count(start_marker) != 1 or existing.count(end_marker) != 1:
            conflicts.append(relative)
            return
        start = existing.index(start_marker)
        end = existing.index(end_marker) + len(end_marker)
        current = existing[start:end]
        if not remove and current == block:
            return
        if state.get(relative) != digest(current.encode()):
            conflicts.append(relative)
            return
        if remove:
            before, after = existing[:start].rstrip("\n"), existing[end:].lstrip("\n")
            changes.append((relative, (before + ("\n\n" if before and after else "\n" if before else "") + after).encode()))
        else:
            changes.append((relative, (existing[:start] + block + existing[end:]).encode()))
    elif not remove:
        separator = "" if not existing else ("\n" if existing.endswith("\n") else "\n\n")
        changes.append((relative, (existing + separator + block + "\n").encode()))


def safe_target(home, relative):
    relative_path = Path(relative)
    if relative_path.is_absolute() or ".." in relative_path.parts:
        raise Conflict("target must stay inside Claude configuration: " + str(relative))
    target = home / relative
    for parent in [target, *target.parents]:
        if parent == home.parent:
            break
        if parent.is_symlink():
            raise Conflict("symlink in target path: " + str(parent))
    return target


def plan(home, preset, claude_md_pointer=True):
    state_path = safe_target(home, STATE)
    state = json.loads(state_path.read_text()) if state_path.is_file() else {}
    changes, conflicts = [], []
    files = planned_files(preset)
    for relative, data in files.items():
        target = safe_target(home, relative)
        if not target.exists():
            changes.append((relative, data))
            continue
        current = digest(target.read_bytes())
        if current == digest(data):
            continue
        if state.get(relative) == current:
            changes.append((relative, data))
        else:
            conflicts.append(relative)
    removals = []
    for relative, previous_hash in state.items():
        target = safe_target(home, relative)
        if relative not in files and relative not in BLOCK_FILES and target.is_file():
            if digest(target.read_bytes()) == previous_hash:
                removals.append(relative)
    blocks = {"AGENTS.md": rules_block(), "CLAUDE.md": pointer_block()}
    block_change(home, "AGENTS.md", blocks["AGENTS.md"], RULES_START, RULES_END, state, changes, conflicts)
    block_change(home, "CLAUDE.md", blocks["CLAUDE.md"], BLOCK_START, BLOCK_END, state, changes, conflicts,
                 remove=not claude_md_pointer)
    return changes, removals, conflicts, state, blocks


def install(home, preset, apply=False, claude_md_pointer=True):
    home = Path(home).expanduser().absolute()
    changes, removals, conflicts, state, blocks = plan(home, preset, claude_md_pointer)
    report = {
        "home": str(home),
        "preset": preset,
        "changes": [r for r, _ in changes],
        "removals": removals,
        "codex_plugin": codex_plugin(home),
        "aside_cli": bool(shutil.which("aside")),
    }
    if conflicts:
        raise Conflict("files differ from this installer's last copy; review them first: " + ", ".join(conflicts))
    if not changes and not removals:
        return dict(report, status="unchanged")
    if not apply:
        return dict(report, status="changes")
    backup_relative = "agent-setup/backups/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S-%f")
    backup = safe_target(home, backup_relative)
    for relative, _ in changes:
        target = safe_target(home, relative)
        safe_target(home, str(target.with_name("." + target.name + ".agent-setup-tmp").relative_to(home)))
    for relative in [r for r, _ in changes] + removals:
        target = safe_target(home, relative)
        if target.exists():
            saved = backup / relative
            saved.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(target, saved)
    for relative, data in changes:
        target = safe_target(home, relative)
        target.parent.mkdir(parents=True, exist_ok=True)
        temporary = target.with_name("." + target.name + ".agent-setup-tmp")
        temporary.write_bytes(data)
        os.replace(temporary, target)
        if relative in BLOCK_FILES:
            if relative == "CLAUDE.md" and not claude_md_pointer:
                state.pop(relative, None)
            else:
                state[relative] = digest(blocks[relative].encode())
        else:
            state[relative] = digest(data)
    for relative in removals:
        safe_target(home, relative).unlink()
        state.pop(relative, None)
    state_path = safe_target(home, STATE)
    state_path.parent.mkdir(parents=True, exist_ok=True)
    state_path.write_text(json.dumps(state, indent=2, sort_keys=True) + "\n")
    report["backup"] = str(backup) if backup.exists() else None
    return dict(report, status="applied")


def verify_loading(timeout=180, home=None):
    """Ask Claude Code to quote the first rules heading; needs the claude CLI and login."""
    claude = shutil.which("claude")
    if not claude:
        return {"status": "skipped", "reason": "claude CLI not found"}
    expected = "작업 원칙"
    prompt = ("사용자 전역 지침(AGENTS.md 관리 구간)의 첫 번째 '##' 제목을 따옴표 없이 그대로 한 줄로만 답해. "
              "그런 지침이 보이지 않으면 NONE 이라고만 답해.")
    import subprocess
    try:
        environment = os.environ.copy()
        if home is not None:
            environment["CLAUDE_CONFIG_DIR"] = str(Path(home).expanduser().absolute())
        done = subprocess.run([claude, "-p", prompt], capture_output=True, text=True, timeout=timeout, env=environment)
    except subprocess.TimeoutExpired:
        return {"status": "unknown", "reason": "timeout"}
    answer = done.stdout.strip()
    loaded = done.returncode == 0 and answer == expected
    return {"status": "loaded" if loaded else "not_loaded", "answer": answer[:200], "exit_code": done.returncode}


def codex_plugin(home):
    path = home / "plugins" / "installed_plugins.json"
    if not path.is_file():
        return "missing"
    plugins = json.loads(path.read_text()).get("plugins", {})
    return "installed" if "codex@openai-codex" in plugins else "missing"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--home", default=os.environ.get("CLAUDE_CONFIG_DIR") or str(Path.home() / ".claude"))
    parser.add_argument("--preset", default=build_agents.load()["default_preset"],
                        choices=sorted(build_agents.load()["presets"]))
    parser.add_argument("--apply", action="store_true", help="write changes; default is preview")
    parser.add_argument("--no-claude-md-pointer", action="store_true",
                        help="leave ~/.claude/CLAUDE.md without the @AGENTS.md import")
    parser.add_argument("--verify-loading", action="store_true",
                        help="ask terminal Claude Code (one model call) whether the global rules are loaded")
    args = parser.parse_args()
    if args.verify_loading:
        result = verify_loading(home=args.home)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if result["status"] == "loaded" else 1
    try:
        result = install(args.home, args.preset, args.apply, not args.no_claude_md_pointer)
    except Conflict as error:
        print(json.dumps({"status": "conflict", "detail": str(error)}, ensure_ascii=False))
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

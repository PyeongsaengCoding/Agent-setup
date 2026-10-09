#!/usr/bin/env python3
"""Compose each executor's global instructions from shared/rules.

Default writes the generated files; --check fails when they are out of date.
"""
import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
RULES = ROOT / "shared" / "rules"
OUTPUTS = {
    # Installed to ~/.codex/AGENTS.md by codex/scripts/apply_managed.py ({{...}} rendered there).
    "codex/instructions/AGENTS.md": ("# 전역 작업 지침 (Agent-setup · Codex)", ["common", "skills", "aside", "routing-codex"]),
    # Installed as the managed block of ~/.claude/AGENTS.md by claude/scripts/install.py.
    "claude/templates/global-rules.md": (None, ["common", "skills", "aside", "routing-claude"]),
    # Added to the selected Hermes profile's SOUL.md by hermes/scripts/install_global_rules.py.
    # Hermes keeps its own Aside and document-delivery blocks and uses OMH for routing and skills.
    "hermes/templates/common-rules.md": (None, ["common"]),
}


def compose(title, parts):
    sections = [(RULES / (name + ".md")).read_text(encoding="utf-8").strip() for name in parts]
    body = "\n\n".join(sections)
    return (title + "\n\n" + body if title else body) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="only verify generated files are current")
    args = parser.parse_args()
    stale = []
    for relative, (title, parts) in OUTPUTS.items():
        target = ROOT / relative
        text = compose(title, parts)
        current = target.read_text(encoding="utf-8") if target.exists() else None
        if current == text:
            continue
        if args.check:
            stale.append(relative)
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(text, encoding="utf-8")
            print("wrote " + relative)
    if stale:
        print("out of date (run python3 scripts/build_rules.py): " + ", ".join(stale))
        return 1
    if args.check:
        print("global rules match shared/rules for " + str(len(OUTPUTS)) + " executors")
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Run each executor's existing local checks without applying configuration."""
import argparse
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
# Every executor first confirms its global instructions match shared/rules.
RULES = ("../scripts/build_rules.py", "--check")
CHECKS = {
    "codex": (RULES, ("-m", "unittest", "discover", "-s", "tests", "-v"),),
    "claude": (
        RULES,
        ("scripts/build_agents.py", "--check"),
        ("-m", "unittest", "discover", "-s", "tests", "-v"),
    ),
    "hermes": (
        RULES,
        ("scripts/check.py",),
        ("-m", "unittest", "discover", "-s", "tests", "-v"),
    ),
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--executor", choices=("all", *CHECKS), default="all")
    args = parser.parse_args()
    if sys.version_info < (3, 12):
        parser.error("Python 3.12 or newer is required")
    selected = CHECKS if args.executor == "all" else (args.executor,)
    for executor in selected:
        for command in CHECKS[executor]:
            result = subprocess.run([sys.executable, *command], cwd=ROOT / executor)
            if result.returncode:
                print(f"FAIL executor: {executor}", flush=True)
                return result.returncode
        print(f"PASS executor: {executor}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

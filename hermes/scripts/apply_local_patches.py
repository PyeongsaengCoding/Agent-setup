#!/usr/bin/env python3
"""Check or re-apply Agent-setup's local patch sets on top of the official Hermes releases.

Each target is an official checkout (Hermes source, provider-usage plugin) at its
latest stable release tag. The matching patch in hermes/patches/<target>/<tag>.patch
holds this user's customizations. Default is a read-only report:

  applied     the checkout already contains the patch
  applicable  the patch applies cleanly; rerun with --apply
  conflict    the patch does not apply; port it to the new release first
  no_patch    no patch exists for the checkout's release tag

  python3 hermes/scripts/apply_local_patches.py            # report
  python3 hermes/scripts/apply_local_patches.py --apply    # apply applicable patches
"""
import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATCHES = ROOT / 'patches'


def targets(home):
    return {
        'hermes-agent': home / 'hermes-agent',
        'provider-usage': home / 'plugins' / 'provider-usage',
    }


def git(checkout, *args):
    return subprocess.run(['git', '-C', str(checkout), *args], capture_output=True, text=True)


def release_tag(checkout):
    result = git(checkout, 'describe', '--tags', '--exact-match', 'HEAD')
    return result.stdout.strip() if result.returncode == 0 else None


def status(name, checkout):
    if not (checkout / '.git').exists():
        return {'target': name, 'path': str(checkout), 'status': 'missing'}
    tag = release_tag(checkout)
    patch = PATCHES / name / f'{tag}.patch' if tag else None
    row = {'target': name, 'path': str(checkout), 'tag': tag, 'patch': str(patch) if patch else None}
    if patch is None or not patch.is_file():
        available = sorted(p.stem for p in (PATCHES / name).glob('*.patch'))
        return {**row, 'status': 'no_patch', 'available': available}
    if git(checkout, 'apply', '--reverse', '--check', str(patch)).returncode == 0:
        return {**row, 'status': 'applied'}
    check = git(checkout, 'apply', '--check', str(patch))
    if check.returncode == 0:
        return {**row, 'status': 'applicable'}
    return {**row, 'status': 'conflict', 'detail': check.stderr.strip()[-800:]}


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--home', type=Path, default=Path(os.environ.get('HERMES_HOME', Path.home() / '.hermes')))
    parser.add_argument('--apply', action='store_true', help='apply patches whose status is applicable')
    args = parser.parse_args()
    rows = []
    for name, checkout in targets(args.home.expanduser()).items():
        row = status(name, checkout)
        if args.apply and row['status'] == 'applicable':
            result = git(checkout, 'apply', row['patch'])
            row = status(name, checkout) if result.returncode == 0 else {**row, 'status': 'apply_failed',
                                                                          'detail': result.stderr.strip()[-800:]}
        rows.append(row)
    print(json.dumps(rows, ensure_ascii=False, indent=2))
    return 0 if all(r['status'] == 'applied' for r in rows) else 1


if __name__ == '__main__':
    sys.exit(main())

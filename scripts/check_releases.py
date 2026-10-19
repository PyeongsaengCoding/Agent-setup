#!/usr/bin/env python3
"""Compare Agent-setup's pinned external components with their latest stable releases.

Reads the pins in hermes/manifest.json, codex/inventories/tools.lock.json,
shared/skills/omh/SOURCE.json and codex/inventories/external-skills.json (one
row per external skill source repository), asks GitHub for each repository's latest
published release (drafts and pre-releases excluded), and resolves the release
tag to a commit with `git ls-remote`. Prints one row per pin and exits 1 when
any pin is behind its latest stable release. Needs network access.

  python3 scripts/check_releases.py          # table
  python3 scripts/check_releases.py --json   # machine-readable
"""
import argparse
import json
import os
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(path):
    return json.loads((ROOT / path).read_text())


def slug(url):
    return url.rstrip('/').removesuffix('.git').split('github.com/')[1]


def external_skill_pins(catalog):
    """Group the external skill catalog by source repository.

    Every skill from one repository must share the same `ref`; a repository whose
    skills disagree is reported with pinned value 'mixed' so it never shows as current.
    """
    groups = {}
    for name, item in catalog['skills'].items():
        groups.setdefault(slug(item['sourceUrl']), []).append((name, item.get('ref')))
    rows = []
    for repo, items in groups.items():
        refs = {ref for _, ref in items}
        pinned = refs.pop() if len(refs) == 1 else 'mixed'
        rows.append((f'외부 스킬 {repo} {len(items)}개 (codex/inventories/external-skills.json)', repo, 'commit', pinned))
    return rows


def pins():
    hermes = load('hermes/manifest.json')
    lock = load('codex/inventories/tools.lock.json')
    omh_copy = load('shared/skills/omh/SOURCE.json')
    rows = [('Hermes 본체 (hermes/manifest.json upstream)', slug(hermes['upstream']['repo']), 'commit', hermes['upstream']['commit'])]
    for plugin in hermes['plugins']:
        rows.append((f"Hermes 플러그인 {plugin['name']} (hermes/manifest.json)", slug(plugin['repo']), 'commit', plugin['commit']))
    rows.append(('OMH Hermes 기준 (hermes/manifest.json omh)', slug(hermes['omh']['repo']), 'commit', hermes['omh']['reference_commit']))
    rows.append(('OMH Codex 기준 (codex/inventories/tools.lock.json)', slug(lock['omh']['source']), 'commit', lock['omh']['commit']))
    rows.append(('OMH 스킬 사본 (shared/skills/omh/SOURCE.json)', slug(omh_copy['upstream']), 'version', omh_copy['version']))
    for key in ('codegraph', 'gam'):
        rows.append((f'{key} (codex/inventories/tools.lock.json)', slug(lock[key]['source']), 'commit', lock[key]['commit']))
    rows.extend(external_skill_pins(load('codex/inventories/external-skills.json')))
    return rows


def latest_release(repo):
    request = urllib.request.Request(f'https://api.github.com/repos/{repo}/releases/latest',
                                     headers={'Accept': 'application/vnd.github+json', 'User-Agent': 'agent-setup'})
    token = os.environ.get('GITHUB_TOKEN')
    if token:
        request.add_header('Authorization', 'Bearer ' + token)
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            return json.load(response)['tag_name']
    except urllib.error.HTTPError as error:
        if error.code == 404:
            return None
        raise


def tag_commit(repo, tag):
    out = subprocess.run(['git', 'ls-remote', '--tags', f'https://github.com/{repo}', tag, tag + '^{}'],
                         capture_output=True, text=True, check=True, timeout=60).stdout
    refs = {}
    for line in out.splitlines():
        if line:
            sha, ref = line.split('\t')
            refs[ref] = sha
    return refs.get(f'refs/tags/{tag}^{{}}') or refs.get(f'refs/tags/{tag}')


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args()
    results, cache = [], {}
    for label, repo, kind, pinned in pins():
        if repo not in cache:
            tag = latest_release(repo)
            cache[repo] = (tag, tag_commit(repo, tag) if tag else None)
        tag, commit = cache[repo]
        if tag is None:
            status = 'no_release'
        elif kind == 'version':
            status = 'current' if tag.lstrip('v') == pinned.lstrip('v') else 'behind'
        else:
            status = 'current' if commit == pinned else 'behind'
        results.append({'component': label, 'repo': repo, 'pinned': pinned, 'latest_tag': tag,
                        'latest_commit': commit, 'status': status})
    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        for row in results:
            pinned = (row['pinned'] or '기본 브랜치')[:12]
            latest = f"{row['latest_tag']} ({(row['latest_commit'] or '')[:12]})" if row['latest_tag'] else '없음'
            print(f"{row['status']:<10} {row['component']}: 고정 {pinned} / 최신 정식 {latest}")
    return 1 if any(row['status'] == 'behind' for row in results) else 0


if __name__ == '__main__':
    sys.exit(main())

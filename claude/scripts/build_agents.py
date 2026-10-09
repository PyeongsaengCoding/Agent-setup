#!/usr/bin/env python3
"""Build Claude Code route agents from routes/claude-code.json."""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ROUTES = ROOT / "routes" / "claude-code.json"
AGENTS = ROOT / ".claude" / "agents"
CODEX_AGENT = "codex:codex-rescue"


def load():
    return json.loads(ROUTES.read_text(encoding="utf-8"))


def family(model):
    return model.split("-")[1]


def executor(category, model):
    if model.startswith("claude-"):
        return f"route-{category}-{family(model)}"
    return CODEX_AGENT


def resolved(routes, preset):
    return {
        category: [dict(entry, executor=executor(category, entry["model"])) for entry in chain]
        for category, chain in routes["presets"][preset].items()
    }


def render(name, category, description, model, effort):
    return "\n".join([
        "---",
        f"name: {name}",
        f"description: {category} 분류({description})의 위임 작업. ~/.claude/AGENTS.md의 모델 라우팅이 이 에이전트를 고를 때 사용한다.",
        f"model: {model}",
        f"effort: {effort}",
        "---",
        "",
        "위임받은 작업을 지정된 파일 범위 안에서 끝낸다.",
        "변경한 파일, 직접 실행한 검증과 결과, 확인하지 못한 항목을 보고한다.",
        "",
    ])


def agents(routes):
    files = {}
    for preset in routes["presets"]:
        for category, chain in resolved(routes, preset).items():
            for entry in chain:
                name = entry["executor"]
                if name == CODEX_AGENT:
                    continue
                text = render(name, category, routes["descriptions"][category], entry["model"], entry["effort"])
                if files.setdefault(name + ".md", text) != text:
                    raise SystemExit(f"{name}: presets disagree on model or effort")
    return files


def check():
    expected = agents(load())
    actual = {p.name: p.read_text(encoding="utf-8") for p in AGENTS.glob("route-*.md")}
    return sorted(set(expected.items()) ^ set(actual.items()))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="compare without writing")
    args = parser.parse_args()
    if args.check:
        differences = check()
        if differences:
            raise SystemExit("agent files differ from routes: " + ", ".join(sorted({n for n, _ in differences})))
        print(f"{len(agents(load()))} route agents match routes/claude-code.json")
        return 0
    expected = agents(load())
    AGENTS.mkdir(parents=True, exist_ok=True)
    for stale in AGENTS.glob("route-*.md"):
        if stale.name not in expected:
            stale.unlink()
    for name, text in expected.items():
        (AGENTS / name).write_text(text, encoding="utf-8")
    print(f"wrote {len(expected)} route agents")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

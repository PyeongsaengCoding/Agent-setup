# Claude Code 구성 원본

이 폴더는 `~/.claude`에 설치할 Claude Code 원본이다. 라우팅은 routes/claude-code.json, 에이전트는 scripts/build_agents.py로 생성한다. 전역 규칙(templates/global-rules.md)은 직접 고치지 않고 `../shared/rules/`를 고친 뒤 `python3 ../scripts/build_rules.py`로 만든다. 라우팅이나 규칙을 바꾸면 생성 명령과 tests를 실행한다.

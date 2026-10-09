---
name: agent-setup-maintenance
description: 이 컴퓨터의 AI 작업 환경(Claude Code·Codex·Hermes의 전역 지침, 모델 라우팅, 공통 스킬, CodeGraph·Aside 연결)을 추가·변경·재설치·제거할 때 Agent-setup 원본과 설치 기록을 기준으로 처리한다.
---

# AI 작업 환경 변경

관리 원본은 Agent-setup 저장소다. 설치 기록은 실행기별로 있다. Codex는 `~/Library/Application Support/codex-setup/installation.json`의 `setup_root`, Claude Code는 `~/.claude/agent-setup/installed.json`(설치한 파일 목록)이다. 기록이 없거나 경로가 사라졌으면 사용자의 체크아웃을 찾거나 공개 저장소에서 다시 받는다. 먼저 README.md와 docs/setup-design.md를 읽고, 대상 실행기 폴더(claude/·codex/·hermes/)의 안내를 필요한 범위에서 읽는다.

1. 설치기의 미리보기로 현재 설치본과 원본의 차이를 확인한다. 홈에 새로 생긴 파일을 자동으로 원본에 채택하거나 삭제하지 않는다.
2. 공통 스킬은 `shared/skills/`, 전역 지침은 `shared/rules/`, 실행기 전용 내용은 해당 실행기 폴더에서 고친다. 홈의 설치본을 직접 고치지 않는다.
3. 설치기를 미리보기 → 적용 순서로 실행한다. 사용자가 고친 설치본은 덮어쓰지 않고 충돌로 보고한다. 적용 전 백업 경로를 확인한다.
4. 설정 파일은 관리 구간과 설치기가 관리하는 키만 바꾼다. 인증·세션·기억·로그·캐시는 저장소에 복사하지 않는다.
5. 파일 적용, 실행기의 발견(새 세션에서 스킬·지침·도구가 보이는지), 실제 작업 성공을 나눠 확인하고 보고한다. 빈 임시 홈에서 성공한 결과를 실제 설치 완료로 보고하지 않는다.
6. 저장소 검사(`python3 scripts/check.py`, `python3 -m unittest discover -s tests -v`)를 실행한다. 커밋·푸시는 사용자가 요청한 범위에서 한다.

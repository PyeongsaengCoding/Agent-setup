# Claude Code 작업 환경 설치 (AI용)

[설치 공통 기준](../docs/install-common.md)을 따른다. 아래는 Claude Code에 갖출 것과 완료 기준이다. 설치 방법은 AI가 정한다.

## 갖출 것

| 항목 | 기준 |
|---|---|
| Claude Code | 설치·로그인 상태 |
| Codex 플러그인 | `openai/codex-plugin-cc`의 `codex@openai-codex`와 Codex CLI 로그인. GPT 라우팅 항목을 실행한다. 사용자가 GPT를 쓰지 않으면 생략하고, 그 항목은 다음 Claude 항목으로 넘어간다 |
| 모델 라우팅 | Claude 넉넉형 (사용자가 원하면 GPT 넉넉형). 분류별 하위 에이전트 23개와 `agent-setup/routing.json` |
| 스킬 | [스킬 표](../docs/skills.md)의 Claude 열 (공통 26개 + codex + 외부 37개) |
| 전역 지침 | `~/.claude/AGENTS.md` 관리 구간, Claude Code가 읽도록 `~/.claude/CLAUDE.md`에 `@AGENTS.md` 한 줄 |
| MCP | CodeGraph, GAM (사용자 범위) |
| Aside | 공통 기준대로 |

외부 스킬 37개(Azure·마케팅 등)는 Codex와 같은 목록(`../codex/inventories/external-skills.json`)을 `../codex/scripts/install_external_skills.py`의 `--skills-dir`로 `~/.claude/skills/`에 설치하고, Codex와 같은 설명 조정(`../codex/config/skill-descriptions.json`)을 `apply_skill_descriptions.py --skill-root`로 적용한다.

`Agent-setup/claude/`에서 Python 3.12 이상으로 실행한다. `scripts/install.py`는 라우팅·공통 26개 스킬·Claude 전용 codex 스킬·전역 지침을 설치한다(미리보기 → `--apply`, 다시 실행하면 `unchanged`). 외부 37개 스킬은 위 외부 스킬 설치기로 따로 적용하며, [README의 설치 명령](README.md#설치)을 따른다. 사용자 설정 폴더를 별도로 쓰면 설치기의 `--home`, 외부 설치기의 `--skills-dir`, 설명 조정의 `--skill-root`를 같은 폴더 기준으로 지정한다. 사용자가 고친 파일은 충돌로 알리며, 바꾸기 전 파일은 해당 사용자 설정 폴더의 `agent-setup/backups/`에 남긴다.

이 폴더의 설치 절차는 Claude Code 전역 환경을 준비한다. 제품 생성·기존 제품 기준 적용은 pycoding-prompt의 절차를 따르며, 제품 파일·프로젝트 의존성·lint·CI는 대상 제품 저장소에서 관리한다. CodeGraph 색인과 GAM의 실제 지식·인증 정보는 사용자 데이터 경로에서 관리한다.

## 완료 기준

새 Claude Code 세션에서 확인하고 각 항목을 완료·실패·미확인으로 보고한다.

1. 전역 지침 로딩: `scripts/install.py --verify-loading` 결과가 `loaded`
2. `/agents`에 `route-*` 23개와 `codex:codex-rescue`(플러그인 설치 시)
3. Claude 항목 하나와 GPT를 사용한다면 GPT 항목 하나로 작은 읽기 전용 작업을 위임해 실제 실행 모델 확인
4. 관련 요청에서 스킬 사용 (예: "테스트 먼저 작성해줘" → tdd)
5. CodeGraph·GAM MCP 도구 실제 응답
6. Aside를 설치했다면 `repl`로 페이지를 열고 결과 읽기

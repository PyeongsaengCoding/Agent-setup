# Agent-setup

**AI 작업 환경 설치 원본.** Claude Code·Codex·Hermes 중 쓰고 싶은 AI를 골라 아래 요청 한 문장을 AI에게 보내면, AI가 이 저장소를 읽고 그 컴퓨터(macOS·Windows)에 맞는 방법으로 모델 라우팅·스킬·도구·전역 지침을 설치하고 실제 동작까지 확인한다. 설치가 끝나면 바로 프로젝트를 시작하면 된다.

| AI | 이런 사람에게 | 지원 OS | 설치 안내 (AI가 읽는 문서) |
|---|---|---|---|
| Claude Code | Claude를 주로 쓰고, 필요할 때 GPT(Codex)도 섞어 쓰고 싶다 | macOS, Windows | [claude/INSTALL_FOR_AGENTS.md](claude/INSTALL_FOR_AGENTS.md) |
| Codex | ChatGPT·Codex(GPT)만 쓴다 | macOS (Windows는 WSL2) | [codex/INSTALL_FOR_AGENTS.md](codex/INSTALL_FOR_AGENTS.md) |
| Hermes | Hermes Desktop에서 GPT·Claude를 함께 쓴다 | Apple Silicon Mac | [hermes/INSTALL_FOR_AGENTS.md](hermes/INSTALL_FOR_AGENTS.md) |

## AI에게 보낼 요청

파일과 명령을 쓸 수 있는 AI 대화에 하나를 골라 보낸다. 무엇을 어떻게 설치할지는 AI가 이 저장소의 설치 안내와 그 컴퓨터 상태를 보고 정한다.

| AI | 요청 |
|---|---|
| Claude Code | `https://github.com/PyeongsaengCoding/Agent-setup 를 받아 이 컴퓨터에 Claude Code 작업 환경을 구성해줘.` |
| Codex | `https://github.com/PyeongsaengCoding/Agent-setup 를 받아 이 컴퓨터에 Codex 작업 환경을 구성해줘.` |
| Hermes | `https://github.com/PyeongsaengCoding/Agent-setup 를 받아 이 컴퓨터에 Hermes 작업 환경을 구성해줘.` |

설치를 맡은 AI는 고른 AI의 설치 안내(`<AI 폴더>/INSTALL_FOR_AGENTS.md`)를 따른다. 지금 설치된 것을 먼저 확인하고, 사용자가 직접 고친 설정은 덮어쓰지 않으며, 로그인·권한·충돌만 사용자에게 묻고, 실제 동작 확인 뒤 완료한 것과 남은 것을 알려준다.

## 설치되는 것

| 항목 | Claude Code | Codex | Hermes |
|---|---|---|---|
| 모델 라우팅 | 12개 분류별 Claude 하위 에이전트 + GPT는 Codex 플러그인 | 12개 분류별 GPT 모델·추론 | OMH 프리셋 |
| 스킬 | 공통 26개 + codex + 외부 37개 | 공통 26개 + 외부 37개 | Hermes 공식 57개 + 공통 10개 + 외부 37개 + OMH 142개 |
| 전역 지침 | `~/.claude/AGENTS.md` | `~/.codex/AGENTS.md` | `SOUL.md` 관리 구간 |
| 코드 탐색 | CodeGraph | CodeGraph | CodeGraph |
| 기억 | GAM | GAM | GAM + Hermes 메모리 |
| 브라우저 | Aside | Aside | Aside |

AI별 스킬은 [스킬 표](docs/skills.md), 자세한 구성과 이유는 [구성 설계](docs/setup-design.md), 세 AI의 차이는 [비교](docs/comparison.md)에 있다.

## 설치 뒤

새 대화를 열어 프로젝트 작업을 시작한다. 새 제품 저장소를 만들거나 기존 제품에 문서 기준을 적용할 때는 [pycoding-prompt](https://github.com/PyeongsaengCoding/pycoding-prompt)의 해당 절차를 사용한다. 생성·적용 뒤 제품별 규칙과 현재 계약은 그 프로젝트의 AGENTS.md와 docs/에서 관리한다. 설정을 바꾸고 싶으면 AI에게 "Agent-setup 기준으로 ~를 바꿔줘"라고 요청하면 agent-setup-maintenance 스킬 절차로 처리한다.

## 저장소 관리

- 공통 원본: 전역 지침 `shared/rules/`, 공통 스킬 `shared/skills/`. 지침을 고치면 `scripts/build_rules.py`로 각 AI용 파일을 다시 만든다.
- 검사: Python 3.12 이상에서 `scripts/check.py`(세 AI 원본 검사)와 `tests/` 단위시험을 실행한다. 실제 컴퓨터의 설치 완료는 [설치 완료 기준](docs/verification.md)과 각 실행기 설치 안내의 결과로 판정한다.
- 출처와 라이선스: [이관 목록](docs/import-manifest.json), [출처 안내](docs/provenance.md), [스킬 출처](shared/skills/SOURCES.md).

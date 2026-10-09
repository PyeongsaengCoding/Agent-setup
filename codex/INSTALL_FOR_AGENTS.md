# Codex 작업 환경 설치 (AI용)

[설치 공통 기준](../docs/install-common.md)을 따른다. 아래는 Codex에 갖출 것과 완료 기준이다. 설치 방법은 AI가 정한다. 모델은 계정에서 쓸 수 있는 GPT 계열(Astra·Sol·Luna)만 쓴다.

Agent-setup 전체 체크아웃을 사용한다. 이 문서의 `scripts/`, `config/`, `inventories/` 경로는 `codex/` 기준이며, 공통 스킬은 형제 폴더 `shared/skills/`에서 읽는다. 저장소 루트에서 계획을 확인할 때는 `python3 codex/scripts/setup_runtime.py plan`, 적용할 때는 `python3 codex/scripts/setup_runtime.py apply`를 사용한다. Python 3.12 이상을 준비한다.

## 갖출 것

| 항목 | 기준 |
|---|---|
| Codex | 앱 또는 CLI 설치·로그인 상태 |
| 모델 라우팅 | 12개 분류별 GPT 모델·추론 (`working-method.md`, `models.json`) |
| 스킬 | [스킬 표](../docs/skills.md)의 Codex 열 (공통 26개 + 외부 37개), `~/.agents/skills/` |
| 전역 지침 | `$CODEX_HOME/AGENTS.md` (기본 `~/.codex/AGENTS.md`) |
| MCP | CodeGraph, GAM (`~/.codex/config.toml`, 다른 설정 키 보존) |
| Aside | 공통 기준대로 |

macOS에서는 `scripts/setup_runtime.py`가 전역 지침·스킬·GAM·CodeGraph를 설치한다(`plan`으로 계획 확인 → `apply`). Codex 앱·CLI 로그인과 Aside 준비는 공통 기준에 따라 별도로 확인한다. 다른 OS에서는 `scripts/apply_managed.py`(전역 지침·모델 파일)와 `scripts/install_core_skills.py`(스킬)를 쓰고, 도구는 공식 문서대로 준비한다. Windows는 WSL2의 Linux 홈에서 구성하고 해당 환경의 도구·서비스 연결을 별도로 검증한다. [기존 설치 이관](05-change-management.md#기존-codex-setup-설치-이관)은 새 원본 경로와 사용자 수정 여부를 함께 확인한다.

## 완료 기준

[macOS 완료 기준](10-new-machine.md)과 [앱 작업 준비](15-local-task-readiness.md)를 따른다. 새 Codex 작업에서 스킬·GAM·CodeGraph가 보이고 실제로 응답하는지, 분류별 모델 위임이 실제로 실행되는지 확인하고 완료·실패·미확인으로 보고한다.

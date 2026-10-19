# Hermes에서 Agent-setup과 OMH의 역할 나눔

확인일: 2026-10-20(KST). Hermes v0.22.2, OMH v4.0.0 기준.

Hermes에서는 Agent-setup이 설치한 구성과 OMH가 설치한 구성이 함께 동작한다. Agent-setup은 이 사용자의 작업 원칙·스킬·모델 정책·도구 연결을 설치하고, OMH는 작업 분류·워크플로 스킬·분류별 위임 모델을 제공한다. Claude Code·Codex는 OMH를 실행하지 않고 Agent-setup이 넣은 OMH 스킬 사본(`shared/skills/omh/`)과 각 실행기 지침을 쓴다.

## 영역별 구성

| 영역 | Agent-setup에만 있는 것 | OMH에만 있는 것 | 둘 다 있을 때 동작 |
|---|---|---|---|
| 스킬 | `~/.hermes/skills/`: Hermes 공식 57개, 공통 스킬(GAM·CodeGraph·코드 검토·한국어 다듬기 등), 외부 스킬, 작업 중 만든 스킬 | `~/.local/share/omh/current/skills/`: OMH 워크플로 144개(`omh-*`, `ulw-*`) | 이름이 같으면 Hermes가 `프로젝트 스킬 → ~/.hermes/skills → skills.create_dir → 외부 폴더(OMH)` 순서로 앞쪽을 쓴다(`agent/skill_utils.py:381`). 같은 순위 안의 같은 이름은 거부한다. 2026-10-20 기준 이름 충돌 0개. 이름이 다르고 역할이 겹치면(예: `coding-code-review`·`omh-code-review`) 둘 다 목록에 나오고, 요청과 설명에 맞는 쪽을 고른다 |
| 전역 지침 | 프로필 `SOUL.md`의 공통 작업 원칙·Aside·문서 전달 구간(`scripts/install_global_rules.py`) | 매 턴 붙는 OMH 안내(분류 힌트·스킬 후보), 프로젝트 `AGENTS.md`의 `omh:agent-instructions` 구간 | 현재 사용자 지시 → 가장 가까운 프로젝트 `AGENTS.md` → 전역 지침 순서로 따른다. OMH 안내는 구조·내용만 정하고, 답변 언어·말투는 `SOUL.md`를 따른다 |
| 모델 라우팅 | 설치 원본 프리셋(`hermes/routing-presets/`), 메인 대화 기본 모델·fallback 설정 | 분류별 기본 체인(패키지 내장), 실행값 파일 `~/.omh/routing/model-chains.json`, 위임 직전 라우팅 도구 | 설치 때 Agent-setup 프리셋을 `omh model-chains set`으로 넣으면 그 분류는 `override`가 되어 OMH 기본값보다 우선한다. OMH 업데이트도 `override`를 유지한다. 분류 체인은 하위 에이전트(`delegate_task`)에만 적용되고, 메인 대화·cron·칸반은 Hermes 기본 모델을 쓴다 |
| 기억 | GAM(`global-memory` MCP): 프로젝트 결정·검증된 해결 경험 | OMH 기억(Hermes 기억 제공자 `omh`): Hermes 작업 방식의 교훈 | 프로젝트 지식은 GAM에 저장해 Claude·Codex와 함께 쓰고, OMH 기억에는 Hermes 실행 교훈만 둔다. Hermes 기본 기억(`MEMORY.md`·`USER.md`)은 모든 세션에 필요한 사실만 둔다 |
| 코드 탐색 | CodeGraph MCP와 `codegraph-context` 스킬(코드 작업 시작 시 상시 사용) | `omh-codegraph-refresh` 워크플로 | 공통 지침이 CodeGraph MCP 사용을 정하고, OMH 워크플로는 색인 갱신 계획이 필요할 때 쓴다 |
| 브라우저 | Aside 설치와 `repl` 직접 조작 규칙 | `omh-browser` 정책 안내(로그인·클릭·폼 작업 범위) | 조작 도구는 Aside 규칙을 따르고, 권한·확인 범위는 OMH 안내를 함께 적용한다 |
| 플러그인 | `provider-usage`, `web-codex-search`, `desktop-discord-reports`, `discord-project-sidebar` | `omh` 플러그인(`omh_*` 도구·턴 훅) | 이름이 달라 각자 등록된다. 같은 이벤트를 쓰는 훅은 모두 실행된다 |
| Hermes 본체 | 런타임 호환 패치 2개, 계정 선택·사용량 표시 로컬 수정 | 없음 | `hermes update --backup`이 로컬 수정을 stash에 보관하고 새 버전에 다시 적용한다 |
| 프로젝트 식별 | 없음 | OMH 기억이 프로젝트를 구분하는 식별자(Git 원격 주소로 자동 결정) | 프로젝트마다 할 초기화는 없다. 식별이 `unresolved`인 프로젝트만 그 폴더에서 `omh memory project-identity init`을 실행한다. OMH 4.0.0에는 `omh init` 명령이 없다 |
| 업데이트 | 외부 구성요소를 최신 정식 릴리스 태그로 고정하고 `scripts/check_releases.py`로 확인 | `omh update`가 자기 명령 패키지·워크플로를 갱신 | [업데이트 절차](model-routing.md#업데이트)의 한 블록으로 Hermes·OMH를 함께 올리고, 저장소 고정값을 맞춘다 |
| Claude Code·Codex | OMH 스킬 사본, 실행기별 라우팅·지침 | 실행 런타임 없음 | Claude·Codex 전역 지침의 `OMH 워크플로 스킬` 절이 `omh_*` 도구를 각 실행기 도구로 대응시킨다 |

## 프로젝트 식별 확인

```bash
cd <프로젝트>
omh memory project-identity show
```

`"state":"resolved"`면 그대로 쓴다. `unresolved`면 `diagnostics` 값을 확인한다. `remote_absent`는 Git 원격을 연결하거나 `init`으로 식별자를 만든다. `git_metadata_unreadable`은 저장소 상태를 먼저 고친다. 2026-10-20 점검에서 `~/Downloads/Coding` 아래 Git 프로젝트 38개 중 36개가 자동으로 식별됐다.

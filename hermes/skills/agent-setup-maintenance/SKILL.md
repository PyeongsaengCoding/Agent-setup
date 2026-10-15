---
name: agent-setup-maintenance
description: 이 컴퓨터의 AI 작업 환경(Claude Code·Codex·Hermes의 전역 지침, 모델 라우팅, 공통 스킬, CodeGraph·Aside 연결)을 추가·변경·재설치·제거할 때 Agent-setup 원본과 설치 기록을 기준으로 처리한다.
---

# AI 작업 환경 변경

관리 원본은 Agent-setup 저장소다. 설치 기록은 실행기별로 있다. Codex는 `~/Library/Application Support/codex-setup/installation.json`의 `setup_root`, Claude Code는 `~/.claude/agent-setup/installed.json`(설치한 파일 목록)이다. 기록이 없거나 경로가 사라졌으면 사용자의 체크아웃을 찾거나 공개 저장소에서 다시 받는다. 먼저 README.md와 docs/setup-design.md를 읽고, 대상 실행기 폴더(claude/·codex/·hermes/)의 안내를 필요한 범위에서 읽는다.

1. 설치기의 미리보기로 현재 설치본과 원본의 차이를 확인한다. 홈에 새로 생긴 파일을 자동으로 원본에 채택하거나 삭제하지 않는다.
2. 공통 스킬은 `shared/skills/`, 전역 지침은 `shared/rules/`, 실행기 전용 내용은 해당 실행기 폴더에서 고친다. 배포 파일은 원본과 설치 절차로 갱신하고, 실행 중 설정은 해당 실행기의 지원 명령과 검증된 설정 스키마로 적용한다.
3. 설치기를 미리보기 → 적용 순서로 실행한다. 사용자가 고친 설치본은 덮어쓰지 않고 충돌로 보고한다. 적용 전 백업 경로를 확인한다.
4. 설정 파일은 관리 구간과 설치기가 관리하는 키만 바꾼다. 인증·세션·기억·로그·캐시는 저장소에 복사하지 않는다.
5. 파일 적용, 실행기의 발견(새 세션에서 스킬·지침·도구가 보이는지), 실제 작업 성공을 나눠 확인하고 보고한다. 빈 임시 홈에서 성공한 결과를 실제 설치 완료로 보고하지 않는다.
6. 저장소가 요구하는 Python 버전(3.12 이상)을 확인하고 같은 호환 인터프리터로 대상 실행기 검사와 루트 시험을 실행한다. 기본 명령은 `python3 scripts/check.py --executor <executor>`와 `python3 -m unittest discover -s tests -v`다. 커밋·푸시는 사용자가 요청한 범위에서 한다.

## 모델 라우팅 변경

- 검토표는 `현재 적용값 / 기본값 / 적용할 값` 순서로 제시하고 모든 분류의 모델 순서·추론 강도를 표시한다. 표 검토는 읽기 전용으로 진행하고 적용 지시를 받은 범위를 갱신한다.
- 각 실행기의 정책은 그 실행기의 원본과 현재 선택한 프로필에 적용한다. 다른 실행기의 프리셋과 설치본은 각각의 승인 범위로 관리하고, 실행기 간 동일성을 강제하는 시험은 실행기별 정책 보존 시험으로 조정한다.
- 작업별 모델 순서와 주·자식 fallback을 각각 관리하고, 승인된 정책의 최종 fallback과 작업별 순서·effort를 보존한다.
- 설정 적용과 실제 모델 호출을 별도로 보고한다. 작은 라우팅 수정은 원본·유효 체인·제공자 연결·대상 시험으로 검증하고, 실제 호출 확인을 요청받으면 최소 실행 증거를 추가한다.

### Hermes 런타임

- OMH 분류 체인은 `delegate_task` 자식에만 적용된다(`delegation.*` 키). 메인 대화·cron·칸반 작업자는 Hermes 기본 모델(세션 시작 시 고정)을 따른다. 작업별 모델은 칸반 `model_override`와 cron 작업 `model` 필드로 지정한다. 하위 에이전트 분류 기록은 `~/.omh/routing/route-provenance.json`에 있다. 사용량이 기대와 다르다는 질문에는 `$HERMES_HOME/state.db`의 `session_model_usage` 실제 호출 기록으로 답한다.
- `web.search_backend`가 비었거나 `openai-native`면 웹 검색은 openai-codex 메인 모델에서만 동작한다. 메인 모델을 다른 제공자로 바꿀 때는 키가 있는 검색 백엔드나 검색 중계 플러그인을 지정하고, 페이지 본문 읽기는 Aside로 한다.
- 갑작스러운 macOS 권한 팝업의 원인 프로세스 추적, `hermes update` 뒤 깨진 플러그인 복구(로컬 본체 수정 autostash), 칸반·cron 작업을 지시한 채팅 추적은 [런타임 이상 추적](references/runtime-diagnosis.md)을 따른다.
- 원본·호환 사본·문서 명령·회귀 시험을 함께 갱신하는 절차는 [모델 라우팅 원본 동기화](references/model-routing-maintenance.md), 실제 사용 모델·구독 사용량 감사와 기본 모델 전환은 [모델 사용량 감사](references/model-usage-audit.md)를 따른다.

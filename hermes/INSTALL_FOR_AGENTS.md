# Hermes 작업 환경 설치 (AI용)

[설치 공통 기준](../docs/install-common.md)을 따른다. 아래는 Hermes에 갖출 것과 완료 기준이다. 설치 방법은 AI가 각 공식 문서를 확인해 정한다. 설치 대상은 **Apple Silicon(M 시리즈) Mac**이다. 다른 컴퓨터면 지원 범위를 사용자에게 알리고 진행 여부를 묻는다.

## 갖출 것

| 항목 | 기준 | 참고 |
|---|---|---|
| Hermes | Desktop 또는 CLI 설치, 사용자가 GPT·Claude 계정 로그인. 인증 파일은 로컬에만 | [공식 설치 안내](https://hermes-agent.nousresearch.com/docs/getting-started/installation) |
| Desktop UI 크기 | 기존 ChatGPT·Claude 앱이 있으면 창·글자·UI 크기를 맞춤 | [UI 크기](docs/desktop-ui.md) |
| 스킬 | [스킬 표](../docs/skills.md)의 Hermes 열 (Hermes 공식 57개 + 공통 10개 + 외부 37개). 공식 스킬은 `manifest.json`의 고정 커밋 원본 그대로 | [설치 목록](INSTALL-LIST.md), `scripts/install_skills.py` |
| 외부 스킬 | Codex·Claude와 같은 Azure·마케팅 등 37개를 `$HERMES_HOME/skills/`에. 같은 설명 조정 적용 | `../codex/inventories/external-skills.json`, `../codex/scripts/install_external_skills.py --skills-dir`, `../codex/scripts/apply_skill_descriptions.py --skill-root` |
| OMH | `manifest.json`의 참조 커밋 기준으로 설치·setup, 연결한 GPT·Claude 제공자 반영 | [OMH 공식 안내](https://github.com/rlaope/oh-my-hermes/blob/4575d7fb64e2d931ee238a10c918a2e5e83f5b97/INSTALL_FOR_AGENTS.md) |
| 모델 라우팅 | Claude 넉넉형 (사용자가 원하면 GPT 넉넉형), 필요한 호환 패치 | [모델 라우팅](docs/model-routing.md) |
| 전역 규칙 | 선택한 프로필의 `SOUL.md`에 공통 작업 원칙·Aside·문서 전달 구간 | [전역 규칙](docs/global-rules.md), `scripts/install_global_rules.py` |
| 사용량 플러그인 | `PhoeniXAbhisheK/hermes-plugin-provider-usage` 고정 ref `753dfbd35c9ed8fec3127ce48e5521d986d3aabe`, GPT·Claude만 표시 | [사용량 표시](docs/provider-usage.md), `scripts/configure_provider_usage.py` |
| MCP | CodeGraph, GAM | 공통 기준 |
| 브라우저 | Aside 설치, 사용자가 고른 프로필 가져오기, Hermes에서 `repl` 직접 조작 | [브라우저](docs/browsers.md), [배포 규칙](templates/aside-browser.md) |

Hermes의 설치·호환 패치 스크립트는 미리보기가 기본이고 `--apply`로 적용한다. 기존 파일과 충돌하면 바꾸지 않고 알린다. 스킬이 쓰는 Python 라이브러리는 프로젝트 `.venv/`에 두고 Hermes 런타임에 임의로 설치하지 않는다.

## 진행 순서와 경로

1. Mac의 지원 범위, Hermes 설치 방식, 선택한 프로필의 실제 홈과 기존 설정을 확인한다. 이름 있는 프로필은 `~/.hermes/profiles/<이름>/`을 명시한다.
2. Hermes·OMH·사용량 플러그인을 고정 출처에 따라 준비한다. 필요한 계정 로그인과 OS 권한은 사용자에게 연결한다.
3. 아래 Hermes 명령은 Agent-setup의 `hermes/`를 작업 폴더로 실행한다. 선택한 실제 홈을 `--home`에 지정해 스킬과 세 전역 규칙 구간을 미리보기하고, 충돌을 해결한 뒤 같은 명령에 `--apply`를 붙인다.

   ```sh
   python3 scripts/install_skills.py --home <선택한-Hermes-홈>
   python3 scripts/install_global_rules.py --home <선택한-Hermes-홈>
   ```

   처음 미리보기의 공식 스킬 `source-needed`는 고정 원본 checkout 준비가 필요하다는 뜻이다. `install_skills.py --apply`는 해당 checkout을 준비한 뒤 전체 스킬의 충돌을 검사하고 복사한다. 공통 스킬 배포본은 루트 `shared/skills/`와 대조한다.
4. 외부 스킬 37개는 Agent-setup 루트의 `codex/scripts/install_external_skills.py`에 `--skills-dir <선택한-Hermes-홈>/skills`와 별도 `--state` 경로를 지정한다. `codex/scripts/apply_skill_descriptions.py`는 같은 스킬 홈을 `--skill-root`로 지정한다. 정확한 적용 옵션은 각 스크립트의 `--help`를 따른다.
5. [라우팅](docs/model-routing.md)과 [사용량 표시](docs/provider-usage.md)를 선택한 프로필에 적용하고 [브라우저](docs/browsers.md)·[UI 크기](docs/desktop-ui.md)를 준비한다. 각 문서의 `scripts/` 명령도 `hermes/` 기준이다. 루트 공통 검사 명령은 [검증 안내](docs/verification.md)를 따른다.

설치 결과에는 선택한 프로필, 적용 원본과 관리 구간, 충돌, 새 세션 검증 결과를 기록한다. 제품의 AGENTS·디자인·코드·lint·CI 설정은 해당 제품 저장소의 생성·적용 절차에서 관리한다.

## 보존과 완료 기준

선택한 프로필만 바꾼다. 다른 프로필, 설치 대상 외의 설정, 기존 브라우저 데이터, 사용자의 포커스·입력 대상·커서를 보존한다. 완료된 단계부터 이어간다.

새 Hermes 세션에서 확인하고 완료·실패·미확인으로 보고한다.

- Desktop 질문 응답, 연결한 제공자의 실제 자식 모델·provider·응답, 라우팅 문서의 fallback·추론 검증
- 전역 규칙 로딩과 문서 전달 시 실제 폴더 카드 제공·앱 미실행
- 사용량 조회·리셋 시간·새로고침과 상태바·툴팁·상세 패널·알림의 GPT·Claude 표시 제한
- CodeGraph·GAM MCP 도구 실제 응답
- 프로젝트별 Aside 프로필에서 `repl` 이동·입력·결과 읽기, 자체 AI 미호출과 포커스 보존
- 기준 앱이 있으면 창·글자·UI 크기 비교와 설정 유지 (재실행 확인 전에는 미확인)

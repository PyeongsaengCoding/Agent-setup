# Hermes 설치 원본

Agent-setup의 `hermes/`는 Apple Silicon macOS용 Hermes 설치 원본이다. 저장소 공통 기준은 루트 `AGENTS.md`, `README.md`, `docs/comparison.md`를 따른다.

- 사용자 문서는 짧은 한국어로 쓴다. 설치 목록은 `INSTALL-LIST.md` 한 표로 관리한다.
- 공개 문서의 경로는 `~`, `$HERMES_HOME`, 프로젝트 상대경로로 쓴다. 개인 계정 식별자·절대 홈 경로·인증·대화·브라우저 데이터를 Git 저장소에 넣지 않는다. 선택한 브라우저 프로필의 로컬 Aside 가져오기는 설치에 포함한다.
- 스킬, 프로젝트 지침, 플러그인, 외부 도구를 구별한다.
- Hermes 작업은 Hermes/OMH 설정을 따른다. 외부 Codex·Claude Code를 실행할 때만 해당 실행기의 모델 정책을 따른다.
- 기존 설치·프로필·스킬을 임의로 덮어쓰지 않는다. 로그인과 OS 권한은 사용자가 직접 승인한다.
- 공통 스킬과 공통 작업 규칙은 루트 `shared/skills/`, `shared/rules/`에서 고치고 Hermes 배포본을 맞춘다. Hermes 전용 라우팅·호환 패치·Aside·문서 전달은 이 폴더에서 관리한다.
- 설치 코드 변경 후 Agent-setup 루트에서 Python 3.12 이상으로 `python3 scripts/check.py --executor hermes`를 실행한다. Hermes 단위시험만 실행할 때는 `hermes/`에서 `python3 -m unittest discover -s tests -v`를 쓴다.

<!-- omh:agent-instructions:begin -->
## 문서와 응답의 표현

- 문서·지침·사용자 응답은 목적, 실제 동작, 적용 대상을 직접 설명한다. `~가 아니다`, `~이 아니라`, `~을 뜻하지 않는다` 같은 부정·대조 표현은 쓰지 않는다.
- 규칙에는 적용 대상, 조건, 수행할 행동을 구체적으로 쓴다. `최신 공통 기준`, `상시 관리`처럼 범위를 추측해야 하는 표현은 실제 문서·작업·주체를 밝혀 쓴다.
- 사용자가 요청하지 않은 상황이나 근거 없는 오해를 가정해 방어·면책 문구를 덧붙이지 않는다. 필요한 승인·보안·데이터 경계는 대상과 조건을 명시하고, 같은 뜻의 설명은 하나로 합친다.

<!-- omh:agent-instructions:end -->

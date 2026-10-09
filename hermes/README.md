# Hermes

macOS에서 Hermes Desktop, OMH, 사용량 플러그인, 스킬과 브라우저 작업 환경을 구성한다. 개인 계정·인증·대화·브라우저 데이터는 Git 저장소에 넣지 않는다. 사용자가 선택한 브라우저 프로필은 로컬 Aside로 가져온다.

설치 대상은 **Apple Silicon(M 시리즈, ARM64) Mac**이다.

## 설치 요청

Hermes가 아직 없으면 로컬 파일과 명령을 사용할 수 있는 AI에 다음 요청을 보낸다.

> https://github.com/PyeongsaengCoding/Agent-setup 을 받아 hermes/INSTALL_FOR_AGENTS.md에 따라 내 Mac에 Hermes 작업 환경을 구성해줘. Hermes Desktop·OMH·사용량 플러그인·스킬과 전역 규칙을 준비하고, GPT·Claude만 사용량에 표시해줘. 브라우저는 프로젝트별 Aside 프로필에서 Hermes가 repl로 직접 조작해줘. 내가 선택한 브라우저 프로필을 가져오고, 기존 ChatGPT·Claude 앱이 있으면 Hermes의 창·글자·UI 크기를 맞춰줘. 선택한 Hermes 프로필과 설치 대상에 적용하고 기존 데이터·포커스를 보존해줘. 필요한 선택·로그인·권한·충돌을 확인하고 설치 안내의 실제 동작 검증까지 맡아서 완료한 것과 남은 것을 알려줘.
>
> 모델 라우팅은 hermes/docs/model-routing.md에 따라 Claude 넉넉형(hermes/routing-presets/claude-generous.json)으로 적용해줘.

### 선택사항: GPT 넉넉형

GPT 넉넉형을 원하면 위 요청의 모델 라우팅 줄만 다음으로 바꾼다.

> 모델 라우팅은 hermes/docs/model-routing.md에 따라 GPT(코덱스) 넉넉형(hermes/routing-presets/gpt-generous.json)으로 적용해줘.

이미 설치했다면 [모델 안내](docs/model-routing.md)의 요청으로 라우팅만 전환할 수 있다.

위 요청은 AI 채팅에 보낸다. 이 저장소의 도구는 스킬·전역 규칙·호환 패치를 준비하며, 로그인과 OS 권한은 사용자가 승인한다.

## 문서

- [설치 목록](INSTALL-LIST.md): 플러그인·스킬·추가 도구와 설치 경로를 한 표로 정리
- [설치](INSTALL_FOR_AGENTS.md): Hermes 없는 상태부터 시작
- [모델 라우팅](docs/model-routing.md): Claude 넉넉형 / GPT(코덱스) 넉넉형, 버전별 AI 요청문·CLI 전환 명령
- [전역 규칙](docs/global-rules.md): 공통 작업 원칙, Aside 직접 조작과 문서 전달 시 폴더 카드 제공·앱 자동 실행 금지를 선택한 프로필의 SOUL.md에 중복 없이 적용
- [Desktop UI 크기](docs/desktop-ui.md): 기존 ChatGPT·Claude 앱 기준으로 창·글자·UI 배율 맞춤
- [사용량 표시 제한](docs/provider-usage.md): GPT·Claude만 상태바·패널·알림에 표시
- [브라우저](docs/browsers.md): Aside·Chrome·Edge·Safari 연결과 프로필 가져오기
- [검증 상태](docs/verification.md): 확인한 결과와 남은 검사

스킬은 작업 방법을 가르치는 문서와 보조 파일이다. `AGENTS.md`는 프로젝트 규칙이다. 플러그인은 특정 프로그램의 확장이다. 여기의 `provider-usage`는 Hermes용이므로 Codex나 Claude Code에 그대로 설치하지 않는다. 외부 CLI·MCP는 지원하는 다른 프로그램에서도 사용할 수 있다.

필수 스킬의 설치·사용 기준은 [설치 목록](INSTALL-LIST.md)과 [설치 안내](INSTALL_FOR_AGENTS.md)를 따른다.

## 원본의 경계

Hermes 전용 원본은 `routing-presets/`, `scripts/`, Aside·문서 전달 템플릿이다. 공통 스킬은 Agent-setup 루트 `shared/skills/`, 공통 전역 규칙은 `shared/rules/`에서 관리한다. 이 폴더의 `skills/`와 `templates/common-rules.md`는 Hermes 설치용 배포본이다. 프로젝트 생성과 제품 기준 적용은 [pycoding-prompt](https://github.com/PyeongsaengCoding/pycoding-prompt), 실제 제품 규칙·코드·검사 설정은 해당 제품 저장소에서 관리한다.

## 유지관리

사용 중인 설정은 `${HERMES_HOME:-~/.hermes}`에 있다. 이 저장소를 지워도 설치한 스킬은 남는다. 스킬 재설치는 같은 파일을 건너뛰고, 다른 기존 파일은 충돌로 보고한다. 업데이트는 설치 시점의 공식 문서와 계정에서 제공하는 모델을 다시 확인한다.

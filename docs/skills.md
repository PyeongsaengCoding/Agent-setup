# AI별 스킬 표

✅ 기본 설치 · ◻️ 요청 시 설치 · — 설치 안 함. **둘 곳**: `Agent-setup`은 AI 작업 도구로 전역 설치, `pycoding-prompt`는 프로젝트 기준, `둘 다`는 도구는 Agent-setup·적용 기준은 pycoding-prompt.

| AI | 기본 설치 | 구성 |
|---|---|---|
| Claude Code | 64 | 공통 26 + codex + 외부 37 |
| Codex | 63 | 공통 26 + 외부 37 |
| Hermes | 104 + OMH 142 | Hermes 공식 57 + 공통 10 + 외부 37 + OMH 142 |

## 1. 공통 스킬과 AI 전용 스킬 (28)

| # | 구분 | 스킬 | 하는 일 | Claude | Codex | Hermes | 세 AI 비교 | 둘 곳 | pycoding-prompt 관계 |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 계획 | coding-plan | 복합 작업의 범위·완료 조건·검증 방법 정하기 | ✅ | ✅ | — | 같은 파일. Hermes는 OMH plan·ulw-plan이 같은 일 | Agent-setup | — |
| 2 | 분담 | coding-work | 팀장으로서 담당·모델·파일 소유권 배정, 결과 통합 | ✅ | ✅ | — | 같은 파일. 위임 방법은 전역 지침이 AI별로 다름 (Claude: route 에이전트·Codex 플러그인 / Codex: 네이티브 위임). Hermes는 OMH 라우팅 | Agent-setup | — |
| 3 | 분담 | coding-handoff | 다른 담당에게 넘길 맥락 구성, 중단 작업 재개 | ✅ | ✅ | — | 같은 파일. Hermes는 OMH ulw-maestro | Agent-setup | — |
| 4 | 분담 | coding-status | 여러 작업의 상태·검증 결과 요약 | ✅ | ✅ | — | 같은 파일. Hermes는 OMH agent-ops-review | Agent-setup | — |
| 5 | 조사 | coding-research | 외부 사양·라이브러리 근거 조사 | ✅ | ✅ | — | 같은 파일. Hermes는 OMH web-research | Agent-setup | — |
| 6 | 조사 | codegraph-context | CodeGraph로 코드 위치·호출 관계·영향 좁히기 | ✅ | ✅ | ✅ | 세 AI 같은 파일, 같은 CodeGraph MCP | Agent-setup | — |
| 7 | 구현 | ponytail | 기존 코드·기능으로 가장 단순하게 구현 | ✅ | ✅ | — | 같은 파일. Hermes는 simplify-code·OMH | Agent-setup | — |
| 8 | 구현 | tdd | 실패 테스트부터 작성 | ✅ | ✅ | — | 같은 파일. Hermes는 공식 test-driven-development | Agent-setup | — |
| 9 | 구현 | diagnosing-bugs | 작은 재현 → 가설 → 수정으로 원인 불명 버그 진단 | ✅ | ✅ | — | 같은 파일. Hermes는 공식 systematic-debugging | Agent-setup | — |
| 10 | 구현 | coding-repair | 실패한 검증 수정, 중단된 구현 이어가기 | ✅ | ✅ | — | 같은 파일. Hermes는 OMH build-failure-triage | Agent-setup | — |
| 11 | 검토 | coding-code-review | 변경 코드의 재현 가능한 결함 찾기 | ✅ | ✅ | — | 같은 파일. 다른 모델 리뷰는 Claude가 /codex:review, Codex는 다른 GPT 담당. Hermes는 OMH code-review | Agent-setup | — |
| 12 | 검토 | coding-verification | 요구사항별 실제 검증 증거로 완료 판단 | ✅ | ✅ | — | 같은 파일. Hermes는 OMH verification-gate | Agent-setup | — |
| 13 | 검토 | coding-design-review | 권한·데이터·시스템 경계 설계의 반례 검토 | ✅ | ✅ | — | 같은 파일. Hermes는 OMH adversarial-consensus | Agent-setup | — |
| 14 | 검토 | coding-failure-audit | 실패를 정상처럼 처리하는 코드 조사 | ✅ | ✅ | — | 같은 파일. Hermes는 OMH failure-signal-audit | Agent-setup | — |
| 15 | 검토 | coding-debt-audit | 유지보수 문제를 근거·영향·노력으로 정리 | ✅ | ✅ | — | 같은 파일. Hermes는 OMH tech-debt-audit | Agent-setup | — |
| 16 | 화면 | product-design-review | OMH frontend·visual-qa의 디자인 시스템·상태·렌더 검증을 Claude Code·Codex에서 직접 수행 | ✅ | ✅ | — | 같은 파일. Hermes는 OMH frontend·visual-qa 원본 | 둘 다 | 제품별 기준은 pycoding-prompt `project_setup_design.md`; 레퍼런스 선택은 사용자 요청이나 동의에 따라 적용 |
| 17 | 화면 | coding-ai-slop-review | 제품 화면 문구의 중복·빈 안내·내부 용어 검토 | ✅ | ✅ | — | 같은 파일. Hermes는 OMH ai-slop-cleaner | 둘 다 | 적용 기준(anti-slop 검사를 lint·CI에)은 pycoding project_setup_docs.md. 스킬은 검토 도구 |
| 18 | 글쓰기 | humanize-korean | 한국어 번역투·상투 표현 교정 | ✅ | ✅ | ✅ | 세 AI 같은 파일 | 둘 다 | 적용 기준(humanize-korean)은 pycoding project_setup_docs.md. 설치는 Agent-setup이 하므로 pycoding의 "프로젝트마다 스킬 준비"는 확인만 하면 됨 |
| 19 | 글쓰기 | humanizer | 영문 AI 투 표현 교정 (blader/humanizer v3.1.0) | ✅ | ✅ | ✅ | 세 AI 같은 파일 (v3.1.0) | 둘 다 | 적용 기준(no-ai-slop 영문)은 pycoding project_setup_docs.md. 설치는 Agent-setup |
| 20 | 화면 | shadcn | shadcn/ui 컴포넌트 추가·검색·구성·스타일 (shadcn 공식 스킬) | ✅ | ✅ | ✅ | 세 AI 같은 파일 (공식 원본) | 둘 다 | shadcn/ui를 쓸지·테마 순서는 pycoding project_setup_design.md·tech_stack.md. 스킬 설치는 Agent-setup (pycoding은 "준비·로드 확인"만) |
| 21 | 화면 | shadcn-lint | @shadcn/lint 설치·등록과 프로젝트가 선택한 규칙 적용 | ✅ | ✅ | ✅ | 세 AI 같은 파일 (SETUP.md 기반) | 둘 다 | Agent-setup은 에이전트용 설치·설정 절차를 제공한다. 제품의 규칙·토큰·lint·CI는 pycoding-prompt 기준과 해당 프로젝트에서 결정·검증한다 |
| 22 | 글쓰기 | writing-for-agents | AGENTS.md·스킬 문서 작성법 | ✅ | ✅ | — | 같은 파일. Hermes는 OMH agent-instructions | Agent-setup | 프로젝트 AGENTS.md 내용은 pycoding 템플릿, 작성 방법은 이 스킬 |
| 23 | 도구 | aside-browser | Aside를 `repl`로 직접 조작 | ✅ | ✅ | ✅ | 세 AI 같은 파일. Hermes는 SOUL.md Aside 규칙도 있음 | Agent-setup | 프로젝트별 Aside 프로필은 프로젝트 AGENTS.md에 적음 |
| 24 | 기억 | gam-memory | GAM으로 과거 결정 회수, 승인한 지식 저장 | ✅ | ✅ | ✅ | 세 AI 같은 파일, 같은 GAM 기억 | Agent-setup | — |
| 25 | 기억 | coding-maintenance | 기억·기록 보존 정책과 승인된 정리 | ✅ | ✅ | ✅ | 세 AI 같은 파일 | Agent-setup | — |
| 26 | 환경 | agent-setup-maintenance | 이 작업 환경(지침·스킬·도구) 변경 절차 | ✅ | ✅ | ✅ | 세 AI 같은 파일 | Agent-setup | — |
| 27 | 선택 | desktop-app-provisioning | 앱 설치, 브라우저 프로필 가져오기 | ◻️ | ◻️ | ✅ | 같은 파일. Claude·Codex는 요청 시, Hermes는 기본 | Agent-setup | — |
| 28 | Claude 전용 | codex | GPT 항목을 Codex 플러그인으로 넘기고 결과 회수 | ✅ | — | — | Claude 전용 (Codex 플러그인) | Agent-setup | — |

## 2. 외부 스킬 (37)

업무별 외부 원본에서 받는다. 세 AI 모두 같은 원본·같은 설명 조정. 세 AI 비교: 파일이 같고 설치 위치만 다름 (`~/.claude/skills`, `~/.agents/skills`, `$HERMES_HOME/skills`).

| # | 스킬 | 하는 일 | Claude | Codex | Hermes | 둘 곳 | pycoding-prompt 관계 |
|---|---|---|---|---|---|---|---|
| 1 | microsoft-foundry | Foundry 모델·에이전트의 구축·운영 | ✅ | ✅ | ✅ | Agent-setup | — |
| 2 | airunway-aks-setup | AI Runway의 AKS 모델 서빙 준비 | ✅ | ✅ | ✅ | Agent-setup | — |
| 3 | appinsights-instrumentation | Application Insights 계측 구성 | ✅ | ✅ | ✅ | Agent-setup | — |
| 4 | azure-ai | Azure AI Search·Speech·OpenAI·문서 처리 | ✅ | ✅ | ✅ | Agent-setup | — |
| 5 | azure-aigateway | AI 서비스용 API Management 게이트웨이 | ✅ | ✅ | ✅ | Agent-setup | — |
| 6 | azure-cloud-migrate | 다른 클라우드에서 Azure로 이전 | ✅ | ✅ | ✅ | Agent-setup | — |
| 7 | azure-compliance | Azure 보안·준수 상태 점검 | ✅ | ✅ | ✅ | Agent-setup | — |
| 8 | azure-compute | Azure VM·VMSS 용량과 운영 | ✅ | ✅ | ✅ | Agent-setup | — |
| 9 | azure-deploy | 준비된 Azure 배포 실행 | ✅ | ✅ | ✅ | Agent-setup | 배포 권한·대상은 프로젝트 AGENTS.md |
| 10 | azure-diagnostics | Azure 장애·로그 진단 | ✅ | ✅ | ✅ | Agent-setup | — |
| 11 | azure-enterprise-infra-planner | 기업 Azure 인프라 설계·구성 | ✅ | ✅ | ✅ | Agent-setup | — |
| 12 | azure-kubernetes | AKS 클러스터 구축·운영 | ✅ | ✅ | ✅ | Agent-setup | — |
| 13 | azure-kusto | Azure 로그·시계열 KQL 분석 | ✅ | ✅ | ✅ | Agent-setup | — |
| 14 | azure-messaging | Event Hubs·Service Bus 문제 해결 | ✅ | ✅ | ✅ | Agent-setup | — |
| 15 | azure-prepare | 요청된 azd 배포 파일 준비 | ✅ | ✅ | ✅ | Agent-setup | 만드는 `azure.yaml`·`.azure/` 배포 파일은 프로젝트 결과물. 배포 권한은 프로젝트 AGENTS.md |
| 16 | azure-quotas | Azure 할당량·지역별 용량 확인 | ✅ | ✅ | ✅ | Agent-setup | — |
| 17 | azure-rbac | Azure 역할·조건·권한 설계 근거 확인 | ✅ | ✅ | ✅ | Agent-setup | — |
| 18 | azure-reliability | Azure App Service·Functions 복원력 점검 | ✅ | ✅ | ✅ | Agent-setup | — |
| 19 | azure-resource-lookup | 구독 전체 Azure 리소스 조회 | ✅ | ✅ | ✅ | Agent-setup | — |
| 20 | azure-resource-visualizer | Azure 리소스 관계 도식화 | ✅ | ✅ | ✅ | Agent-setup | — |
| 21 | azure-storage | Blob·Files·Queues·Tables·Data Lake 작업 | ✅ | ✅ | ✅ | Agent-setup | — |
| 22 | azure-upgrade | Azure 요금제·서비스·SDK 업그레이드 | ✅ | ✅ | ✅ | Agent-setup | — |
| 23 | azure-validate | Azure 배포 전 설정·권한 점검 | ✅ | ✅ | ✅ | Agent-setup | — |
| 24 | entra-agent-id | Entra 에이전트 ID·토큰 교환 구성 | ✅ | ✅ | ✅ | Agent-setup | — |
| 25 | entra-app-registration | Entra 앱 등록·OAuth·MSAL 구성 | ✅ | ✅ | ✅ | Agent-setup | — |
| 26 | python-appservice-deploy | Python 앱을 Azure App Service에 배포 | ✅ | ✅ | ✅ | Agent-setup | 배포 권한·대상은 프로젝트 AGENTS.md |
| 27 | copywriting | 마케팅 페이지·캠페인 문구 작성 | ✅ | ✅ | ✅ | Agent-setup | 스킬이 읽는 제품 맥락 파일(`.claude/product-marketing.md`)은 프로젝트에 둠 |
| 28 | seo-audit | 웹 검색 노출·기술 SEO 점검 | ✅ | ✅ | ✅ | 둘 다 | 검색 노출 기준은 pycoding project_setup_seo.md. 스킬은 점검 도구 |
| 29 | aso | 앱 스토어 검색·전환 점검 | ✅ | ✅ | ✅ | 둘 다 | 스토어 노출·현지화 기준은 pycoding project_setup_aso.md. 스킬은 점검 도구 |
| 30 | analytics | 제품·마케팅 이벤트 계측 | ✅ | ✅ | ✅ | 둘 다 | 계측 기준(이벤트 이름·개인정보)은 pycoding project_setup_analytics.md |
| 31 | cro | 랜딩·폼 전환 개선 검토 | ✅ | ✅ | ✅ | Agent-setup | 스킬이 읽는 제품 맥락 파일은 프로젝트에 둠 |
| 32 | archify | 공유할 HTML 구조·흐름 다이어그램 | ✅ | ✅ | ✅ | Agent-setup | — |
| 33 | iterative-retrieval | 이미 배정한 하위 작업의 부족한 맥락 보완 | ✅ | ✅ | ✅ | Agent-setup | — |
| 34 | cost-analysis | 실제 Azure 비용·청구 변화 분석 | ✅ | ✅ | ✅ | Agent-setup | — |
| 35 | cost-estimation | 계획 중인 Azure 사용료 추정 | ✅ | ✅ | ✅ | Agent-setup | — |
| 36 | cost-governance | Azure 예산·알림·정책 관리 | ✅ | ✅ | ✅ | Agent-setup | — |
| 37 | cost-optimization | 실행 중인 Azure 리소스 비용 최적화 | ✅ | ✅ | ✅ | Agent-setup | — |

## 3. Hermes 공식 스킬 (57)

Hermes 원본 고정 커밋에서 받는다. Hermes 도구 기준으로 쓰여 Hermes에만 설치한다.

| # | 분류 | 스킬 | 하는 일 | Claude | Codex | Hermes | Claude·Codex에 안 넣는 이유 | 둘 곳 | pycoding-prompt 관계 |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Apple | apple-notes | Apple 메모 읽기·검색·작성 | — | — | ✅ | Hermes 도구·경로를 고쳐야 쓸 수 있음 | Agent-setup (Hermes) | — |
| 2 | Apple | apple-reminders | Apple 미리 알림 관리 | — | — | ✅ | 선택 묶음 후보 (요청 시 설치 가능) | Agent-setup (Hermes) | — |
| 3 | Apple | findmy | 나의 찾기 기기·AirTag 확인 | — | — | ✅ | 작업 환경 기본에 불필요 | Agent-setup (Hermes) | — |
| 4 | Apple | imessage | iMessage·SMS 조회·전송 | — | — | ✅ | 선택 묶음 후보 (요청 시 설치 가능) | Agent-setup (Hermes) | — |
| 5 | 다른 AI·화면 | claude-code | 외부 Claude Code에 코딩 위임 | — | — | ✅ | 다른 AI를 CLI로 부르는 Hermes용 (Claude는 Codex 플러그인, Codex는 GPT 전용) | Agent-setup (Hermes) | — |
| 6 | 다른 AI·화면 | codex | 외부 Codex CLI에 코딩 위임 | — | — | ✅ | 다른 AI를 CLI로 부르는 Hermes용 (Claude는 Codex 플러그인, Codex는 GPT 전용) | Agent-setup (Hermes) | — |
| 7 | 다른 AI·화면 | computer-use | 네이티브 앱 화면·입력 제어 | — | — | ✅ | Hermes 전용 기능에 묶임 | Agent-setup (Hermes) | — |
| 8 | 다른 AI·화면 | hermes-agent | Hermes 사용·설정·문제 해결 | — | — | ✅ | Hermes 전용 기능에 묶임 | Agent-setup (Hermes) | — |
| 9 | 다른 AI·화면 | opencode | 외부 OpenCode에 코딩 위임 | — | — | ✅ | 라우팅에 OpenCode를 쓰지 않음 | Agent-setup (Hermes) | — |
| 10 | 창작 | architecture-diagram | 아키텍처 다이어그램 작성 | — | — | ✅ | 선택 묶음 후보 (요청 시 설치 가능) | Agent-setup (Hermes) | — |
| 11 | 창작 | ascii-video | 영상·오디오를 ASCII 영상으로 변환 | — | — | ✅ | 선택 묶음 후보 (요청 시 설치 가능) | Agent-setup (Hermes) | — |
| 12 | 창작 | baoyu-infographic | 정보를 인포그래픽으로 구성 | — | — | ✅ | Hermes 도구·경로를 고쳐야 쓸 수 있음 | Agent-setup (Hermes) | — |
| 13 | 창작 | claude-design | 일회성 HTML 화면·발표·프로토타입 | — | — | ✅ | 선택 묶음 후보 (요청 시 설치 가능) | Agent-setup | 정식 제품 화면 기준은 pycoding project_setup_design.md |
| 14 | 창작 | design-md | DESIGN.md 디자인 토큰 작성·검사 | — | — | ✅ | 선택 묶음 후보 (요청 시 설치 가능) | 둘 다 | DESIGN.md를 둘지·내용 기준은 pycoding project_setup_design.md |
| 15 | 창작 | manim-video | Manim 수학·알고리즘 영상 | — | — | ✅ | 선택 묶음 후보 (요청 시 설치 가능) | Agent-setup (Hermes) | — |
| 16 | 창작 | p5js | p5.js 생성형 그래픽·인터랙션 | — | — | ✅ | 선택 묶음 후보 (요청 시 설치 가능) | Agent-setup (Hermes) | — |
| 17 | 창작 | popular-web-designs | 실제 디자인 시스템 참고 화면 | — | — | ✅ | Hermes 도구·경로를 고쳐야 쓸 수 있음 | 둘 다 | 레퍼런스 사이트 목록·선택 기준은 pycoding project_setup_design.md와 겹침 |
| 18 | 창작 | songwriting-and-ai-music | 작사·작곡 방향·음악 생성 요청 | — | — | ✅ | 작업 환경 기본에 불필요 | Agent-setup (Hermes) | — |
| 19 | 개발 운영 | sdlc-review | Kanban 작업 결과 검토 | — | — | ✅ | Hermes Kanban 전용 (리뷰는 coding-code-review) | Agent-setup (Hermes) | — |
| 20 | 메일 | email-inbox-triage | 메일 우선순위·답장 초안 | — | — | ✅ | 선택 묶음 후보 (요청 시 설치 가능) | Agent-setup (Hermes) | — |
| 21 | 메일 | himalaya | IMAP·SMTP 메일 CLI 작업 | — | — | ✅ | 선택 묶음 후보 (요청 시 설치 가능) | Agent-setup (Hermes) | — |
| 22 | 미디어 | gif-search | Tenor GIF 검색·다운로드 | — | — | ✅ | 작업 환경 기본에 불필요 | Agent-setup (Hermes) | — |
| 23 | 미디어 | songsee | 오디오 스펙트럼 분석 | — | — | ✅ | 작업 환경 기본에 불필요 | Agent-setup (Hermes) | — |
| 24 | 미디어 | youtube-content | YouTube 자막을 요약·콘텐츠로 변환 | — | — | ✅ | Hermes 도구·경로를 고쳐야 쓸 수 있음 | Agent-setup (Hermes) | — |
| 25 | 노트 | obsidian | Obsidian vault 노트 작업 | — | — | ✅ | 선택 묶음 후보 (요청 시 설치 가능) | Agent-setup (Hermes) | — |
| 26 | 업무 | airtable | Airtable 레코드 조회·수정 | — | — | ✅ | 선택 묶음 후보 (요청 시 설치 가능) | Agent-setup (Hermes) | — |
| 27 | 업무 | box | Box 파일·권한·메타데이터 관리 | — | — | ✅ | 선택 묶음 후보 (요청 시 설치 가능) | Agent-setup (Hermes) | — |
| 28 | 업무 | document-to-action-items | 문서에서 의무·기한·할 일 추출 | — | — | ✅ | 선택 묶음 후보 (요청 시 설치 가능) | Agent-setup | — |
| 29 | 업무 | docx | Word 문서 작성·편집 | — | — | ✅ | 선택 묶음 후보 (요청 시 설치 가능) | Agent-setup | 보고서 문체는 pycoding project_setup_docs.md |
| 30 | 업무 | google-workspace | Gmail·Calendar·Drive·Docs·Sheets | — | — | ✅ | Hermes 도구·경로를 고쳐야 쓸 수 있음 | Agent-setup (Hermes) | — |
| 31 | 업무 | maps | 위치·경로·시간대 조회 | — | — | ✅ | 선택 묶음 후보 (요청 시 설치 가능) | Agent-setup (Hermes) | — |
| 32 | 업무 | meeting-action-items | 회의에서 결정·담당·할 일 추출 | — | — | ✅ | 선택 묶음 후보 (요청 시 설치 가능) | Agent-setup (Hermes) | — |
| 33 | 업무 | notion | Notion 페이지·DB 작업 | — | — | ✅ | 선택 묶음 후보 (요청 시 설치 가능) | Agent-setup (Hermes) | — |
| 34 | 업무 | pdf | PDF 읽기·작성·병합·OCR | — | — | ✅ | 선택 묶음 후보 (요청 시 설치 가능) | Agent-setup (Hermes) | — |
| 35 | 업무 | powerpoint | PowerPoint 작성·편집·렌더링 | — | — | ✅ | 선택 묶음 후보 (요청 시 설치 가능) | Agent-setup (Hermes) | — |
| 36 | 업무 | product-price-monitor | 상품·항공권·매물 가격 감시 | — | — | ✅ | Hermes 도구·경로를 고쳐야 쓸 수 있음 | Agent-setup (Hermes) | — |
| 37 | 업무 | teams-meeting-pipeline | Teams 회의 자막·요약 파이프라인 | — | — | ✅ | Hermes 전용 기능에 묶임 | Agent-setup (Hermes) | — |
| 38 | 업무 | weekly-review-planning | 주간 회고·다음 주 계획 | — | — | ✅ | 선택 묶음 후보 (요청 시 설치 가능) | Agent-setup (Hermes) | — |
| 39 | 업무 | xlsx | Excel·CSV 작성·분석 | — | — | ✅ | 선택 묶음 후보 (요청 시 설치 가능) | Agent-setup (Hermes) | — |
| 40 | 조사 | arxiv | arXiv 논문 검색·조회 | — | — | ✅ | 선택 묶음 후보 (요청 시 설치 가능) | Agent-setup (Hermes) | — |
| 41 | 조사 | competitor-news-monitor | 경쟁사 뉴스 감시·근거 정리 | — | — | ✅ | Hermes 도구·경로를 고쳐야 쓸 수 있음 | Agent-setup (Hermes) | — |
| 42 | 조사 | grounded-citations | 검증 가능한 인용·출처 관리 | — | — | ✅ | Hermes 도구·경로를 고쳐야 쓸 수 있음 | Agent-setup (Hermes) | — |
| 43 | 조사 | llm-wiki | Markdown 지식 위키 구축 | — | — | ✅ | 선택 묶음 후보 (요청 시 설치 가능) | Agent-setup (Hermes) | — |
| 44 | 소셜 | xurl | X 검색·게시·메시지 CLI | — | — | ✅ | 선택 묶음 후보 (요청 시 설치 가능) | Agent-setup (Hermes) | — |
| 45 | 개발 | codebase-inspection | 언어·코드량·구성 조사 | — | — | ✅ | 작업 환경 기본에 불필요 | Agent-setup (Hermes) | — |
| 46 | 개발 | dogfood | 웹 앱 탐색 QA·오류 증거 | — | — | ✅ | Hermes 도구·경로를 고쳐야 쓸 수 있음 | Agent-setup (Hermes) | — |
| 47 | 개발 | github | GitHub 저장소·PR·이슈 작업 | — | — | ✅ | Hermes 도구·경로를 고쳐야 쓸 수 있음 | Agent-setup (Hermes) | — |
| 48 | 개발 | hermes-agent-skill-authoring | Hermes 스킬 작성·검증 | — | — | ✅ | Hermes 전용 기능에 묶임 | Agent-setup (Hermes) | — |
| 49 | 개발 | inspecting-hermes-desktop-dom | Hermes Desktop DOM·CSS 검사 | — | — | ✅ | Hermes 전용 기능에 묶임 | Agent-setup (Hermes) | — |
| 50 | 개발 | node-inspect-debugger | Node.js 디버깅 | — | — | ✅ | Hermes 도구·경로를 고쳐야 쓸 수 있음 | Agent-setup (Hermes) | — |
| 51 | 개발 | python-debugpy | Python pdb·debugpy 디버깅 | — | — | ✅ | Hermes 도구·경로를 고쳐야 쓸 수 있음 | Agent-setup (Hermes) | — |
| 52 | 개발 | requesting-code-review | 변경 검토·품질 검사 | — | — | ✅ | 공통 스킬 coding-code-review와 같은 역할 | Agent-setup (Hermes) | — |
| 53 | 개발 | simplify-code | 최근 코드 변경 정리 | — | — | ✅ | 선택 묶음 후보 (요청 시 설치 가능) | Agent-setup (Hermes) | — |
| 54 | 개발 | spike | 짧은 실험으로 가정 검증 | — | — | ✅ | 선택 묶음 후보 (요청 시 설치 가능) | Agent-setup (Hermes) | — |
| 55 | 개발 | systematic-debugging | 재현·원인 확인 후 수정 | — | — | ✅ | 공통 스킬 diagnosing-bugs와 같은 역할 | Agent-setup (Hermes) | — |
| 56 | 개발 | test-driven-development | 실패 테스트부터 구현 | — | — | ✅ | 공통 스킬 tdd와 같은 역할 | Agent-setup (Hermes) | — |
| 57 | 웹 | blocked-page-recovery | 차단·로그인 벽 페이지 접근 복구 | — | — | ✅ | Hermes 도구·경로를 고쳐야 쓸 수 있음 | Agent-setup (Hermes) | — |

## 4. OMH 스킬 (142)

OMH 설치기가 관리하는 Hermes 전용 스킬. 같은 작업 원칙은 Claude·Codex에서 1절 공통 스킬이 맡는다. 둘 곳은 모두 Agent-setup(Hermes·OMH)이고, 아래 "pycoding-prompt 관계"가 있는 18개는 프로젝트 기준과 겹치므로 프로젝트에서는 pycoding-prompt 기준을 우선한다.

| # | 역할 폴더 | 스킬 | 하는 일 | Claude | Codex | Hermes | pycoding-prompt 관계 |
|---|---|---|---|---|---|---|---|
| 1 | guide | omh-apps | 앱 연동 작업 카드·전송 전 확인 | — | — | ✅ | — |
| 2 | guide | omh-browser | 브라우저 작업 범위·권한 통제 | — | — | ✅ | — |
| 3 | guide | omh-content-operator | 게시용 콘텐츠 작성·검토 관리 | — | — | ✅ | — |
| 4 | guide | omh-data-analysis | 제공 데이터 분석·근거 기반 보고 | — | — | ✅ | — |
| 5 | guide | omh-external-connector-readiness | 외부 커넥터 도입 준비도 평가 | — | — | ✅ | — |
| 6 | guide | omh-files | 로컬 파일 작업 범위·확인 통제 | — | — | ✅ | — |
| 7 | guide | omh-gateway-intent-card | 메신저 게이트웨이 세션 정규화 | — | — | ✅ | — |
| 8 | guide | omh-jev-ask | Jev 판정 서비스 질의·결과 보고 | — | — | ✅ | — |
| 9 | guide | omh-jev-route | 라우팅 미결정 시 Jev 추천 활용 | — | — | ✅ | — |
| 10 | guide | omh-live-info | 실시간 정보 조회·출처 명시 | — | — | ✅ | — |
| 11 | guide | omh-media-input | 전사·OCR 등 미디어 텍스트 추출 | — | — | ✅ | — |
| 12 | guide | omh-meta-router | /omh 명령 워크플로 선택·연결 | — | — | ✅ | — |
| 13 | guide | omh-model-setup | Hermes 모델 설정 진단·구성 | — | — | ✅ | — |
| 14 | guide | omh-morning-brief | 모닝 브리프용 메일·캘린더 설정 | — | — | ✅ | — |
| 15 | guide | omh-parallel-tools | 병렬 도구 호출 지원 점검 | — | — | ✅ | — |
| 16 | guide | omh-prompt-import-readiness | 외부 에이전트 프롬프트 이식성 점검 | — | — | ✅ | — |
| 17 | guide | omh-routing | OMH 요청 라우팅·우선순위 규칙 | — | — | ✅ | — |
| 18 | guide | omh-terminal | 셸 명령 안전 등급·실행 통제 | — | — | ✅ | — |
| 19 | guide | omh-voice-input | 음성 요청 해석·단일 행동 변환 | — | — | ✅ | — |
| 20 | guide | omh-websearch-setup | Hermes 웹 검색 진단·설정 | — | — | ✅ | — |
| 21 | handoff-guide | omh-ai-slop-cleaner | 동작 보존 코드 정리·군더더기 제거 | — | — | ✅ | — |
| 22 | handoff-guide | omh-executor-runtime-readiness | 코딩 실행 런타임 준비 점검 | — | — | ✅ | — |
| 23 | handoff-guide | omh-frontend-refactor | 동작 고정 UI 리팩터링 | — | — | ✅ | — |
| 24 | memory-keeper | omh-decision-recall | 기각된 결정 기억 조회 | — | — | ✅ | — |
| 25 | memory-keeper | omh-memory-new | 신규 프로젝트 사실 기억 평가 | — | — | ✅ | — |
| 26 | memory-keeper | omh-memory-sync | Hermes 메모리 파일 검토·정리 | — | — | ✅ | — |
| 27 | memory-keeper | omh-rules-distill | 반복 교훈의 규칙 후보화 | — | — | ✅ | — |
| 28 | memory-keeper | omh-wiki | 대상 독자별 위키 설계 | — | — | ✅ | — |
| 29 | operator | omh-agent-debug | 멈춘 에이전트 실행 진단 | — | — | ✅ | — |
| 30 | operator | omh-agent-evaluation | 공정한 에이전트 비교 평가 설계 | — | — | ✅ | — |
| 31 | operator | omh-apple-design | 애플 플랫폼 디자인 방향·검토 | — | — | ✅ | Apple 화면 기준은 pycoding project_setup_design.md |
| 32 | operator | omh-automation-blueprint | 반복 요청 자동화 일정 설계 | — | — | ✅ | — |
| 33 | operator | omh-award-bar-score | 웹 디자인 어워드 기준 채점 | — | — | ✅ | 디자인 레퍼런스 기준은 pycoding project_setup_design.md |
| 34 | operator | omh-cto-loop | CTO 관점 운영 판단 루프 | — | — | ✅ | — |
| 35 | operator | omh-decide | 의사결정 브리프 작성 | — | — | ✅ | 결정 기록(ADR) 위치·형식은 pycoding project_setup_docs.md 문서 구조 |
| 36 | operator | omh-deliverable-package | 첨부 산출물 상태 추적 | — | — | ✅ | 산출물·보고 위치는 pycoding project_setup_docs.md |
| 37 | operator | omh-deploy-and-monitor | 배포·모니터링·롤백 체크리스트 | — | — | ✅ | 배포 권한·절차는 프로젝트 AGENTS.md (pycoding 템플릿) |
| 38 | operator | omh-design-orchestration | 디자인 방향·하위 레인 연계 | — | — | ✅ | 디자인 방향 결정은 pycoding project_setup_design.md |
| 39 | operator | omh-design-quality-gate | 고품질 디자인 기준·렌더 검증 | — | — | ✅ | 화면 품질 기준은 pycoding project_setup_design.md |
| 40 | operator | omh-feedback-triage | 고객 피드백 분류·우선순위화 | — | — | ✅ | — |
| 41 | operator | omh-finance-analysis | 재무 데이터 차이·현금 위험 분석 | — | — | ✅ | — |
| 42 | operator | omh-frontend | 디자인 시스템·화면 상태 기준과 구현 전달 준비 | — | — | ✅ | 디자인 기준·순서는 pycoding project_setup_design.md |
| 43 | operator | omh-github-event-ops | GitHub 이벤트 처리 경로 판단 | — | — | ✅ | — |
| 44 | operator | omh-github-issue-intake | 버그 제보의 GitHub 이슈화 | — | — | ✅ | — |
| 45 | operator | omh-idea-to-deploy | 아이디어부터 배포까지 단계 설계 | — | — | ✅ | 새 프로젝트 구성 절차가 pycoding project_setup_request.md와 겹침 |
| 46 | operator | omh-image-cards | 이미지 생성 프롬프트 카드 작성 | — | — | ✅ | — |
| 47 | operator | omh-inference-serving | LLM 서빙 엔진 선택·배포·벤치마크 | — | — | ✅ | — |
| 48 | operator | omh-lifecycle-growth | 활성화·리텐션 성장 실험 설계 | — | — | ✅ | — |
| 49 | operator | omh-live-incident-response | 진행 중 장애 대응 지휘 | — | — | ✅ | — |
| 50 | operator | omh-llm-app-dev | LLM 기능 개발·출력 검증 설계 | — | — | ✅ | — |
| 51 | operator | omh-materials-package | 문서·자료 산출물 구성 계획 | — | — | ✅ | 문서 산출물 위치는 pycoding project_setup_docs.md |
| 52 | operator | omh-meeting-brief | 회의 안건·준비 자료 작성 | — | — | ✅ | — |
| 53 | operator | omh-operating-rhythm | 정기 회의록·결정 로그 관리 | — | — | ✅ | — |
| 54 | operator | omh-ops-review | 운영 현황·위험·후속 조치 요약 | — | — | ✅ | — |
| 55 | operator | omh-people-ops | 공정한 채용 평가 자료 준비 | — | — | ✅ | — |
| 56 | operator | omh-physical-device-readiness | 물리 장치 제어 전 안전 점검 | — | — | ✅ | — |
| 57 | operator | omh-provider-profile-posture | 제공자 프로필 역량 메타데이터 기록 | — | — | ✅ | — |
| 58 | operator | omh-reliability-review | 종료 장애 사후 검토·SLO 점검 | — | — | ✅ | — |
| 59 | operator | omh-report-package | 정기·임원 보고서 작성 | — | — | ✅ | 보고서 문체·저장 위치는 pycoding project_setup_docs.md |
| 60 | operator | omh-sales-development | 영업 계정 탐색·자격 검증 브리프 | — | — | ✅ | — |
| 61 | operator | omh-sales-pipeline-review | 영업 파이프라인 건전성 검토 | — | — | ✅ | — |
| 62 | operator | omh-skill-health | 스킬 포트폴리오 상태 대시보드 | — | — | ✅ | — |
| 63 | operator | omh-skill-scout | 기존 스킬 탐색·재사용 판단 | — | — | ✅ | — |
| 64 | operator | omh-support-operations | 지원 티켓 답변 초안·에스컬레이션 | — | — | ✅ | — |
| 65 | operator | omh-visual-qa | 화면 캡처 기반 시각 품질 검증 | — | — | ✅ | 실제 화면 검증 기준은 pycoding project_setup_design.md |
| 66 | operator | omh-workspace-audit | 작업 공간 구성 읽기 전용 점검 | — | — | ✅ | — |
| 67 | planner | omh-adversarial-consensus | 제안 레드팀 검토·합의 도출 | — | — | ✅ | — |
| 68 | planner | omh-agent-instructions | 에이전트 지침 파일 작성·갱신 | — | — | ✅ | 프로젝트 AGENTS.md 내용은 pycoding 템플릿 |
| 69 | planner | omh-backend | 서버·API 설계 전 경계·오류 정리 | — | — | ✅ | — |
| 70 | planner | omh-codebase-onboarding | 코드베이스 구조 파악·온보딩 | — | — | ✅ | — |
| 71 | planner | omh-codebase-uml | 코드베이스 UML 다이어그램 생성 | — | — | ✅ | — |
| 72 | planner | omh-codegraph-refresh | 코드그래프 갱신 실행·보고 | — | — | ✅ | — |
| 73 | planner | omh-curriculum-design | 학습 목표 기반 커리큘럼 설계 | — | — | ✅ | — |
| 74 | planner | omh-data-pipelines | 데이터 파이프라인 멱등성 설계 | — | — | ✅ | — |
| 75 | planner | omh-decision-prototype | 결정용 소규모 스파이크 실행 | — | — | ✅ | — |
| 76 | planner | omh-iac-change | 인프라 코드 변경 계획·영향 검토 | — | — | ✅ | — |
| 77 | planner | omh-mobile-release | 모바일 앱 스토어 출시 계획 | — | — | ✅ | — |
| 78 | planner | omh-model-finetuning | 모델 파인튜닝 여부·방식 결정 | — | — | ✅ | — |
| 79 | planner | omh-plan | 목표·수용 기준 중심 작업 계획 | — | — | ✅ | — |
| 80 | planner | omh-product-brief | PRD·로드맵 우선순위 브리프 | — | — | ✅ | 제품 기획 의도 정리는 pycoding project_setup_request.md 1단계 |
| 81 | planner | omh-product-discovery-validation | 초기 제품 아이디어 근거 검증 | — | — | ✅ | 제품 기획 의도 정리는 pycoding project_setup_request.md 1단계 |
| 82 | planner | omh-refactor-plan | 대규모 리팩터링 단계별 계획 | — | — | ✅ | — |
| 83 | planner | omh-relational-db | 관계형 DB 인덱스·마이그레이션 계획 | — | — | ✅ | — |
| 84 | planner | omh-release-cut | 버전 릴리스 범위·카나리 계획 | — | — | ✅ | — |
| 85 | planner | omh-rust | Rust 변경 설계·검증 게이트 | — | — | ✅ | — |
| 86 | researcher | omh-docs | OMH 공식 문서 기반 질의응답 | — | — | ✅ | — |
| 87 | researcher | omh-jit-learn | 현재 막힌 지점 즉시 학습 | — | — | ✅ | — |
| 88 | researcher | omh-long-document-reading | 대용량 PDF 구간별 정독 | — | — | ✅ | — |
| 89 | researcher | omh-paper-learning | 논문 수준별 섹션 해설 | — | — | ✅ | — |
| 90 | researcher | omh-research-brief | 시장·경쟁 조사 근거 브리프 | — | — | ✅ | — |
| 91 | researcher | omh-research-department | 정기 리서치 운영 체계 구성 | — | — | ✅ | — |
| 92 | researcher | omh-source-finder | 연구 자료 후보 목록 작성 | — | — | ✅ | — |
| 93 | researcher | omh-web-research | 최신 사실 웹 조사·출처 명시 | — | — | ✅ | — |
| 94 | reviewer | omh-accessibility-audit | WCAG 접근성 감사 | — | — | ✅ | 접근성 기준은 pycoding project_setup_design.md |
| 95 | reviewer | omh-app-debugging | 재현 기반 앱 버그 디버깅 | — | — | ✅ | — |
| 96 | reviewer | omh-application-threat-model | 애플리케이션 위협 모델링 | — | — | ✅ | — |
| 97 | reviewer | omh-ask | 외부 자문 모델 비평 요청 | — | — | ✅ | — |
| 98 | reviewer | omh-build-failure-triage | 빌드·CI 실패 원인 분류 | — | — | ✅ | — |
| 99 | reviewer | omh-code-review | 버그 우선 코드 리뷰 | — | — | ✅ | — |
| 100 | reviewer | omh-commit-pr-authoring | 커밋 메시지·PR 본문 작성 | — | — | ✅ | — |
| 101 | reviewer | omh-failure-signal-audit | 숨은 오류·거짓 성공 신호 감사 | — | — | ✅ | — |
| 102 | reviewer | omh-git-workflow | 병합 충돌·이력 재작성 계획 | — | — | ✅ | — |
| 103 | reviewer | omh-internal-audit | 내부통제 테스트·감사 | — | — | ✅ | — |
| 104 | reviewer | omh-jev-action-check | 위험 명령 Jev 보류 점검 | — | — | ✅ | — |
| 105 | reviewer | omh-jev-done-check | 완료 주장 Jev 검증 | — | — | ✅ | — |
| 106 | reviewer | omh-jev-failure-triage | 실패 명령 Jev 대응 제안 | — | — | ✅ | — |
| 107 | reviewer | omh-jev-review-gate | Jev 기반 diff 위험 플래그 검토 | — | — | ✅ | — |
| 108 | reviewer | omh-legal-compliance-review | 법률·컴플라이언스 쟁점 검토 | — | — | ✅ | — |
| 109 | reviewer | omh-localization-review | 현지화 번역 품질 검토 | — | — | ✅ | 현지화 기준은 pycoding project_setup_aso.md |
| 110 | reviewer | omh-native-debugging | 네이티브 크래시 가설 기반 디버깅 | — | — | ✅ | — |
| 111 | reviewer | omh-production-audit | 출시 준비도 점검·판정 | — | — | ✅ | — |
| 112 | reviewer | omh-security-event-response | 출시 코드 보안 이벤트 대응 | — | — | ✅ | — |
| 113 | reviewer | omh-security-safety-review | 에이전트 실행 전 보안 검토 | — | — | ✅ | — |
| 114 | reviewer | omh-tech-debt-audit | 기술 부채 감사·개선 대장 | — | — | ✅ | — |
| 115 | reviewer | omh-verification-gate | 관찰 결과 기반 검증 판정 | — | — | ✅ | — |
| 116 | tracker | omh-achievements | 업적 배지·등급 요약 | — | — | ✅ | — |
| 117 | tracker | omh-agent-board | 다중 에이전트 칸반 작업 조율 | — | — | ✅ | — |
| 118 | tracker | omh-agent-ops-review | 에이전트 진행 현황 관리 카드 | — | — | ✅ | — |
| 119 | tracker | omh-buzz | Buzz 커뮤니티 연결·릴레이 진단 | — | — | ✅ | — |
| 120 | tracker | omh-cancel | 활성 워크플로 중단·상태 정리 | — | — | ✅ | — |
| 121 | tracker | omh-capability-toggle | OMH 기능군 활성화 전환 | — | — | ✅ | — |
| 122 | tracker | omh-context-budget-review | 장기 작업 컨텍스트 예산 계획 | — | — | ✅ | — |
| 123 | tracker | omh-doctor | OMH 설치 상태 진단 | — | — | ✅ | — |
| 124 | tracker | omh-harness-session-inventory | 에이전트 세션 메타데이터 통합 | — | — | ✅ | — |
| 125 | tracker | omh-instinct-ledger | 반복 교훈의 직관 후보 관리 | — | — | ✅ | — |
| 126 | tracker | omh-model-optimization | 신규 모델 출시 대응 최적화 | — | — | ✅ | — |
| 127 | tracker | omh-ops-observability-card | 토큰·비용·지연 운영 현황판 | — | — | ✅ | — |
| 128 | tracker | omh-run-efficiency | 실행 효율 지표 보고 | — | — | ✅ | — |
| 129 | tracker | omh-running-work-board | 실행 중 코딩 작업 현황판 | — | — | ✅ | — |
| 130 | tracker | omh-skill | 로컬 OMH 스킬 관리 | — | — | ✅ | — |
| 131 | tracker | omh-todo-checklist | 계획 체크리스트 선언·진행 | — | — | ✅ | — |
| 132 | tracker | omh-toolbelt-readiness | 워크플로 필요 도구 준비 점검 | — | — | ✅ | — |
| 133 | tracker | omh-workflow-learning | 워크플로 시도 기록·개선 학습 | — | — | ✅ | — |
| 134 | ultrawork | ulw-context | 저장소 용어 정렬·결정 | — | — | ✅ | — |
| 135 | ultrawork | ulw-interview | 모호한 요청 단계별 명확화 | — | — | ✅ | — |
| 136 | ultrawork | ulw-loop | 장기 목표 반복 실행 엔진 | — | — | ✅ | — |
| 137 | ultrawork | ulw-maestro | 외부 코딩 CLI 핸드오프 프롬프트 작성 | — | — | ✅ | — |
| 138 | ultrawork | ulw-perf | 성능 저하·누수 원인 국소화 | — | — | ✅ | — |
| 139 | ultrawork | ulw-plan | 실행 전 검토된 계획 수립 | — | — | ✅ | 계획 파일을 `.omh/plans`에 씀. 프로젝트 문서 위치는 pycoding project_setup_docs.md |
| 140 | ultrawork | ulw-qa | 적대적 QA 시나리오 생성 | — | — | ✅ | — |
| 141 | ultrawork | ulw-research | 의사결정 전 심층 리서치 | — | — | ✅ | — |
| 142 | ultrawork | ulw-work | 승인 계획 의존성 기반 실행 | — | — | ✅ | — |

## 5. pycoding-prompt와의 적용 경계

| 항목 | 현재 상태 | 경계와 후속 작업 |
|---|---|---|
| 새 시각 방향의 레퍼런스 선택 | 사용자가 선택 절차를 요청하거나 에이전트의 제안에 동의하면 최소 5개 추천→사용자 선택→구현을 따른다 | 일반 화면 요청은 제품 목적·기존 브랜드·현재 디자인 기준으로 구현한다. pycoding-prompt도 사용자 선택이 없는 구현 경로를 둔다 |
| @shadcn/lint | Agent-setup `shadcn-lint` 스킬은 설치·설정 방법을 제공한다 | 규칙 선택, 제품 토큰, 프로젝트 의존성과 lint·CI는 pycoding-prompt 기준 및 대상 프로젝트가 소유한다 |
| 문장·코드 정리 스킬 준비 (Humanizer 등) | Agent-setup은 전역 스킬을 설치한다. pycoding-prompt는 현재 부족한 스킬의 설치도 요청한다 | Agent-setup으로 먼저 준비한 환경에서는 pycoding-prompt가 스킬 로드를 확인한다. 설치 책임을 완전히 분리하는 pycoding-prompt 문구 변경이 남아 있다 |
| shadcn 공식 스킬 | Agent-setup은 전역 스킬을 설치한다 | pycoding-prompt는 프로젝트 작업에서 로드된 스킬을 사용하고, 제품의 shadcn/ui 구성은 대상 프로젝트에 적용한다 |
| 문서와 응답의 표현 3줄 | Agent-setup 전역 지침 + pycoding `project_setup_docs.md` | 전역 작업과 제품 문서 적용 양쪽에서 쓰는 짧은 공통 기준. pycoding을 독립적으로 사용할 때도 적용 가능하게 유지 |

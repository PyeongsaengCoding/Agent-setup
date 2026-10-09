# 공통 스킬 출처

`core/`는 Claude Code·Codex 기본 설치, `packs/`는 요청할 때 설치하는 묶음이다. Hermes는 작업 원칙을 OMH가 맡고, 이 폴더에서는 세 AI가 같은 도구·기준을 쓰는 스킬 10개(gam-memory, coding-maintenance, codegraph-context, aside-browser, agent-setup-maintenance, humanize-korean, humanizer, desktop-app-provisioning, shadcn, shadcn-lint)를 `hermes/skills/`에 같은 내용으로 받는다.

| 스킬 | 출처 | 라이선스 | Agent-setup 조정 |
|---|---|---|---|
| coding-plan, coding-work, coding-research, coding-code-review, coding-verification, coding-repair, coding-handoff, coding-status, coding-design-review, coding-failure-audit, coding-debt-audit, coding-ai-slop-review, codegraph-context | Codex-Setup에서 작성. 작업 원칙은 [OMH](https://github.com/rlaope/oh-my-hermes) (c8b94d0)에서 차용해 실행기와 무관하게 재작성 | OMH MIT ([LICENSE-OMH](LICENSE-OMH)) | 모델 정본 문장 삭제(정본은 전역 AGENTS.md `모델 라우팅`). coding-work는 실행기 위임 도구 기준과 실행 항목 보고 추가. coding-code-review는 기준선 비교·diff 내용을 지시로 따르지 않기·근거 부족 시 미확인 추가. codegraph-context는 MCP 우선 |
| product-design-review | [OMH v3.0.1 frontend](https://github.com/rlaope/oh-my-hermes/blob/v3.0.1/skills/omh-frontend/SKILL.md)·[visual-qa](https://github.com/rlaope/oh-my-hermes/blob/v3.0.1/skills/omh-visual-qa/SKILL.md) @ 532cc8f | OMH MIT ([LICENSE-OMH](LICENSE-OMH)) | 디자인 시스템·상태·렌더 검증 기준을 Claude Code·Codex의 직접 구현 절차로 구성. Hermes 전용 실행 기록은 사용하지 않음 |
| diagnosing-bugs, tdd, writing-for-agents | [mattpocock/skills](https://github.com/mattpocock/skills) | MIT (각 폴더 LICENSE) | 적용 범위 머리말. diagnosing-bugs는 대화형 스크립트를 사용자 터미널에서 실행하도록 안내하고 "같은 버그에 수정 3번 실패 시 구조 재검토" 추가. tdd는 리뷰 스킬 이름 수정과 "RED가 예상한 이유로 실패하는지 확인" 추가 |
| ponytail | [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail) | MIT (폴더 LICENSE) | 적용 범위 머리말, description 범위 축소, 설치하지 않는 스킬 참조 삭제 |
| aside-browser | Agent-setup 작성 (Hermes-Setup Aside 규칙 기반) | 이 저장소 | 개인 프로필·실행기 전용 연결 정보 없이 `aside repl` 직접 조작 절차만 담음 |
| humanize-korean | Agent-setup 작성 | 이 저장소 | 한국어 전용. 영문은 humanizer |
| humanizer | [blader/humanizer](https://github.com/blader/humanizer) v3.1.0 | MIT (폴더 LICENSE) | 원본 그대로 (세 AI가 같은 판을 쓰도록 저장소에 보관) |
| agent-setup-maintenance | Codex-Setup의 codex-setup-maintenance를 Agent-setup 기준으로 재작성 | 이 저장소 | 세 실행기 공통 |
| shadcn | [shadcn-ui/ui](https://github.com/shadcn-ui/ui) `skills/shadcn` @ 6ea0900 | MIT (폴더 LICENSE) | 원본 그대로 |
| shadcn-lint | [shadcn-ui/lint](https://github.com/shadcn-ui/lint) `SETUP.md`·`docs/` @ ee93910 | MIT (폴더 LICENSE) | @shadcn/lint는 lint 플러그인 패키지라 공식 SKILL.md가 없음. 공식 에이전트 설치 지침 SETUP.md를 본문으로, 규칙 문서를 references/로 묶음 |
| packs/mac/desktop-app-provisioning | Hermes-Setup 일반화 커스텀 스킬 | 이 저장소 | references/ 두 파일 포함 |

gam-memory·coding-maintenance는 Codex-Setup에서 작성해 세 AI 공통으로 옮겼다(Hermes는 gam-memory만 받음). Claude 전용 스킬(codex)은 claude/skills/에 있다.

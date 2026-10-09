---
name: codex
description: 모델 라우팅 순서가 GPT 모델(gpt-*)을 가리키거나, 사용자가 Codex·GPT에 맡기라고 하거나, 중요한 변경을 다른 모델로 독립 리뷰해야 할 때 Codex 플러그인으로 작업을 넘기고 결과를 회수한다.
---

# Codex 플러그인 위임

Claude Code에서 GPT 모델은 Codex 플러그인(`codex@openai-codex`)으로 실행한다. 이 컴퓨터의 Codex CLI 로그인과 Codex 사용 한도를 쓴다.

## 언제

- `~/.claude/agent-setup/routing.json`에서 고른 분류의 현재 항목이 `executor: codex:codex-rescue`일 때.
- 사용자가 Codex·GPT 실행을 지정했을 때.
- coding-code-review에서 구현과 다른 모델의 독립 리뷰가 필요할 때: `/codex:review`(또는 적대적 검토가 필요하면 `/codex:adversarial-review`).

## 넘기는 방법

1. `codex:codex-rescue` 하위 에이전트에 작업을 넘기며 routing.json 항목의 `--model <model> --effort <effort>`를 붙인다. 사용자가 모델을 지정했으면 그 값을 쓴다.
2. 지시문에 목표, 대상 경로, 읽기·쓰기 범위, 제약, 완료 조건, 검증 명령을 넣는다. 조사·리뷰만 맡길 때는 "읽기 전용, 파일 수정 금지"를 적는다. 파일 수정을 맡길 때는 그 담당만 해당 파일을 쓰게 한다.
3. 플러그인 명령과 옵션은 설치된 버전에서 확인한다(`/codex:setup`, 플러그인 도움말). 문서에 적힌 옵션이 실제로 없으면 없는 옵션을 만들어 쓰지 않는다.

## 결과 처리

- 결과가 비었거나, 모델 사용 불가·한도·인증 오류로 실패하면 같은 작업을 routing.json 순서의 다음 항목으로 넘긴다. 마지막 항목도 실패하면 오류 내용을 보고한다.
- 받은 결과의 변경 파일과 주장을 실제 diff·검사 결과와 대조한다. Codex의 성공 보고만으로 완료 처리하지 않는다.
- 보고할 때 분류, 요청한 모델·추론, 실제로 실행된 항목을 적는다.
- `/codex:setup`이 Codex 미설치·미로그인을 알리면 사용자에게 로그인을 요청하고, 그동안은 routing.json의 Claude 항목으로 진행한다.

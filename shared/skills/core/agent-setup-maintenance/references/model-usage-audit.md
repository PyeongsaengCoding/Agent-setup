# 실제 사용 모델·구독 사용량 감사 (Hermes)

사용자가 "Claude(또는 GPT) 사용량이 왜 안 줄어드나/왜 이쪽만 빠지나"를 물을 때 쓴다. 설정값보다 실제 호출 기록을 근거로 답한다.

## 1. 경로별 적용 규칙 구분

- `~/.omh/routing/model-chains.json`(OMH 분류 체인)은 `delegate_task` 자식에만 적용된다. 메인 대화는 `$HERMES_HOME/config.yaml`의 `model.default`/`model.provider`를 따른다.
- 메인 세션 모델은 세션 시작 시 고정된다(`sessions.model`). 기본 모델을 바꿔도 열린 세션은 그대로이므로 새 세션을 열거나 Desktop/gateway를 재시작해야 한다.
- cron 작업(`$HERMES_HOME/cron/jobs.json`)에 `model`/`provider`가 비어 있으면 기본 모델을 따른다. 특정 작업을 Claude로 돌리려면 작업에 모델을 직접 지정한다.
- Claude Code CLI(`claude`)는 Hermes의 anthropic provider와 인증이 따로다. `claude auth status`(`loggedIn`)와 `claude -p "..." --output-format json`으로 확인한다. `is_error:true`에 usage가 전부 0이면 요청이 API에 도달하지 않은 것이다. 재로그인(`claude auth login`)은 브라우저 인증이 필요해 사용자가 한다.

## 2. 세션 단위 증거 (`$HERMES_HOME/state.db`)

```sql
-- 세션이 실제로 쓴 모델·provider·호출 수
select model,billing_provider,task,api_call_count,input_tokens,output_tokens
  from session_model_usage where session_id='<S>';
-- 자식 세션
select id,model from sessions where parent_session_id='<S>';
-- 일별 provider별 호출량
select date(last_seen,'unixepoch','localtime') d,billing_provider,sum(api_call_count)
  from session_model_usage where last_seen>strftime('%s','now','-5 days')
  and billing_provider!='' group by 1,2;
```

- `delegate_task` 실행 여부는 `messages.tool_calls`와 자식 세션으로 판단한다. `content like '%delegate_task%'`는 스킬 본문 텍스트에도 걸려 오탐이 난다.

```sql
-- 라우팅표가 실제로 닿는 비중: 메인(기본 모델) vs 하위 에이전트(OMH 체인), 출처별
select case when ifnull(s.parent_session_id,'')='' then 'main' else 'subagent' end kind,
       s.source, u.billing_provider, sum(u.api_call_count)
  from session_model_usage u join sessions s on s.id=u.session_id
 where u.last_seen>strftime('%s','now','-7 days') and u.billing_provider!=''
 group by 1,2,3 order by 4 desc;
-- 최근 15분 활성 세션별 모델 (지금 무엇이 어떤 모델로 도는지)
select session_id,model,billing_provider,sum(api_call_count)
  from session_model_usage where last_seen>strftime('%s','now','-15 minutes') group by 1,2,3;
```

- "이 세션에서 돌아가는 작업"을 물으면 자식 세션만 보지 않는다. 총괄 대화는 칸반에 일을 넘기는 경우가 많다. `hermes kanban boards`로 보드를 찾고 `$HERMES_HOME/kanban/boards/<slug>/kanban.db`의 `tasks`(status·model_override·session_id=생성한 세션)를 읽은 뒤, 작업자 세션(`source=kanban`, 첫 메시지 `work kanban task <id>`)의 모델을 대조한다. 기본 `kanban.db`는 비어 있을 수 있다.
- `ps`에서 `hermes_cli.main ... chat -q "work kanban task t_…"`가 실행 중인 칸반 작업자다.
- cron 하위 에이전트가 `route-provenance.json`에 기록이 없으면 분류 없이 부모(cron 세션) 모델을 물려받은 것으로 본다.

## 3. 계정 분배

- `hermes auth list`로 anthropic 자격증명 풀(계정·우선순위)을 본다. 호출은 풀 계정에 나뉘며 state.db에는 계정별 분배가 남지 않고 `request_count`도 0으로 남을 수 있다. 사용자가 본 사용량 화면이 어느 계정인지 묻고, 1순위 계정과 대조한다.

## 4. 기본 모델을 Claude로 전환할 때

1. `config.yaml`을 타임스탬프 백업한다.
2. `model.default`/`model.provider`를 anthropic 모델로 바꾸고 `fallback_providers`의 GPT/Claude를 맞바꾼다.
3. `model.base_url`이 `https://chatgpt.com/backend-api/codex`면 주석 처리한다. 남기면 anthropic 요청이 Codex 엔드포인트로 간다.
4. 전환 전에 `config.yaml`의 web 검색·추출 backend를 확인한다. `openai-native`는 openai-codex 전송에서만 동작해서, 메인 provider를 anthropic으로 바꾸면 web_search는 키 없는 임시 경로로 떨어지고 web_extract(링크 본문 읽기)는 실패한다. firecrawl·tavily·exa 등 키가 있는 backend를 지정하거나, 없으면 전환과 함께 이 영향을 사용자에게 알리고 Aside 브라우저 읽기를 대안으로 제시한다.
5. `hermes chat -q "한 단어로: 안녕"`으로 실제 응답을 확인하고, 이후 해당 세션의 `session_model_usage`에 anthropic이 찍히는지 본다. 전환 후 `logs/gui.log`에서 `web_search backend`·`web_extract` 실패가 새로 생겼는지 본다.

## 보고

원인 → 증거 표(모델·용도·호출 수) → 라우팅표 → 바로 할 수 있는 조치 순서로 짧게 답한다. 구독 사용량 질문에는 설정값보다 실제 호출 기록을 먼저 보여 준다.

- "OMH를 적용했으니 모든 작업이 작업 종류별 모델로 돈다"는 기대가 흔하다. 첫 답에서 라우팅이 닿는 범위(하위 에이전트만)와 닿지 않는 범위(메인·cron·칸반)를 main/subagent 호출 비중 표로 바로 보여 준다. 범위를 여러 턴에 걸쳐 조금씩 드러내면 신뢰를 잃는다.
- 범위 밖을 메우는 조치는 세 가지로 제시한다: 기본 모델 조정, 칸반 `model_override`·cron `model`에 작업 종류별 모델 지정(제안 매핑 표 포함), 메인은 지휘만 하고 실작업을 분류해 `delegate_task`로 위임하는 지침. 전역 지침 변경은 Agent-setup 원본 경로로 하고 적용 전 확인받는다.

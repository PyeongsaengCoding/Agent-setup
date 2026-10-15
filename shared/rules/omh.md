## OMH 워크플로 스킬

- OMH(oh-my-hermes) 스킬(`omh-*`, `ulw-*`)이 설치되어 있다. 요청이 계획·검토·조사·운영·디자인처럼 결과를 문서나 근거로 남겨야 하는 작업이면 맞는 OMH 스킬을 읽고 그 절차를 따른다. 일반 답변과 한 번에 끝나는 조회는 바로 처리한다.
- 같은 일을 하는 공통 스킬(coding-*)과 OMH 스킬이 함께 맞으면 OMH 스킬의 절차를 우선하고, 공통 스킬의 보고·검증 기준을 함께 적용한다.
- OMH 스킬은 Hermes 도구 이름을 쓴다. 이 실행기에서는 대응 수단으로 같은 결과를 만든다: `omh_todo`는 실행기의 할 일 목록, `omh_memory`는 GAM(gam-memory), `omh_delegate_route`·`delegate_task`는 아래 모델 라우팅에 따른 위임, `omh_jev_ask`는 다른 모델 계열에 맡긴 독립 검토, `omh_codegraph_summary`는 CodeGraph, `omh_agent_board`·`omh_run_summary`는 작업 폴더의 Markdown 기록, `omh_reviewed`·`omh_operation_artifact`는 결과 파일과 검증 기록이다. 그 밖의 `omh_*` 도구는 같은 산출물을 파일과 명령으로 만든다.
- OMH 기록은 작업 대상 저장소의 `.omh/`에 둔다. OMH 스킬이 말하는 준비 상태와 실제 실행·검증 결과를 구분해 보고한다.
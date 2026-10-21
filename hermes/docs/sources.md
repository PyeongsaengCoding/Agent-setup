# 출처

- [Hermes 공식 문서](https://hermes-agent.nousresearch.com/docs/): 설치·스킬·플러그인·브라우저·설정
- [Hermes 원본](https://github.com/NousResearch/hermes-agent/tree/d923a5eb487a17c0a68801bba9ef0f56c81040a8): 이 목록의 공식 스킬 57개 기준 (v0.22.2)
- [OMH v4.0.0 설치 안내](https://github.com/rlaope/oh-my-hermes/blob/36e96feb432068cd27eecf5b434acdf1328341b4/INSTALL_FOR_AGENTS.md): Hermes용 검토 기준
- [Provider Usage](https://github.com/PhoeniXAbhisheK/hermes-plugin-provider-usage/tree/023e7e54d6f6c5ec55314f7603ed5b80af81cd54): 필수 사용량 플러그인 v0.2.1
- [Aside 개발자 안내](https://docs.aside.com/help/developers): CLI·REPL·MCP
- [Agent-setup 공통 스킬 출처](../../shared/skills/SOURCES.md): 공통 스킬 34개의 원본과 고정 버전

`manifest.json`은 설치 출처를 고정한다. 설치 시점의 최신 문서를 확인하되 검증 없이 잠금 버전을 바꾸지 않는다. 공식 스킬의 지원 파일과 라이선스는 원본에서 함께 가져온다.

Hermes 배포본의 공통 스킬 34개는 Agent-setup `shared/skills/`에서 관리한다. 공식 스킬 57개는 위 Hermes 고정 커밋의 지원 파일과 라이선스를 함께 배포한다. 외부 스킬 39개는 Agent-setup `codex/inventories/external-skills.json`의 출처와 고정값(원본별 최신 정식 릴리스 태그 `releaseTag`와 그 커밋 `ref`)을 따른다.

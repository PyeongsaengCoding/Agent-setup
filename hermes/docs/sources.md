# 출처

- [Hermes 공식 문서](https://hermes-agent.nousresearch.com/docs/): 설치·스킬·플러그인·브라우저·설정
- [Hermes 원본](https://github.com/NousResearch/hermes-agent/tree/b2860025adc1478eca63a0b2a82440798eadbfd1): 이 목록의 공식 스킬 57개 기준
- [OMH 설치 안내](https://github.com/rlaope/oh-my-hermes/blob/4575d7fb64e2d931ee238a10c918a2e5e83f5b97/INSTALL_FOR_AGENTS.md): 조사 시점의 설치 기준
- [Provider Usage](https://github.com/PhoeniXAbhisheK/hermes-plugin-provider-usage/tree/753dfbd35c9ed8fec3127ce48e5521d986d3aabe): 필수 사용량 플러그인 v0.2.0
- [Aside 개발자 안내](https://docs.aside.com/help/developers): CLI·REPL·MCP
- [Agent-setup 공통 스킬 출처](../../shared/skills/SOURCES.md): 공통 스킬 10개의 원본과 고정 버전

`manifest.json`은 설치 출처를 고정한다. 설치 시점의 최신 문서를 확인하되 검증 없이 잠금 버전을 바꾸지 않는다. 공식 스킬의 지원 파일과 라이선스는 원본에서 함께 가져온다.

Hermes 배포본의 공통 스킬 10개는 Agent-setup `shared/skills/`에서 관리한다. 공식 스킬 57개는 위 Hermes 고정 커밋의 지원 파일과 라이선스를 함께 배포한다. 외부 스킬 37개는 Agent-setup `codex/inventories/external-skills.json`의 출처와 잠금 버전을 따른다.

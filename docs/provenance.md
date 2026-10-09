# 출처

세 원본 저장소의 추적 파일을 실행기 폴더에 복사했다. 출처 커밋과 파일별 SHA256는 [이관 목록](import-manifest.json)에 있다.

| 폴더 | 원본 | 라이선스·출처 |
|---|---|---|
| codex/ | Codex-Setup | upstream/README.md, upstream-LICENSE-OMH (OMH MIT), 차용 스킬별 LICENSE, inventories/ 잠금 기록 |
| claude/ | Claude-Setup (로컬) | routes/claude-code.json의 OMH 출처, upstream-LICENSE-OMH (OMH MIT 사본) |
| hermes/ | Hermes-Setup | LICENSE (MIT), docs/sources.md, manifest.json의 원본·플러그인 커밋 |

OMH 참조 커밋은 Codex·Claude가 c8b94d0, Hermes가 4575d7f다.

외부 공개 전에 확인할 항목:

- Codex-Setup 자체의 최상위 라이선스
- codex/inventories/external-skills.json 외부 스킬 38개의 라이선스
- Hermes provider-usage 플러그인의 라이선스

루트의 README·AGENTS·CLAUDE·docs/·scripts/check.py·tests/는 Agent-setup에서 작성했다.

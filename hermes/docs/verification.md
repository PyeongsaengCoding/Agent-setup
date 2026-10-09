# 검증 상태

Agent-setup 루트에서 Python 3.12 이상으로 Hermes 원본을 검사한다.

```sh
python3 scripts/check.py --executor hermes
```

위 통합 검사는 문서·경로·스킬 목록 검사와 Hermes 단위시험을 실행한다. 단위시험만 실행할 때는 `hermes/`에서 `python3 -m unittest discover -s tests -v`를 쓴다. 이관 이후 검사 결과는 Agent-setup 루트의 project-records/에 있다. 이관 전 기록은 Hermes-Setup 저장소의 reports/·project-records/에 있다.

## 실제 환경 완료 기준

- 라우팅은 선택한 [프리셋](model-routing.md)으로 맞춘다.
- Aside·문서 전달 규칙은 [전역 규칙 안내](global-rules.md)대로 선택한 프로필에 적용하고 새 세션에서 동작을 확인한다.
- [설치 완료 기준](../INSTALL_FOR_AGENTS.md)에 따라 설치·로그인·실제 위임·fallback·추론·사용량 UI·Aside 프로필과 포커스·Desktop UI 크기를 각각 확인한다.
- fallback과 추론 유지는 실제 제공자 전환으로 확인한다. mock 시험 결과는 별도로 기록한다.

현재 전역 규칙 설치 대상은 공통 작업 원칙, Aside 직접 조작, Desktop 문서 전달의 세 관리 구간이다.

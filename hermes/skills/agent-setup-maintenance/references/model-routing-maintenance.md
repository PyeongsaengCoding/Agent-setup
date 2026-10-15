# 실행기별 모델 라우팅 원본과 적용 동기화

## 1. 승인안과 수정 범위 고정

설치 기록에서 Agent-setup 루트를 찾고 대상 실행기 지침을 읽는다. 선택한 프리셋의 모델 ID·순서·effort를 기대값 한 곳에 정리한다. 사용자에게 현재 적용값, 설치된 OMH 기본값, 적용할 값을 나란히 제시하고 승인된 분류를 고정한다. 주 에이전트와 자식 공통 fallback은 별도로 읽어 보존 또는 변경 범위를 정한다.

## 2. 원본 의존성 좁게 읽기

Hermes 변경에서는 선택한 `hermes/routing-presets/<preset>.json`, `hermes/routing-snapshot.json`, `hermes/docs/model-routing.md`와 관련 시험을 확인한다. 프리셋을 읽는 시험, 문서의 CLI 블록을 검사하는 시험, snapshot에 옛 모델 순서를 고정한 시험, 실행기 간 동일성을 검사하는 루트 시험을 함께 검색한다. 그래프는 위치를 좁히는 데 쓰고 실제 파일과 시험을 근거로 삼는다.

- 프리셋 비교 시험이 동일 후보 집합을 강제하면 새 정책의 후보·추론 변경까지 검증하도록 계약을 조정한다. 서로 다른 정책에는 승인된 각각의 기대값을 사용한다.
- 한 실행기만 변경할 때 다른 실행기의 원본과 동일하도록 만드는 시험은 실행기별 기존 정책 보존 시험으로 바꾼다. 공유 시험 때문에 승인 범위를 넓히면 외부 실행기의 모델 선택도 함께 바뀐다.

## 3. 회귀 시험부터 갱신

승인된 전체 분류의 정확한 `(model, reasoning_effort)` 배열과 주·자식 fallback 마지막 후보를 검증하는 시험을 먼저 추가하고 기대한 assertion 실패를 확인한다. 실제 인터프리터 버전을 확인해 RED와 GREEN에 같은 호환 Python을 사용한다.

원본 프리셋과 필요한 호환 사본을 갱신하고, 사람이 읽는 표와 복사 가능한 `omh model-chains set` 명령을 같은 데이터에서 생성한다. 날짜·가용성 metadata는 관찰한 상태에 맞게 작성하며 설정 예정값과 실제 모델 응답을 구분한다. 변경한 effort를 검사하는 fixture에도 승인된 값을 포함한다.

## 4. 현재 Hermes 적용

1. 선택한 OMH 홈의 기존 체인과 모델 제공자 연결을 비공개 백업에 보존한다.
2. 프리셋의 각 분류를 `omh model-chains set <category> '<model>:<effort>, ...'`로 적용한다.
3. 새 alias는 `model_provider_routes/v1`의 `models`에서 정확한 wire model과 provider를 연결한다. 기존 alias와 다른 실행기의 설정을 유지한다.
4. `omh model-chains show --json`을 파싱해 모든 분류의 순서·effort를 원본과 비교한다.
5. `omh_delegate_route(action="status")`로 실행 중 resolver를 읽고 모든 후보의 provider 연결을 확인한다. `served=true`는 provider가 실제로 해석됐는지 확인하는 단계와 함께 사용한다.
6. `hermes config get fallback_providers`와 `hermes config get delegation.fallback_providers`로 최종 후보를 대조한다. 이미 맞는 공통 fallback은 그대로 유지한다.

## 5. 통합 검사와 보고

호환 Python으로 루트에서 `scripts/check.py --executor hermes`와 루트 `unittest discover -s tests -v`를 실행한다. `git diff --check`와 대상 외 실행기 경로의 diff를 확인해 승인 범위 보존을 증명한다. 코드·문서가 마지막으로 변경된 뒤의 통합 결과를 사용한다.

필요한 소스 호환 패치는 미리보기 결과와 실제 runtime 동작을 함께 검토한다. 라우팅 설정 변경만 요청받은 경우 소스 패치와 활성 프로세스 재시작은 별도 영향 범위로 판단한다. 완료 보고에는 원본 동기화, 실행 중 유효 설정, 실제 호출 여부, 커밋·푸시 상태를 짧게 적고 변경한 문서 경로를 함께 적는다.

# OMH 프론트엔드 적용 기준

OMH [컴포넌트 도입](https://github.com/rlaope/oh-my-hermes/blob/41de9dc5d00956f052e1863d8e1b58eaeef544cb/skills/omh-frontend/references/component-registry-adoption.md), [차트](https://github.com/rlaope/oh-my-hermes/blob/41de9dc5d00956f052e1863d8e1b58eaeef544cb/skills/omh-frontend/references/chart-styling.md), [스타일·푸터](https://github.com/rlaope/oh-my-hermes/blob/41de9dc5d00956f052e1863d8e1b58eaeef544cb/skills/omh-frontend/references/taste-foundations.md)를 Claude Code·Codex의 직접 구현에 적용한다. 해당 요소를 실제로 쓰는 작업에서 필요한 항목만 확인한다.

## 컴포넌트와 라이브러리 선택

- 제품에 이미 있는 컴포넌트와 디자인 토큰을 먼저 확인한다. 새 제품은 필요한 동작·접근성·디자인 자유도·유지보수 비용에 맞춰 headless primitive, shadcn/ui 또는 다른 레지스트리를 선택하고 `DESIGN.md`에 이유를 적는다.
- shadcn 방식의 레지스트리에서 가져온 코드는 프로젝트가 소유한다. Magic UI, React Bits, Aceternity UI 등에서 복사할 때도 실제 원본의 라이선스, 추가 의존성, 번들·성능 비용, CSP, 접근성, 키보드·터치 조작, 줄임 효과 동작, 제품 토큰 대응을 확인한다. 이후 갱신은 로컬 수정과 upstream 차이를 비교해 병합한다.
- 효과는 사용자 과업을 돕는 범위에서 선택한다. 화면마다 주 시각 효과를 정하고, 저사양 기기와 줄임 효과 모드에서 읽기와 조작을 확인한다.

## 마키와 텍스트 효과

- 반복을 위해 복제한 마키 항목과 장식용 분할 문자는 스크린 리더에서 숨긴다. 읽을 수 있는 속도를 택하고 일시정지는 마우스·키보드·터치에서 작동하게 한다.
- `prefers-reduced-motion`에서는 움직임을 멈추고 완전한 내용이나 최종 상태를 보여준다. 텍스트 분할 효과는 원래 문장의 접근 가능한 표현과 폰트 로딩·해제 동작을 확인한다.

## 차트

- 범주형 시리즈와 연속형 값에 서로 다른 색 토큰을 사용한다. 라이트·다크 모드별 팔레트와 대비를 확인하며 색 외에도 직접 레이블이나 모양으로 시리즈를 구분한다.
- 차트 축의 글꼴·크기는 라이브러리의 축 레이블 API로 설정한다. 로딩·데이터 없음·오류 상태를 차트의 최종 크기와 함께 설계한다.

## 스타일과 푸터

- 네오브루탈리즘 같은 스타일 이름은 테두리·그림자·색·모서리·상호작용 토큰으로 정의한다. 네오브루탈리즘을 선택하면 두꺼운 단색 테두리, 블러 없는 오프셋 그림자, 평면적인 색과 눌림 상태를 기준으로 검수한다.
- 푸터는 제품 설명, 방문자 목적에 따른 링크, 필요한 행동·소셜·법적 정보를 정리한다. 모바일에서는 링크 그룹을 읽고 조작할 수 있게 재배치한다.

# Agent-setup

이 저장소는 Codex·Claude Code·Hermes 설치 원본을 실행기별 폴더로 관리한다.

- 작업 전에 README.md와 docs/comparison.md를 읽고, 대상 실행기 폴더의 지침을 따른다.
- 실행기별 원본은 codex/, claude/, hermes/에 있다. 모델·추론·위임·fallback·스킬 발견·설치 방식은 각 폴더에서 관리한다.
- 현재 실행 중인 에이전트는 자기 실행기의 모델 정책을 쓴다. Hermes 안에서 쓰는 Codex 제공자는 Hermes 정책을 따르고, 외부로 실행한 Codex·Claude Code 프로세스는 각자의 정책을 따른다.
- 설치·업데이트는 요청한 실행기와 프로필에 적용한다. 계정·인증·대화·메모리·브라우저 데이터·DB·로그는 Git 저장소에 넣지 않는다.
- 세 실행기의 전역 지침은 `shared/rules/`가 원본이다. 고친 뒤 `python3 scripts/build_rules.py`로 codex/instructions/AGENTS.md, claude/templates/global-rules.md, hermes/templates/common-rules.md를 만든다. 공통 스킬 원본은 `shared/skills/`다. Hermes의 Aside·문서 전달 규칙 원본은 hermes/templates/다.
- Claude Code는 각 폴더의 CLAUDE.md(`@AGENTS.md` 한 줄)로 AGENTS.md를 읽는다. 작업 규칙은 AGENTS.md에만 쓴다.
- 검사는 Python 3.12 이상에서 `python3 scripts/check.py`와 `python3 -m unittest discover -s tests -v`로 실행한다. `python3`가 3.12 미만이면 Homebrew의 `python3.13`이나 `uv run --no-project --python 3.13 python`으로 실행한다.
- 현재 지식은 docs/, 보고용 Markdown은 reports/, 상세 검증 결과는 project-records/에 둔다.
- 커밋·원격 생성·push·외부 게시는 사용자가 요청한 범위에서 실행한다.

<!-- omh:agent-instructions:begin -->
## 문서와 응답의 표현

- 문서·지침·사용자 응답은 목적, 실제 동작, 적용 대상을 직접 설명한다. `~가 아니다`, `~이 아니라`, `~을 뜻하지 않는다` 같은 부정·대조 표현은 쓰지 않는다.
- 규칙에는 적용 대상, 조건, 수행할 행동을 구체적으로 쓴다.
- 요청하지 않은 상황이나 근거 없는 오해를 가정한 방어·면책 문구를 덧붙이지 않는다. 같은 뜻의 설명은 하나로 합친다.

<!-- omh:agent-instructions:end -->

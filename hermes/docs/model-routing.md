# 모델 라우팅

Hermes 내부 위임에 적용하는 사용자 지정 정책이다. 외부 Claude Code·Codex 설정과 현재 대화 모델은 변경하지 않는다. 정확한 모델 ID·순서·추론·fallback은 선택한 프리셋 JSON을 정본으로 삼는다.

## 버전 선택

- [Claude 넉넉형](../routing-presets/claude-generous.json)
- [GPT(코덱스) 넉넉형](../routing-presets/gpt-generous.json)

설치 기본은 Claude 넉넉형이며 GPT(코덱스) 넉넉형은 선택사항이다. [routing-snapshot.json](../routing-snapshot.json)은 Claude형 호환 사본이며 적용 요청에는 프리셋을 명시한다. 설치·전환 요청 없이 기존 환경의 라우팅을 자동 변경하지 않는다.

| 분류 | Claude 넉넉형 | 추론 | GPT 넉넉형 | 추론 |
|---|---|---|---|---|
| ultrabrain | Astra → Opus | xhigh | Astra → Opus | xhigh |
| deep | Opus → Sol | high | Sol → Opus | high |
| architect | Opus → Astra | xhigh | Astra → Opus | xhigh |
| unspecified-high | Sol → Opus | medium | Opus | medium |
| unspecified-low | Sol → Sonnet | low | Opus | low |
| quick | Luna → Opus | low | Luna → Opus → Astra | low |
| writing | Opus → Sonnet → Sol | medium | Sol → Opus | medium |
| visual-engineering | Opus | high | Astra → Opus | high |
| artistry | Opus | high | Astra → Opus | high |
| capable | Opus → Sol | medium | Astra → Opus → Sonnet | medium |
| simple-work | Luna → Haiku 5.5 | low | Luna → Opus → Haiku 4.5 | low |
| deep-work | Opus → Sol | max | Opus → Sol | max |

Claude 넉넉형은 GPT·Claude 후보로 작업별 순서를 구성하고, 최종 fallback을 Opus로 유지한다. Sol은 GPT-6.1 Sol, Luna·Astra는 GPT-6, Opus·Sonnet은 Claude 5.5다. 두 프리셋의 deep-work는 OMH 4.0.0 기본값(Opus → Sol, `max`)을 따른다. 각 실행기의 정책은 해당 폴더에서 독립적으로 관리한다.

## 적용 기준

- GPT·Claude 후보만 사용한다. Kimi·Qwen·Gemini·GLM·DeepSeek를 추가하지 않으며 계정·인증·제공자 연결은 보존한다.
- OMH 분류별 후보와 Hermes 실행 fallback은 별개다. 전역 fallback은 Opus, 자식 공통 fallback은 Opus → Astra → Sonnet이며(2026-10-15 결정: Anthropic 계정 사용량이 모두 소진되면 GPT로 넘어감) 분류 변경으로 공통 순서를 바꾸지 않는다.
- 주 모델이 사용 가능하면 유지한다. 이미 시도한 모델·사용 불가능한 후보는 건너뛴다. 모델별 제한·계정 전체 제한·인증·통신 오류를 구분하고 사용 제한 기록은 초기화하지 않는다.
- 추론은 작업 분류별로 유지하며 전역 모델별 고정으로 대체하지 않는다. 이 프리셋을 최신 모델 목록으로 취급하지 않는다.

선택한 프로필의 로그인·모델 가용성을 확인하고 프리셋의 모든 분류를 적용한다. `~/.omh/routing/model-providers.json`의 `models`에는 GPT 후보를 `openai-codex`, Claude 후보를 `anthropic`으로 연결한다. Claude 넉넉형의 `claude-haiku-5-5`도 같은 이름의 모델과 `anthropic` 제공자를 명시하고 기존 모델 연결을 보존한다. OMH는 연결된 후보를 앞으로 모을 수 있으므로 저장 후 순서·추론·제공자와 실제 자식 fallback을 다시 읽는다.

```sh
omh model-chains show --json
```

공통 fallback 적용 명령:

```sh
hermes config set fallback_providers '[{"provider":"anthropic","model":"claude-opus-5-5"}]'
hermes config set delegation.fallback_providers '[{"provider":"anthropic","model":"claude-opus-5-5"},{"provider":"openai-codex","model":"gpt-6-astra"},{"provider":"anthropic","model":"claude-sonnet-5-5"}]'
```

## fallback 순서·추론 보존

설치된 소스에서 fallback 순서·추론 보존이 필요한지 확인한다. 아래는 소스 호환 패치다. `scripts/` 명령은 Agent-setup의 `hermes/`에서 실행한다.

- `configure_delegation_reasoning.py`: fallback 시 자식에게 배정한 추론을 유지한다.
- `configure_gpt_fallback.py`: GPT 시작 자식에서 Opus를 마지막에 두고 나머지 공통 순서(Astra → Sonnet)를 유지한다. 이전 버전 패치가 설치돼 있으면 같은 명령이 새 순서로 갱신한다. Claude 시작 자식과 공통 설정은 보존한다.

```sh
python3 scripts/configure_delegation_reasoning.py --source-root <확인한-Hermes-소스-루트>
python3 scripts/configure_delegation_reasoning.py --source-root <확인한-Hermes-소스-루트> --apply
python3 scripts/configure_gpt_fallback.py --source-root <확인한-Hermes-소스-루트>
python3 scripts/configure_gpt_fallback.py --source-root <확인한-Hermes-소스-루트> --apply
```

실제 import 경로의 소스 루트를 지정하고 미리보기 후 호환될 때만 적용한다. 변경된 관리 구간·다른 함수 구조·심볼릭 링크는 거부하며 같은 패치는 건너뛴다. 새 프로세스에서 반영을 확인한다. 전환 모델이 추론을 지원하지 않으면 오류를 알리고 수준을 조용히 낮추지 않는다.

## 완료 확인

작업 분류에 맞는 `omh_delegate_route` 적용 직후 `delegate_task`로 최소 실제 위임을 실행한다. 응답과 `session_model_usage`의 모델·`billing_provider`·API 호출 수를 대조하며, 추론이 관측되지 않으면 배정값과 구분한다. 오류가 포함된 `completed`나 대체 모델의 성공을 원래 모델의 성공으로 보고하지 않는다.

fallback 순서와 추론 유지는 실제 한도를 소진하거나 제한을 초기화하지 않고 통제된 시험으로 확인한다. 설정 대조·mock 전환·실제 제공자 호출은 따로 기록한다. 현재 확인 범위와 과거 근거는 [검증 상태](verification.md)에 있다.

## AI에게 적용 요청

아래는 쉘 명령이 아니라 AI 채팅에 붙여 넣는 요청이다. 둘 중 하나만 사용한다.

### Claude 넉넉형 요청

```text
https://github.com/PyeongsaengCoding/Agent-setup 의 main에서 hermes/docs/model-routing.md와 hermes/routing-presets/claude-generous.json을 읽고, 내 현재 Hermes 프로필을 Claude 넉넉형으로 맞춰줘. OMH 분류별 모델 순서·추론과 Hermes 전역·자식 공통 fallback을 구분하고 공통 fallback의 마지막 Opus를 유지해줘. GPT·Claude 계열 외 후보는 모든 분류에서 제거하고, 로그인·구독·다른 프로필은 변경하지 말고, 필요한 호환 패치까지 확인·적용한 뒤 라우팅 설정과 실제 위임 결과를 알려줘.
```

### GPT(코덱스) 넉넉형 요청

```text
https://github.com/PyeongsaengCoding/Agent-setup 의 main에서 hermes/docs/model-routing.md와 hermes/routing-presets/gpt-generous.json을 읽고, 내 현재 Hermes 프로필을 GPT(코덱스) 넉넉형으로 맞춰줘. OMH 분류별 모델 순서·추론과 Hermes 전역·자식 공통 fallback을 구분하고 공통 fallback의 마지막 Opus를 유지해줘. GPT·Claude 계열 외 후보는 모든 분류에서 제거하고, 로그인·구독·다른 프로필은 변경하지 말고, 필요한 호환 패치까지 확인·적용한 뒤 라우팅 설정과 실제 위임 결과를 알려줘.
```

## 선택적 CLI 전환

선택한 버전의 열두 분류를 적용하는 명령이다. 기존 환경에서도 제거한 후보가 남지 않도록 전체 분류를 명시한다. 새 설치는 위 AI 요청으로 전체 프리셋과 호환 패치까지 맞춘다. 현재 프로필을 확인한 뒤 둘 중 한 블록만 실행한다. 미연결 후보를 연결하거나 로그인하지 않는다.

### claude-generous CLI

```sh
omh model-chains set ultrabrain 'gpt-6-astra:xhigh, claude-opus-5-5:xhigh'
omh model-chains set deep 'claude-opus-5-5:high, gpt-6.1-sol:high'
omh model-chains set architect 'claude-opus-5-5:xhigh, gpt-6-astra:xhigh'
omh model-chains set unspecified-high 'gpt-6.1-sol:medium, claude-opus-5-5:medium'
omh model-chains set unspecified-low 'gpt-6.1-sol:low, claude-sonnet-5-5:low'
omh model-chains set quick 'gpt-6-luna:low, claude-opus-5-5:low'
omh model-chains set writing 'claude-opus-5-5:medium, claude-sonnet-5-5:medium, gpt-6.1-sol:medium'
omh model-chains set visual-engineering 'claude-opus-5-5:high'
omh model-chains set artistry 'claude-opus-5-5:high'
omh model-chains set capable 'claude-opus-5-5:medium, gpt-6.1-sol:medium'
omh model-chains set simple-work 'gpt-6-luna:low, claude-haiku-5-5:low'
omh model-chains set deep-work 'claude-opus-5-5:max, gpt-6.1-sol:max'
omh model-chains show --json
```

### gpt-generous CLI

```sh
omh model-chains set ultrabrain 'gpt-6-astra:xhigh, claude-opus-5-5:xhigh'
omh model-chains set deep 'gpt-6.1-sol:high, claude-opus-5-5:high'
omh model-chains set architect 'gpt-6-astra:xhigh, claude-opus-5-5:xhigh'
omh model-chains set unspecified-high 'claude-opus-5-5:medium'
omh model-chains set unspecified-low 'claude-opus-5-5:low'
omh model-chains set quick 'gpt-6-luna:low, claude-opus-5-5:low, gpt-6-astra:low'
omh model-chains set writing 'gpt-6.1-sol:medium, claude-opus-5-5:medium'
omh model-chains set visual-engineering 'gpt-6-astra:high, claude-opus-5-5:high'
omh model-chains set artistry 'gpt-6-astra:high, claude-opus-5-5:high'
omh model-chains set capable 'gpt-6-astra:medium, claude-opus-5-5:medium, claude-sonnet-5-5:medium'
omh model-chains set simple-work 'gpt-6-luna:low, claude-opus-5-5:low, claude-haiku-4-5:low'
omh model-chains set deep-work 'claude-opus-5-5:max, gpt-6.1-sol:max'
omh model-chains show --json
```

## 업데이트

Hermes와 OMH는 아래 블록 하나로 함께 최신 정식 릴리스로 갱신하고, Hermes 본체·provider-usage에는 이 사용자의 수정 묶음(`hermes/patches/`)을 다시 적용한다. Hermes 공식 설치본은 `stable` 채널(최신 `vX.Y.Z` 릴리스 커밋)을 따르고, `hermes update --check`의 `Update channel: stable`로 확인한다. 실행 중인 Hermes 작업이 끝난 뒤 Hermes Desktop을 ⌘Q로 종료하고 터미널에 한 번에 붙여넣는다. `set -e`는 괄호 안에만 적용되어 실패한 단계에서 멈춘다.

```bash
(
  set -e
  AGENT_SETUP="$HOME/Downloads/Coding/personal/Agent-setup"   # 이 컴퓨터의 Agent-setup 체크아웃

  printf '\n[1/5] 업데이트 예정 확인\n'
  hermes update --check
  hermes update --plan

  printf '\n[2/5] Hermes 백업·업데이트·로컬 수정 재적용\n'
  hermes update --backup

  printf '\n[3/5] OMH 최신 정식 릴리스로 업데이트\n'
  OMH_LATEST=$(curl -fsSL https://api.github.com/repos/rlaope/oh-my-hermes/releases/latest | python3 -c 'import json,sys; print(json.load(sys.stdin)["tag_name"].lstrip("v"))')
  printf 'OMH %s\n' "$OMH_LATEST"
  omh update --channel stable --version "$OMH_LATEST"

  printf '\n[4/5] 우리 수정 묶음 확인·설치 상태 점검\n'
  python3 "$AGENT_SETUP/hermes/scripts/apply_local_patches.py" --apply
  omh doctor
  hermes doctor

  printf '\n[5/5] 게이트웨이 재시작 및 상태 확인\n'
  hermes gateway restart
  hermes gateway status
  hermes --version
  omh --version

  printf '\n완료. Hermes Desktop을 다시 켜세요.\n'
)
```

- `hermes update --backup`은 설정·대화 백업을 만들고, Hermes 본체의 로컬 수정을 stash에 보관한 뒤 새 버전 위에 재적용한다. 재적용 질문에는 사용자가 동의한다. 재적용 충돌이 나면 멈추고 stash를 보존한 채 충돌 파일을 검토한다.
- `apply_local_patches.py --apply`는 각 체크아웃의 릴리스 태그에 맞는 패치(`hermes/patches/<대상>/<태그>.patch`)를 확인한다. `applied`면 수정이 들어 있는 상태이고, `applicable`이면 적용한다. `no_patch`(새 태그용 패치 없음)나 `conflict`가 나오면 블록이 멈춘다. 이때 AI에게 "Agent-setup 수정 묶음을 새 Hermes 버전에 옮겨줘"라고 요청한다. AI는 이전 태그 패치를 새 버전에 맞춰 적용·시험한 뒤 아래 명령으로 새 태그 패치를 저장한다.

  ```bash
  cd ~/.hermes/hermes-agent && cp .git/index "$TMPDIR/idx" && GIT_INDEX_FILE="$TMPDIR/idx" git add -A && GIT_INDEX_FILE="$TMPDIR/idx" git diff --cached --binary HEAD > "$AGENT_SETUP/hermes/patches/hermes-agent/$(git describe --tags --exact-match).patch"
  ```

  provider-usage는 `dashboard/`·`tests/` 경로만 같은 방식으로 저장한다(`desktop/plugin.js`는 `configure_provider_usage.py`가 따로 맞춘다).
- `--keep-stash`는 재적용을 건너뛰고 수정을 stash에 남긴다. 로컬 수정을 새 버전에 맞춰 직접 다시 합칠 때만 쓴다.
- `omh update --channel stable --version <최신>`은 GitHub 최신 정식 릴리스의 wheel로 명령 패키지와 워크플로를 함께 갱신하고 설치 기록을 `stable` 채널로 남긴다. 옵션 없는 `omh update`는 설치 기록의 패키지 주소를 다시 쓰므로, 기록이 main 브랜치 zip이면 preview 빌드를 받는다. `~/.omh/routing/model-chains.json`의 사용자 지정 분류는 유지되고, 기본값을 쓰는 분류는 새 기본 체인을 따른다.
- 갱신 뒤 Agent-setup 루트에서 `python3 scripts/check_releases.py`로 저장소 고정값이 최신 정식 릴리스와 같은지 확인한다. `behind`가 나온 항목은 고정값·사본·문서를 함께 올린다.
- 점검 경고 중 선택 기능(Docker, OpenRouter, image_gen 등)의 `⚠`와 OMH doctor의 `plugin_loader_observed`·`plugin_runtime_observed`는 터미널 점검에서 Hermes 실행을 관측하지 못했다는 표시다. 재시작 후 Desktop 새 세션에서 OMH 도구 호출이 되면 정상이다. `차단` 항목과 실패한 명령은 해결한 뒤 진행한다.

갱신 후 `omh model-chains show --json`으로 12개 분류의 `origin`과 체인을 [라우팅 비교표](../../docs/model-routing-comparison.md)와 대조하고, Hermes 설정의 fallback·스킬 폴더 등록을 확인한다. 소스 호환 패치 두 개는 미리보기로 확인하고 필요한 경우에만 적용한다. Hermes Desktop 새 세션에서 플러그인 로딩, 실제 위임 모델, 계정 선택·사용량 표시를 확인한다.

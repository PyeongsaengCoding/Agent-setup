# 실행기별 모델 라우팅 비교

확인일: 2026-10-20(KST). OMH 설치본 4.0.0, Hermes 0.22.2 기준.

## 적용 대상과 출처

| 구분 | 표의 기준 | 출처 |
|---|---|---|
| Codex | 저장소의 GPT 전용 정책 | [작업 방식](../codex/11-working-method.md), [모델 ID](../codex/config/models.json) |
| Claude Code | 저장소 기본 프리셋 `claude-generous` | [라우팅 원본](../claude/routes/claude-code.json) |
| Hermes 커스텀 OMH | 확인 시점에 실제 적용된 12개 사용자 지정 체인 | 선택한 Hermes 환경의 `omh model-chains show --json` |
| OMH 기본값 | 설치된 OMH 4.0.0 패키지의 기본 체인 | `omh/plugin_bundle/omh/hermes_delegation.py`의 `HERMES_MIXTURE_CATEGORY_CHAINS` |

Codex·Claude Code 열은 설치 원본의 정책을 보여준다. Hermes 커스텀 열은 확인 시점의 적용값을 보여준다. 실제 모델 호출·계정 지원 검증은 실행 기록으로 별도 확인한다. 후보는 왼쪽부터 시도하며 괄호는 행의 모든 후보에 적용되는 추론 강도다.

## 네 가지 구성 비교

| 분류 | Codex | Claude Code · 기본 프리셋 | Hermes 커스텀 OMH · 현재 적용 | OMH 4.0.0 기본값 |
|---|---|---|---|---|
| `ultrabrain` | Astra (`xhigh`) | Astra → Fable → Opus (`xhigh`) | Astra → Opus (`xhigh`) | Astra (`xhigh`) |
| `deep` | Sol (`high`) | Sol → Fable → Opus (`high`) | Opus → Sol (`high`) | Opus → Sol → Kimi K3 (`high`) |
| `architect` | Astra (`xhigh`) | Fable → Astra → Opus (`xhigh`) | Opus → Astra (`xhigh`) | Opus → Astra → Fable → Kimi K3 (`xhigh`) |
| `unspecified-high` | Sol (`medium`) | Opus (`medium`) | Sol → Opus (`medium`) | Sol → Opus → Kimi K3 (`medium`) |
| `unspecified-low` | Luna (`low`) | Opus (`low`) | Sol → Sonnet (`low`) | GLM-5.3 → DeepSeek Flash → Sol → Sonnet (`low`) |
| `quick` | Luna (`low`) | Luna → Fable → Opus → Astra (`low`) | Luna → Opus (`low`) | GLM-5.3 Flash → Luna → Haiku 5.5 → Kimi K3 (`low`) |
| `writing` | Sol (`medium`) | Opus → Sol (`medium`) | Opus → Sonnet → Sol (`medium`) | Opus → Sonnet → Kimi K3 → Gemini 3.1 Pro (`medium`) |
| `visual-engineering` | Sol (`high`) | Fable → Opus → Astra (`high`) | Opus (`high`) | Opus → Fable → Gemini 3.1 Pro → Kimi K3 (`high`) |
| `artistry` | Astra (`high`) | Fable → Opus → Astra (`high`) | Opus (`high`) | Gemini 3.1 Pro → Opus → Fable → Kimi K3 (`high`) |
| `capable` | Sol (`medium`) | Fable → Opus → Sonnet → Astra (`medium`) | Opus → Sol (`medium`) | Opus → Sol → Fable → Kimi K3 (`medium`) |
| `simple-work` | Luna (`low`) | Luna → Fable → Opus → Haiku 4.5 (`low`) | Luna → Haiku 5.5 (`low`) | Luna → Haiku 5.5 → DeepSeek Flash (`low`) |
| `deep-work` | Astra (`high`) | Fable → Opus → Astra (`high`) | Opus → Sol (`max`) | Opus → Sol (`max`) |

## 두 설치 프리셋 비교

각 실행기는 자기 라우팅 원본을 유지한다. 아래 표는 Claude Code의 두 설치 프리셋을 비교한다. Hermes의 두 설치 프리셋은 [기존 라우팅 안내](../hermes/docs/model-routing.md)와 [README](../README.md#hermes--omh-분류별-위임)에서 확인한다.

| 분류 | Claude 넉넉형 · 기본 | GPT 넉넉형 |
|---|---|---|
| `ultrabrain` | Astra → Fable → Opus (`xhigh`) | Astra → Fable → Opus (`xhigh`) |
| `deep` | Sol → Fable → Opus (`high`) | Sol → Fable → Opus (`high`) |
| `architect` | Fable → Astra → Opus (`xhigh`) | Fable → Astra → Opus (`xhigh`) |
| `unspecified-high` | Opus (`medium`) | Opus (`medium`) |
| `unspecified-low` | Opus (`low`) | Opus (`low`) |
| `quick` | Luna → Fable → Opus → Astra (`low`) | Luna → Fable → Opus → Astra (`low`) |
| `writing` | Opus → Sol (`medium`) | Sol → Opus (`medium`) |
| `visual-engineering` | Fable → Opus → Astra (`high`) | Fable → Astra → Opus (`high`) |
| `artistry` | Fable → Opus → Astra (`high`) | Fable → Astra → Opus (`high`) |
| `capable` | Fable → Opus → Sonnet → Astra (`medium`) | Fable → Astra → Opus → Sonnet (`medium`) |
| `simple-work` | Luna → Fable → Opus → Haiku 4.5 (`low`) | Luna → Fable → Opus → Haiku 4.5 (`low`) |
| `deep-work` | Fable → Opus → Astra (`high`) | Astra → Fable → Opus (`high`) |

## Hermes 설치 원본과 현재 적용값 차이

저장소의 `hermes/routing-presets/claude-generous.json`과 현재 적용값 사이에 다음 차이가 있다. 여섯 분류 모두 현재 적용값에서 Fable만 빠졌다. 2026-10-15 사용자 결정(Fable을 대체하고 기본 fallback을 Opus 5.5로 둠)이 실행 환경에만 반영되고 설치 원본에는 반영되지 않은 상태다. 설치 원본을 다시 적용하면 Fable이 되살아나므로, 재적용 전에 설치 원본을 현재 적용값으로 맞춘다.

| 분류 | 저장소 설치 원본 | 현재 적용값 |
|---|---|---|
| `ultrabrain` | Astra → Fable → Opus (`xhigh`) | Astra → Opus (`xhigh`) |
| `architect` | Opus → Astra → Fable (`xhigh`) | Opus → Astra (`xhigh`) |
| `quick` | Luna → Fable → Opus (`low`) | Luna → Opus (`low`) |
| `visual-engineering` | Opus → Fable (`high`) | Opus (`high`) |
| `artistry` | Opus → Fable (`high`) | Opus (`high`) |
| `capable` | Opus → Sol → Fable (`medium`) | Opus → Sol (`medium`) |

## 정확한 모델 ID

| 표 이름 | 모델 ID |
|---|---|
| Astra | `gpt-6-astra` |
| Sol | `gpt-6.1-sol` |
| Luna | `gpt-6-luna` |
| Fable | `claude-fable-5-1` |
| Opus | `claude-opus-5-5` |
| Sonnet | `claude-sonnet-5-5` |
| Haiku 4.5 | `claude-haiku-4-5` |
| Haiku 5.5 | `claude-haiku-5-5` |
| Kimi K3 | `kimi-k3` |
| GLM-5.3 | `glm-5.3` |
| GLM-5.3 Flash | `glm-5.3-flash` |
| DeepSeek Flash | `deepseek-flash` |
| Gemini 3.1 Pro | `gemini-3.1-pro` |

## 업데이트 후 비교 방법

1. `omh --version`과 `hermes --version`으로 버전을 기록한다.
2. `omh model-chains show --json`으로 사용자 지정 체인과 `origin`을 확인한다.
3. 설치된 같은 버전 패키지의 `HERMES_MIXTURE_CATEGORY_CHAINS`를 읽어 기본값과 비교한다.
4. 기존 `model-chains.json`의 명시된 분류는 사용자 체인을 유지하고, 기본값을 따르는 분류는 새 패키지의 체인을 사용한다.
5. 변경은 사용자가 승인한 실행기·분류에 적용한다. 확인 시점의 스냅샷과 설치 프리셋을 각각 갱신한다.

패키지 기본값 출처 SHA256: `d97311befc37815422bdc42a0f4118d129eb0abe763ae5aa1dfd8f28e38192b6`.

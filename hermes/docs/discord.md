# Discord 연동 (선택)

Hermes를 Discord로 쓸 때의 구성이다. Desktop 왼쪽의 프로젝트마다 Discord 채널을 하나씩 두고, 밖에서도 보고를 받고 바로 명령을 내린다. 구성 요소는 `discord/`에 있다.

## 동작

| 상황 | 동작 |
|---|---|
| Discord 프로젝트 채널·스레드에서 명령 | 해당 프로젝트 폴더 기준으로 작업하고 그 스레드에 답한다. Desktop 왼쪽의 같은 프로젝트 아래 채팅으로 보인다 |
| Desktop 채팅에서 턴이 끝남 | 턴마다 결과를 그 프로젝트 채널의 채팅별 스레드로 보낸다. 프로젝트 밖 채팅은 홈 채널로 보낸다 |
| 예약 작업 결과 | 프로젝트 채널의 알림 전용 스레드로 보낸다 (`--deliver discord:<채널>:<스레드>`) |
| 매일 04:30 정리 | 왼쪽 채팅은 프로젝트마다 직접 나눈 대화 최근 4개만 남기고 영구 삭제한다. 30일 넘게 쓰지 않은 대화는 보관된 것까지 삭제한다. 예약 작업·칸반·일회성 실행 기록, `Subagent:` 대화, 빈 대화는 남길 4개에 넣지 않고 마지막 활동 2시간 뒤 삭제한다. Discord 스레드는 3일 넘게 쓰지 않은 것을 삭제하고 채널마다 최근 3개를 남긴다. 고정 채팅, 예약 알림 스레드와 그 대화는 남긴다. 결과는 홈 채널로 보낸다. 기준값 원본은 `shared/retention/policy.json`의 `hermes_desktop_chats`다 |

모든 구성 요소는 모델을 호출하지 않는다. 채널에서 답하는 모델은 선택한 Hermes 프로필의 라우팅을 따른다.

## 구성 요소

| 파일 | 설치 위치 | 역할 |
|---|---|---|
| `discord/plugins/discord-project-sidebar/` | `H/plugins/` | Discord 세션의 작업 폴더를 채널의 프로젝트 폴더로 지정해 Desktop 프로젝트 아래에 표시 |
| `discord/plugins/desktop-discord-reports/` | `H/plugins/` | Desktop 채팅의 작업 결과를 프로젝트 채널의 채팅별 스레드로 전송 (멘션 알림 차단, 2,000자 단위 분할) |
| `discord/scripts/discord-project-hygiene.py` | `H/scripts/` | 매일 정리. `--dry-run`은 미리보기 |

세 구성 요소는 `H/config.yaml`의 `discord.channel_prompts`를 프로젝트 지도로 쓴다. 각 채널 안내문에 `(folder: <프로젝트 절대경로>)`를 넣는다.

## 설정 순서

1. **봇과 서버:** Hermes 공식 Discord 안내로 봇을 만들고 서버에 초대한다. 토큰·허용 사용자·홈 채널은 `H/.env`의 `DISCORD_BOT_TOKEN`, `DISCORD_ALLOWED_USERS`(소유자 ID를 첫 번째로), `DISCORD_HOME_CHANNEL`에 둔다. 봇 역할에 채널 관리, 공개 스레드 만들기, 스레드에서 메시지 보내기, **스레드 및 포스트 관리하기** 권한을 준다. 스레드 삭제에는 마지막 권한이 필요하다.
2. **프로젝트 채널:** `desktop_project list`의 프로젝트마다 텍스트 채널을 만든다. 채널 ID마다 안내문을 등록한다.

   ```sh
   hermes config set "discord.channel_prompts.<채널ID>" "This Discord channel/thread is dedicated to the '<프로젝트>' project (folder: <절대경로>). At the start of a new conversation here, call the desktop_project tool with action=switch and name=<프로젝트> to anchor your working directory to this project before handling the user's request."
   ```

   예약 알림 스레드처럼 멘션 없이 답할 스레드는 `discord.free_response_channels`에 쉼표로 추가한다.
3. **게이트웨이 상시 실행:** `hermes gateway install` 후 `hermes gateway start`. `hermes gateway status`에 launchd 관리가 보이면 Desktop을 닫거나 재부팅해도 봇이 유지된다.
4. **플러그인:** `discord/plugins/`의 두 폴더를 `H/plugins/`에 복사하고 활성화한다.

   ```sh
   hermes plugins enable discord-project-sidebar
   hermes plugins enable desktop-discord-reports
   ```

   플러그인은 실행 중인 프로세스가 시작할 때 한 번 읽힌다. 설치하거나 플러그인 파일을 고친 뒤에는 Desktop 앱을 완전히 종료(⌘Q)했다가 다시 열어 `desktop-discord-reports`를 반영하고, `hermes gateway restart`로 `discord-project-sidebar`를 반영한다.

5. **정리 작업:** 스크립트를 `H/scripts/`에 복사하고 미리보기로 대상 수를 확인한 뒤 예약한다. Python은 Hermes가 쓰는 인터프리터를 지정한다.

   ```sh
   python3 H/scripts/discord-project-hygiene.py --dry-run
   hermes cron create "30 4 * * *" --name "디스코드·왼쪽채팅 정리" \
     --script discord-project-hygiene.py --no-agent \
     --interpreter <Hermes Python> --deliver discord:<홈 채널ID>
   ```

   스크립트는 cron의 기본 Python에 없는 Hermes 패키지를 `H/installs/*/environments/*/venv`에서 찾아 쓴다. Hermes 업데이트 뒤 `ruamel` 가져오기 오류가 나면 이 경로를 확인한다.

   Desktop 채팅 삭제는 되돌릴 수 없다. 처음 적용할 때는 `sqlite3 H/state.db ".backup <백업 경로>"`로 대화 기록을 먼저 백업한다.

## 확인

- 프로젝트 채널에서 새 스레드를 열어 질문하고, 답과 Desktop 프로젝트 아래 표시를 확인한다.
- Desktop 프로젝트 채팅에서 작업을 하나 끝내고 해당 채널에 채팅 제목의 스레드와 결과가 생기는지 확인한다.
- 봇으로 테스트 스레드를 만들고 삭제해 권한을 확인한다.
- 정리 스크립트 `--dry-run` 출력과 첫 정기 실행 보고를 확인한다.

## 알려진 동작

- 보고 스레드에 답하면 Discord 쪽 새 대화로 이어진다. 보고 끝의 Desktop 채팅 ID로 앞선 맥락을 찾는다.
- Desktop 채팅 판별은 `sessions.source`·`created_source`로 한다. Hermes v0.22부터 Desktop 채팅은 `source='local'`·`created_source='desktop'`으로 저장되므로, 플러그인은 cron·kanban·subagent·메신저 등 Desktop 밖 출처를 제외하는 방식으로 판별한다.
- 보고가 오지 않으면 `H/state/desktop-discord-threads.json`에 해당 채팅이 있는지, Desktop 백엔드 시작 시각(`ps -eo lstart,command | grep hermes`)이 플러그인 파일 수정 시각보다 뒤인지 확인한다.
- 삭제된 보고 스레드는 다음 보고 때 새로 만든다. 채팅과 스레드의 대응은 `H/state/desktop-discord-threads.json`에 둔다.

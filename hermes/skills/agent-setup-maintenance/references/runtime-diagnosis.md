# Hermes 런타임 이상 추적

## macOS 권한 팝업이 갑자기 뜰 때 (osascript·python 등)

1. 원인 프로세스를 TCC 로그에서 찾는다.
   `log show --last 30m --style compact --predicate 'subsystem == "com.apple.TCC"' | grep -E 'AUTHREQ_ATTRIBUTION|Prompting|AUTHREQ_RESULT'`
   `AUTHREQ_ATTRIBUTION`의 `responsible`는 팝업에 표시되는 이름이고, `accessing`의 binary_path와 pid가 실제로 파일에 접근한 프로세스다.
2. `ps -o pid,ppid,lstart,command -p <responsible>,<accessing>`로 둘을 확인한다. 게이트웨이는 launchd 아래에서 `osascript -l JavaScript ... hermes gateway run` 래퍼로 실행된다. 그래서 게이트웨이가 띄운 하위 작업(칸반 작업자, cron, `find` 같은 셸 명령)이 보호 폴더에 접근하면 팝업에는 osascript가 요청한 것으로 나온다.
3. 흔한 원인은 작업자가 `find /`처럼 디스크 전체를 훑어 iCloud Drive나 다른 앱 데이터(`kTCCServiceFileProviderDomain`, `kTCCServiceSystemPolicyAppData`)를 건드리는 경우다. 해당 프로세스를 종료하면 새 팝업이 더 생기지 않는다. 권한은 허용하지 않고, 작업 범위를 작업 폴더로 좁힌다. osascript에 전체 디스크 접근 권한을 주면 osascript를 거치는 모든 스크립트가 같은 권한을 얻게 되므로 권하지 않는다.
4. 열린 팝업은 화면 캡처 도구로 확인한다. 사용자 TCC.db는 전체 디스크 접근 권한 없이 읽을 수 없다. 저장된 결정은 사용자가 시스템 설정 → 개인정보 보호 및 보안에서 확인하도록 안내하고, 로그의 `authValue`(0=거부, 2=허용)로 확인한 범위만 보고한다.

## `hermes update` 뒤 플러그인·기능이 깨질 때

`hermes update`는 hermes-agent 체크아웃의 로컬 수정을 `hermes-update-autostash-<시각>` stash로 치우고 고정 커밋으로 detached checkout한다. 본체에 직접 넣은 수정(새 모듈 포함)이 사라지므로, 그 모듈을 import하는 사용자 플러그인이 500을 내고 Desktop 상태바에는 `backend down` 같은 표시만 남는다. 로컬 본체 수정이 있는 한 업데이트마다 반복된다.

1. `$HERMES_HOME/logs/desktop.log`에서 `/api/plugins/<이름>/` 500을 찾고, 플러그인 폴더의 `git diff`로 본체 모듈 import를 확인한다.
2. `cd $HERMES_HOME/hermes-agent && git stash list`, `git stash show --include-untracked --stat stash@{0}`로 치워진 수정을 확인한다.
3. `git worktree add --detach <scratch> HEAD`에서 먼저 `git stash apply`로 충돌을 확인한 뒤 실제 트리에 `git stash apply`(pop 대신 apply로 stash 보존)한다. worktree에서 돌린 시험은 `home_io_guard`가 `.git/worktrees/...` 경로를 실제 홈으로 잡아 가짜 실패를 낼 수 있으니 그 실패는 분리해 보고한다.
4. 플러그인의 선택적 본체 import는 `try/except ImportError`로 감싸 기본 동작으로 떨어지게 한다. 다음 업데이트에서 기능 일부만 빠지고 플러그인 전체가 죽지 않는다.
5. 플러그인 코드는 Hermes 런타임으로 직접 실행해 확인한다. 런처가 `-I`로 PYTHONPATH를 지우므로 임시 모듈을 `$HERMES_HOME/hermes-agent/_probe_tmp.py`에 두고 `hermes --run-module _probe_tmp`로 실행한 뒤 즉시 지운다.
6. 반영에는 재시작이 필요하다. 게이트웨이가 띄운 세션 안에서는 `hermes gateway restart`가 차단되므로 사용자에게 별도 터미널 실행을 요청하고, 플러그인 API는 Desktop 앱 완전 종료·재실행으로 다시 읽힌다. 반복을 막으려면 로컬 수정을 별도 브랜치나 플러그인으로 옮기는 선택지를 제시한다.

## 백그라운드 작업이 어디서 지시됐는지 찾기

1. 작업 ID로 보드를 찾는다. `hermes kanban show <id>`가 "no such task"를 반환하면 다른 보드에 있는 작업이다. `grep -rl <id> $HERMES_HOME/kanban/boards`로 보드를 찾은 뒤 `hermes kanban --board <slug> show <id>`로 생성 시각·생성자·본문을 본다.
2. 이 작업을 만든 채팅을 `$HERMES_HOME/state.db`에서 찾는다.
   `select s.id,s.title,s.source,datetime(s.started_at,'unixepoch','localtime') from sessions s where s.id in (select distinct session_id from messages where content like '%<id>%' or content like '%<카드 제목>%')`
   `source='kanban'` 세션은 작업자 실행이고, `desktop`·`discord` 세션이 작업을 만든 채팅이다. 생성 시각 직전의 user 메시지를 조회하면 어느 지시에서 나온 작업인지 알 수 있다.
3. 사용자에게는 채팅 제목, 보드 이름, 생성 시각과 직전 지시, 그리고 사용자가 직접 만든 작업인지 에이전트가 작업을 나눠 만든 것인지(`created_by`)를 보고한다.

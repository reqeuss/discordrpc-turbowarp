# TurboWarp용 Discord Rich Presence

사용자 지정 확장 프로그램과 로컬 bridge를 통해 TurboWarp 게임에 Discord Rich Presence를 추가합니다.

**중요:** 게임을 내보내거나 컴파일하기 전에 개발 중인 TurboWarp 프로젝트에 확장 프로그램을 포함해야 합니다. 확장 프로그램 없이 이미 내보낸 게임에 RPC를 자동으로 삽입할 수는 없습니다.

[Français](README.fr.md) · [English](README.en.md) · [Español](README.es.md) · [日本語](README.ja.md) · [简体中文](README.zh-CN.md) · [繁體中文](README.zh-TW.md) · [한국어](README.ko.md) · [Deutsch](README.de.md) · [Português](README.pt-BR.md) · [Русский](README.ru.md) · [العربية](README.ar.md) · [हिन्दी](README.hi.md) · [Italiano](README.it.md)

## 기능
- Discord 활동의 세부 정보, 상태, 시작/종료 시각을 사용자 지정합니다.
- Discord 이미지 에셋, 파티 정보, Join/Spectate secret 및 인스턴스 플래그를 지원합니다.
- bridge 연결이 끊기면 자동으로 다시 연결합니다.
- `127.0.0.1:32123` 로컬 WebSocket을 사용합니다.
- Windows에서 `game.bat`으로 실행합니다.
- 컴파일된 `rpc_bridge.exe`를 사용하면 플레이어 PC에 Python을 설치할 필요가 없습니다.

## 설치 및 설정
1. 개발 중 `extension.js`를 TurboWarp 사용자 지정 **unsandboxed** 확장 프로그램으로 불러오고 프로젝트에서 블록을 사용합니다.
2. 확장 프로그램이 포함된 상태로 게임을 내보내거나 컴파일합니다.
3. [Discord Developer Portal](https://discord.com/developers/applications)에서 앱을 만들고 Application ID를 복사합니다.
4. `resources/rpc/rpc_bridge.py`에서 `APP_ID`를 설정합니다. bot token이나 client secret은 입력하지 마세요.
5. `ingame/` 폴더의 내용을 게임 실행 파일 옆에 복사합니다.
**중요:** `resources/rpc/rpc_bridge.py`를 열고 `GAME_EXE`의 `testdiscordrpc.exe`를 게임 폴더의 루트(`game.bat`와 같은 위치)에 있는 컴파일된 게임 실행 파일의 정확한 이름으로 바꾸세요. `.exe` 확장자와 따옴표는 유지하세요. 예를 들어 파일명이 `MyGame.exe`라면 `GAME_EXE = GAME_DIR / "MyGame.exe"`로 설정합니다.

먼저 `resources/rpc/rpc_bridge.exe`를 찾고, 없으면 Python 3를 찾아 최초 실행 시 의존성을 설치합니다. 컴파일된 bridge를 배포하려면 빌드 전에 Application ID를 설정하세요. Discord 데스크톱 앱이 실행 중이고 로그인되어 있어야 합니다.

## 확장 프로그램 블록
- **set [field] to [value]** — 활동 필드를 설정합니다.
- **update presence** — Discord로 활동 정보를 보냅니다.
- **clear presence** — 활동을 지웁니다.
- **reconnect to bridge** — 다시 연결합니다.
- **RPC connection status** — 연결 상태와 마지막 오류를 확인합니다.
- **current value of [field]** — 현재 필드 값을 읽습니다.

타임스탬프는 밀리초가 아닌 Unix 초를 사용합니다. 이미지 필드에는 이미지 URL이 아니라 Discord Developer Portal의 에셋 키를 사용합니다.

## 문제 해결
- 연결되지 않으면 bridge 실행 여부와 확장 프로그램의 unsandboxed 설정을 확인하세요.
- 활동이 표시되지 않으면 Discord 데스크톱 앱과 Application ID를 확인하세요.
- 이미지가 표시되지 않으면 Rich Presence 에셋 키를 확인하세요.
- 브라우저에서 `http://127.0.0.1:32123/`를 여는 것은 유효한 테스트가 아닙니다. 해당 주소는 WebSocket 연결용입니다.

## 크레딧 및 사용
이 프로젝트를 게임이나 다른 프로젝트에서 사용, 재배포 또는 수정하는 경우 **Reqeuss를 크레딧에 표시하고 저장소 링크를 포함해 주세요**.

> [Discord RPC for TurboWarp](https://github.com/reqeuss/discordrpc-turbowarp) by Reqeuss

수정본을 재배포할 때도 크레딧을 유지해 주세요. 이 요청은 적용되는 제3자 라이선스 조건을 대체하지 않습니다.

## 보안
bridge는 로컬 컴퓨터의 `127.0.0.1`에서만 수신 대기합니다. 위험을 이해하지 못한다면 다른 기기에 공개하지 마세요.

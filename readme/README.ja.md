# TurboWarp 向け Discord Rich Presence

カスタム拡張機能とローカルブリッジを使って、TurboWarp ゲームに Discord Rich Presence を追加します。

**重要：** ゲームをエクスポートまたはコンパイルする前に、開発中の TurboWarp プロジェクトへ拡張機能を組み込む必要があります。拡張機能なしで既に出力されたゲームへ、後から RPC を自動追加することはできません。

[Français](README.fr.md) · [English](README.en.md) · [Español](README.es.md) · [日本語](README.ja.md) · [简体中文](README.zh-CN.md) · [繁體中文](README.zh-TW.md) · [한국어](README.ko.md) · [Deutsch](README.de.md) · [Português](README.pt-BR.md) · [Русский](README.ru.md) · [العربية](README.ar.md) · [हिन्दी](README.hi.md) · [Italiano](README.it.md)

## 機能
- Discord のアクティビティ詳細、状態、開始・終了時刻を設定できます。
- Discord アセット画像、パーティー情報、Join/Spectate シークレット、インスタンス状態に対応します。
- ブリッジが一時的に切断されても自動で再接続します。
- `127.0.0.1:32123` のローカル WebSocket を使用します。
- Windows では `game.bat` から起動できます。
- コンパイル済み `rpc_bridge.exe` を使えば、プレイヤー側に Python を要求せずに配布できます。

## セットアップ

1. 開発中に `extension.js` を TurboWarp のカスタム **unsandboxed** 拡張機能として読み込み、ブロックをプロジェクトで使用します。
2. 拡張機能を含めた状態でゲームをエクスポートまたはコンパイルします。
3. [Discord Developer Portal](https://discord.com/developers/applications) でアプリケーションを作成し、Application ID を取得します。
4. `resources/rpc/rpc_bridge.py` の `APP_ID` を自分の数値 ID に変更します。Bot token や client secret は記入しないでください。
5. `ingame/` の中身をゲームの実行ファイルと同じフォルダーへコピーします。
**重要：** `resources/rpc/rpc_bridge.py` を開き、`GAME_EXE` の `testdiscordrpc.exe` を、ゲームフォルダーのルート（`game.bat` と同じ場所）にあるコンパイル済みゲーム実行ファイルの正確な名前に置き換えてください。`.exe` 拡張子と引用符はそのままにします。例：`MyGame.exe` の場合は `GAME_EXE = GAME_DIR / "MyGame.exe"` とします。

ブリッジは最初に `resources/rpc/rpc_bridge.exe` を探します。存在しない場合は Python 3 を探し、初回起動時に依存関係をインストールします。コンパイル済みブリッジを配布する場合は、ビルド前に Application ID を設定してください。Discord デスクトップアプリへのログインも必要です。

## 拡張機能のブロック
- **set [field] to [value]** — アクティビティの項目を設定します。
- **update presence** — Discord に送信します。
- **clear presence** — アクティビティを消去します。
- **reconnect to bridge** — 再接続します。
- **RPC connection status** — 接続状態と直近のエラーを確認します。
- **current value of [field]** — 現在の項目値を取得します。

時刻はミリ秒ではなく Unix 秒です。画像には URL ではなく Discord Developer Portal で設定したアセットキーを使用します。

## トラブルシューティング
- 接続できない場合、ブリッジが起動していること、拡張機能が unsandboxed で読み込まれていることを確認してください。
- 表示されない場合、Discord デスクトップアプリと Application ID を確認してください。
- 画像が表示されない場合、アセットキーを確認してください。
- `http://127.0.0.1:32123/` をブラウザーで開いても正常性確認にはなりません。ここは WebSocket エンドポイントです。

## クレジット
このプロジェクトをゲームなどで使用、再配布、改変する場合は、**Reqeuss のクレジットとリポジトリへのリンク**を記載してください。

> [Discord RPC for TurboWarp](https://github.com/reqeuss/discordrpc-turbowarp) by Reqeuss

改変版を再配布する場合もクレジットを残してください。これは、適用される第三者ライセンスの条件に代わるものではありません。

## セキュリティ
ブリッジはローカルマシンの `127.0.0.1` のみで待ち受けます。リスクを理解せずに外部ネットワークへ公開しないでください。

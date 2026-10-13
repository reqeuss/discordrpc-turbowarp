# TurboWarp 的 Discord Rich Presence

透過自訂擴充功能與本機 bridge，為 TurboWarp 遊戲加入 Discord Rich Presence。

**重要：** 必須在開發期間、匯出或編譯遊戲之前，將擴充功能整合進 TurboWarp 專案。本專案無法將 RPC 自動注入已匯出且未包含擴充功能的遊戲。

[Français](README.fr.md) · [English](README.en.md) · [Español](README.es.md) · [日本語](README.ja.md) · [简体中文](README.zh-CN.md) · [繁體中文](README.zh-TW.md) · [한국어](README.ko.md) · [Deutsch](README.de.md) · [Português](README.pt-BR.md) · [Русский](README.ru.md) · [العربية](README.ar.md) · [हिन्दी](README.hi.md) · [Italiano](README.it.md)

## 功能
- 自訂 Discord 活動詳細資訊、狀態與起訖時間。
- 支援 Discord 圖片資源、派對資訊、Join/Spectate secrets 與執行個體標記。
- bridge 暫時中斷時會自動重新連線。
- 使用 `127.0.0.1:32123` 本機 WebSocket。
- Windows 可透過 `game.bat` 啟動。
- 可使用編譯版 `rpc_bridge.exe`，避免要求玩家安裝 Python。

## 安裝與設定
1. 開發期間將 `extension.js` 以 TurboWarp 自訂 **unsandboxed** 擴充功能載入，並在專案中使用其積木。
2. 確認擴充功能已整合，再匯出或編譯遊戲。
3. 在 [Discord Developer Portal](https://discord.com/developers/applications) 建立應用程式並複製 Application ID。
4. 在 `resources/rpc/rpc_bridge.py` 設定 `APP_ID`。請勿填入 bot token 或 client secret。
5. 將 `ingame/` 內的內容複製到遊戲執行檔旁邊。
**重要：** 開啟 `resources/rpc/rpc_bridge.py`，將 `GAME_EXE` 中的 `testdiscordrpc.exe` 替換成遊戲資料夾根目錄（與 `game.bat` 同一層）中已編譯遊戲執行檔的正確檔名。保留 `.exe` 副檔名與引號。例如檔名為 `MyGame.exe`，請設定 `GAME_EXE = GAME_DIR / "MyGame.exe"`。

程式會先尋找 `resources/rpc/rpc_bridge.exe`。若不存在，便嘗試使用 Python 3，並在首次啟動時安裝相依套件。若要發佈編譯版 bridge，請在編譯前設定 Application ID。玩家必須開啟並登入 Discord 桌面版。

## 擴充功能積木
- **set [field] to [value]** — 設定活動欄位。
- **update presence** — 傳送活動到 Discord。
- **clear presence** — 清除活動。
- **reconnect to bridge** — 重新連線。
- **RPC connection status** — 查看連線狀態與最近錯誤。
- **current value of [field]** — 讀取欄位目前值。

時間戳使用 Unix 秒，不是毫秒。圖片欄位使用 Discord Developer Portal 設定的資源鍵，不是圖片網址。

## 疑難排解
- 無法連線：確認 bridge 正在執行，且擴充功能以 unsandboxed 模式載入。
- 活動沒有顯示：確認 Discord 桌面版正在執行且 Application ID 正確。
- 圖片沒有顯示：檢查 Rich Presence 資源鍵。
- 在瀏覽器開啟 `http://127.0.0.1:32123/` 不是有效測試；該端點使用 WebSocket。

## 使用與署名
若在遊戲或其他專案中使用、重新散布或修改本專案，**請標示 Reqeuss 並連結至此儲存庫**：

> [Discord RPC for TurboWarp](https://github.com/reqeuss/discordrpc-turbowarp) by Reqeuss

重新散布修改版本時也請保留署名。本署名請求不取代任何適用的第三方授權條款。

## 安全性
bridge 僅監聽本機位址 `127.0.0.1`。除非了解相關風險，否則請勿將它公開給其他裝置。

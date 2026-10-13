# TurboWarp 的 Discord Rich Presence

通过自定义扩展和本地 bridge，为 TurboWarp 游戏添加 Discord Rich Presence。

**重要：** 必须在开发阶段、导出或编译游戏之前，将扩展集成到 TurboWarp 项目中。对于未集成扩展且已经导出的游戏，本项目无法自动注入 RPC。

[Français](README.fr.md) · [English](README.en.md) · [Español](README.es.md) · [日本語](README.ja.md) · [简体中文](README.zh-CN.md) · [繁體中文](README.zh-TW.md) · [한국어](README.ko.md) · [Deutsch](README.de.md) · [Português](README.pt-BR.md) · [Русский](README.ru.md) · [العربية](README.ar.md) · [हिन्दी](README.hi.md) · [Italiano](README.it.md)

## 功能
- 自定义 Discord 活动详情、状态和起止时间。
- 支持 Discord 资源图片、派对信息、Join/Spectate secrets 和实例标记。
- bridge 暂时断开时自动重连。
- 使用 `127.0.0.1:32123` 本地 WebSocket。
- Windows 下通过 `game.bat` 启动。
- 可使用编译好的 `rpc_bridge.exe`，避免要求玩家安装 Python。

## 安装与配置
1. 开发时将 `extension.js` 作为 TurboWarp 自定义 **unsandboxed** 扩展加载，并在项目中使用其积木。
2. 确保扩展已集成，再导出或编译游戏。
3. 在 [Discord Developer Portal](https://discord.com/developers/applications) 创建应用并复制 Application ID。
4. 在 `resources/rpc/rpc_bridge.py` 中设置 `APP_ID`。不要填写 bot token 或 client secret。
5. 将 `ingame/` 文件夹中的内容复制到游戏可执行文件旁边。
**重要：** 打开 `resources/rpc/rpc_bridge.py`，将 `GAME_EXE` 中的 `testdiscordrpc.exe` 替换为游戏文件夹根目录（与 `game.bat` 同一目录）中已编译游戏可执行文件的准确文件名。保留 `.exe` 扩展名和引号。例如，文件名为 `MyGame.exe` 时，设置为 `GAME_EXE = GAME_DIR / "MyGame.exe"`。

启动时会优先查找 `resources/rpc/rpc_bridge.exe`；如果不存在，则尝试使用 Python 3，并在首次启动时安装依赖。若要分发编译版 bridge，请在编译前配置 Application ID。玩家需要运行并登录 Discord 桌面版。

## 扩展积木
- **set [field] to [value]** — 设置活动字段。
- **update presence** — 发送活动到 Discord。
- **clear presence** — 清除活动。
- **reconnect to bridge** — 重新连接。
- **RPC connection status** — 查看连接状态和最近错误。
- **current value of [field]** — 读取字段当前值。

时间戳使用 Unix 秒，而不是毫秒。图片字段使用 Discord Developer Portal 中配置的资源键，不是图片 URL。

## 故障排除
- 无法连接：确认 bridge 正在运行，并且扩展以 unsandboxed 模式加载。
- 活动不显示：检查 Discord 桌面版是否运行，以及 Application ID 是否正确。
- 图片不显示：检查 Rich Presence 资源键。
- 在浏览器打开 `http://127.0.0.1:32123/` 不是有效测试；该地址使用 WebSocket 协议。

## 使用与署名
如果你在游戏或其他项目中使用、再发布或修改本项目，**请注明 Reqeuss 并链接到此仓库**：

> [Discord RPC for TurboWarp](https://github.com/reqeuss/discordrpc-turbowarp) by Reqeuss

再发布修改版时也请保留署名。本署名请求不取代任何适用的第三方许可证条款。

## 安全
bridge 仅监听本机地址 `127.0.0.1`。除非了解风险，否则不要将其暴露给其他设备。

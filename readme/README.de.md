# Discord Rich Presence für TurboWarp

Füge Discord Rich Presence mithilfe einer benutzerdefinierten Erweiterung und einer lokalen Bridge zu einem TurboWarp-Spiel hinzu.

**Wichtig:** Die Erweiterung muss während der Entwicklung in das TurboWarp-Projekt integriert werden, **bevor das Spiel exportiert oder kompiliert wird**. RPC lässt sich mit diesem Projekt nicht nachträglich automatisch in ein bereits exportiertes Spiel ohne Erweiterung einfügen.

[Français](README.fr.md) · [English](README.en.md) · [Español](README.es.md) · [日本語](README.ja.md) · [简体中文](README.zh-CN.md) · [繁體中文](README.zh-TW.md) · [한국어](README.ko.md) · [Deutsch](README.de.md) · [Português](README.pt-BR.md) · [Русский](README.ru.md) · [العربية](README.ar.md) · [हिन्दी](README.hi.md) · [Italiano](README.it.md)

## Funktionen
- Benutzerdefinierte Aktivitätsdetails, Status und Zeitstempel.
- Discord-Bild-Assets, Party-Informationen, Join-/Spectate-Secrets und Instanzstatus.
- Automatische Wiederverbindung mit der Bridge.
- Lokale WebSocket-Verbindung unter `127.0.0.1:32123`.
- Start unter Windows über `game.bat`.
- Eine kompilierte `rpc_bridge.exe` ist optional, damit Spieler kein Python installieren müssen.

## Installation
1. Lade `extension.js` während der Entwicklung als benutzerdefinierte **unsandboxed** Erweiterung in TurboWarp und verwende ihre Blöcke im Projekt.
2. Exportiere oder kompiliere das Spiel mit integrierter Erweiterung.
3. Erstelle eine Anwendung im [Discord Developer Portal](https://discord.com/developers/applications) und kopiere die Application ID.
4. Trage deine numerische ID in `APP_ID` in `resources/rpc/rpc_bridge.py` ein. Niemals Bot-Token oder Client-Secret eintragen.
5. Kopiere den **Inhalt** von `ingame/` neben die Spieldatei.
**Wichtig:** Öffne `resources/rpc/rpc_bridge.py` und ersetze `testdiscordrpc.exe` in `GAME_EXE` durch den exakten Namen der kompilierten Spieldatei im Stammordner des Spiels (neben `game.bat`). Behalte die Erweiterung `.exe` und die Anführungszeichen bei. Bei `MyGame.exe` lautet die Zeile beispielsweise `GAME_EXE = GAME_DIR / "MyGame.exe"`.

Zuerst wird `resources/rpc/rpc_bridge.exe` gesucht. Fehlt sie, wird Python 3 gesucht und beim ersten Start werden Abhängigkeiten installiert. Konfiguriere die Application ID vor dem Kompilieren einer Bridge. Die Discord-Desktop-App muss geöffnet und angemeldet sein.

## Erweiterungsblöcke
- **set [field] to [value]** — Aktivitätsfeld festlegen.
- **update presence** — Aktivität an Discord senden.
- **clear presence** — Aktivität löschen.
- **reconnect to bridge** — Verbindung erneut herstellen.
- **RPC connection status** — Verbindungsstatus und letzten Fehler anzeigen.
- **current value of [field]** — aktuellen Feldwert auslesen.

Zeitstempel verwenden Unix-Sekunden, keine Millisekunden. Bildfelder benötigen Asset-Schlüssel aus dem Discord Developer Portal, keine Bild-URLs.

## Fehlerbehebung
- Keine Verbindung: Prüfe, ob die Bridge läuft und die Erweiterung unsandboxed geladen wurde.
- Keine Aktivität: Prüfe Discord Desktop und die Application ID.
- Fehlende Bilder: Prüfe die Rich-Presence-Asset-Schlüssel.
- `http://127.0.0.1:32123/` im Browser aufzurufen ist kein gültiger Test; der Endpunkt erwartet WebSocket-Verbindungen.

## Namensnennung
Wenn du dieses Projekt in einem Spiel oder anderen Projekt verwendest, weiterverbreitest oder anpasst, **nenne bitte Reqeuss als Urheber und verlinke dieses Repository**:

> [Discord RPC for TurboWarp](https://github.com/reqeuss/discordrpc-turbowarp) by Reqeuss

Behalte den Hinweis auch bei der Weitergabe veränderter Versionen bei. Diese Bitte ersetzt keine anwendbaren Lizenzbedingungen Dritter.

## Sicherheit
Die Bridge lauscht nur lokal unter `127.0.0.1`. Gib sie nicht für andere Geräte frei, wenn du die Risiken nicht verstehst.

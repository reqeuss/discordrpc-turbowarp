# Discord Rich Presence per TurboWarp

Aggiungi Discord Rich Presence a un gioco TurboWarp tramite un'estensione personalizzata e un bridge locale.

**Importante:** l'estensione deve essere integrata nel progetto TurboWarp durante lo sviluppo, **prima di esportare o compilare il gioco**. Questo progetto non può inserire automaticamente RPC in un gioco già esportato senza l'estensione.

[Français](README.fr.md) · [English](README.en.md) · [Español](README.es.md) · [日本語](README.ja.md) · [简体中文](README.zh-CN.md) · [繁體中文](README.zh-TW.md) · [한국어](README.ko.md) · [Deutsch](README.de.md) · [Português](README.pt-BR.md) · [Русский](README.ru.md) · [العربية](README.ar.md) · [हिन्दी](README.hi.md) · [Italiano](README.it.md)

## Funzionalità
- Dettagli, stato e orari personalizzati nell'attività Discord.
- Supporto per immagini Discord, informazioni sul gruppo, secret Join/Spectate e flag dell'istanza.
- Riconnessione automatica al bridge.
- WebSocket locale su `127.0.0.1:32123`.
- Avvio su Windows tramite `game.bat`.
- Bridge compilato opzionale per non richiedere Python sul PC del giocatore.

## Installazione
1. Durante lo sviluppo, carica `extension.js` in TurboWarp come estensione personalizzata **unsandboxed** e usa i suoi blocchi nel progetto.
2. Esporta o compila il gioco includendo l'estensione.
3. Crea o seleziona un'app nel [Discord Developer Portal](https://discord.com/developers/applications) e copia l'Application ID.
4. Imposta il tuo ID numerico in `APP_ID` in `resources/rpc/rpc_bridge.py`. Non inserire bot token o client secret.
5. Copia il contenuto di `ingame/` accanto all'eseguibile del gioco.
6. Su Windows, avvia `game.bat`. Per impostazione predefinita il bridge cerca `testdiscordrpc.exe`; se il nome è diverso, modifica `GAME_EXE`.

Lo script cerca prima `resources/rpc/rpc_bridge.exe`. Se non è presente, cerca Python 3 e installa le dipendenze al primo avvio. Configura l'Application ID prima di compilare il bridge. Discord Desktop deve essere aperto e connesso.

## Blocchi dell'estensione
- **set [field] to [value]** — imposta un campo dell'attività.
- **update presence** — invia l'attività a Discord.
- **clear presence** — cancella l'attività.
- **reconnect to bridge** — tenta di riconnettersi.
- **RPC connection status** — mostra lo stato della connessione e l'ultimo errore.
- **current value of [field]** — legge il valore corrente di un campo.

I timestamp usano i secondi Unix, non i millisecondi. I campi immagine richiedono le chiavi degli asset di Discord Developer Portal, non URL di immagini.

## Risoluzione dei problemi
- Nessuna connessione: verifica che il bridge sia in esecuzione e che l'estensione sia caricata come unsandboxed.
- Nessuna attività: controlla Discord Desktop e l'Application ID.
- Immagini assenti: controlla le chiavi degli asset Rich Presence.
- Aprire `http://127.0.0.1:32123/` nel browser non è un test valido: l'endpoint usa WebSocket.

## Crediti e utilizzo
Se usi, redistribuisci o modifichi questo progetto in un gioco o in un altro progetto, **attribuisci il credito a Reqeuss e inserisci un link a questo repository**:

> [Discord RPC for TurboWarp](https://github.com/reqeuss/discordrpc-turbowarp) by Reqeuss

Mantieni il credito anche quando redistribuisci versioni modificate. Questa richiesta non sostituisce i termini delle licenze di terze parti applicabili.

## Sicurezza
Il bridge ascolta solo su `127.0.0.1`, cioè sulla macchina locale. Non esporlo ad altri dispositivi senza comprenderne i rischi.

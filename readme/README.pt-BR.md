# Discord Rich Presence para TurboWarp

Adicione Discord Rich Presence a um jogo TurboWarp usando uma extensão personalizada e uma bridge local.

**Importante:** a extensão precisa ser integrada ao projeto TurboWarp durante o desenvolvimento, **antes de exportar ou compilar o jogo**. Este projeto não injeta RPC automaticamente em um jogo já exportado sem a extensão.

[Français](README.fr.md) · [English](README.en.md) · [Español](README.es.md) · [日本語](README.ja.md) · [简体中文](README.zh-CN.md) · [繁體中文](README.zh-TW.md) · [한국어](README.ko.md) · [Deutsch](README.de.md) · [Português](README.pt-BR.md) · [Русский](README.ru.md) · [العربية](README.ar.md) · [हिन्दी](README.hi.md) · [Italiano](README.it.md)

## Recursos
- Detalhes, estado e horários personalizados na atividade do Discord.
- Suporte a imagens, informações de grupo, secrets Join/Spectate e indicador de instância.
- Reconexão automática com a bridge.
- WebSocket local em `127.0.0.1:32123`.
- Inicialização no Windows por `game.bat`.
- Bridge compilada opcional para não exigir Python no computador do jogador.

## Instalação
1. Durante o desenvolvimento, carregue `extension.js` no TurboWarp como extensão personalizada **unsandboxed** e use seus blocos no projeto.
2. Exporte ou compile o jogo com a extensão incluída.
3. Crie ou selecione um aplicativo no [Discord Developer Portal](https://discord.com/developers/applications) e copie o Application ID.
4. Defina `APP_ID` em `resources/rpc/rpc_bridge.py` com seu ID numérico. Não inclua bot token nem client secret.
5. Copie o conteúdo de `ingame/` para a pasta do executável do jogo.
6. No Windows, execute `game.bat`. A bridge procura `testdiscordrpc.exe` por padrão; altere `GAME_EXE` se o nome for diferente.

O script procura primeiro `resources/rpc/rpc_bridge.exe`. Se não existir, procura Python 3 e instala as dependências na primeira execução. Configure o Application ID antes de compilar a bridge. O aplicativo Discord para desktop precisa estar aberto e conectado.

## Blocos da extensão
- **set [field] to [value]** — define um campo da atividade.
- **update presence** — envia os dados ao Discord.
- **clear presence** — limpa a atividade.
- **reconnect to bridge** — tenta reconectar.
- **RPC connection status** — mostra o estado da conexão e o último erro.
- **current value of [field]** — lê o valor atual do campo.

Os horários usam segundos Unix, não milissegundos. Os campos de imagem usam chaves de assets configuradas no Discord Developer Portal, não URLs de imagens.

## Solução de problemas
- Sem conexão: confirme que a bridge está ativa e que a extensão foi carregada como unsandboxed.
- Sem atividade: verifique o Discord Desktop e o Application ID.
- Sem imagens: confira as chaves dos assets Rich Presence.
- Abrir `http://127.0.0.1:32123/` no navegador não é um teste válido; o endpoint espera WebSocket.

## Créditos e uso
Se usar, redistribuir ou adaptar este projeto em um jogo ou outro projeto, **dê crédito a Reqeuss e inclua um link para este repositório**:

> [Discord RPC for TurboWarp](https://github.com/reqeuss/discordrpc-turbowarp) by Reqeuss

Mantenha os créditos ao redistribuir versões modificadas. Este pedido não substitui os termos de licenças de terceiros aplicáveis.

## Segurança
A bridge escuta apenas em `127.0.0.1`, na máquina local. Não a exponha a outros dispositivos sem entender os riscos.

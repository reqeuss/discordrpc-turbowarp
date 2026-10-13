# Discord Rich Presence para TurboWarp

Añade Discord Rich Presence a un juego de TurboWarp mediante una extensión personalizada y un bridge local.

**Importante:** la extensión debe integrarse en el proyecto de TurboWarp durante el desarrollo, **antes de exportar o compilar el juego**. Este proyecto no puede inyectar RPC en un juego ya exportado que no incluya la extensión.

[🇫🇷 Français](README.fr.md) · [🇬🇧 English](README.en.md) · [🇪🇸 Español](README.es.md)

## Funciones

- Detalles y estado personalizados en la actividad de Discord.
- Marcas de tiempo de inicio y finalización.
- Imágenes de Discord, información del grupo, secretos Join/Spectate e indicador de instancia.
- Reconexión automática al bridge.
- Comunicación WebSocket local en `127.0.0.1:32123`.
- Inicio en Windows mediante `game.bat`.
- Bridge compilado opcional para no exigir Python en el PC del jugador.

## Cómo funciona

1. Durante el desarrollo, carga `extension.js` en TurboWarp como extensión personalizada **unsandboxed**.
2. Usa los bloques de la extensión en el proyecto.
3. Exporta o compila el juego con la extensión incluida.
4. Configura el Application ID de Discord en el bridge.
5. Copia el contenido de `ingame/` junto al ejecutable del juego.
6. Inicia el juego con `game.bat`.

Si el juego se exportó sin la extensión, añadir los archivos del bridge después no es suficiente.

## Instalación

### 1. Integrar la extensión antes de exportar

Añade `extension.js` a TurboWarp como extensión personalizada **unsandboxed**. Configura los campos con sus bloques y ejecuta **update presence**. La extensión debe estar incluida antes de exportar o compilar el proyecto.

### 2. Configurar Discord

En el [Discord Developer Portal](https://discord.com/developers/applications), crea o selecciona una aplicación y copia el **Application ID** desde General Information.

En `resources/rpc/rpc_bridge.py`, sustituye:

```python
APP_ID = "YOUR_DISCORD_APPLICATION_ID"
```

Usa tu Application ID numérico. Para mostrar imágenes, configura los recursos Rich Presence en la aplicación de Discord y utiliza sus claves. **No incluyas un token de bot ni un client secret.**

Si distribuyes `rpc_bridge.exe`, configura el ID antes de compilar el ejecutable.

### 3. Preparar la carpeta del juego

Copia el **contenido** de `ingame/` junto al ejecutable exportado:

```text
MiJuego/
├── MiJuego.exe
├── game.bat
└── resources/
    └── rpc/
        ├── rpc_bridge.py
        └── requirements.txt
```

Por defecto, el bridge busca `testdiscordrpc.exe`. Si el ejecutable tiene otro nombre, actualiza `GAME_EXE` en `rpc_bridge.py`.

### 4. Iniciar

Haz doble clic en `game.bat`. Primero busca `resources/rpc/rpc_bridge.exe`. Si no existe, busca Python 3 e instala las dependencias en un entorno local `.venv` la primera vez.

Para no exigir Python en el PC del jugador, proporciona un bridge compilado y configurado en `resources/rpc/rpc_bridge.exe`. La aplicación **Discord para escritorio** debe estar abierta y con la sesión iniciada.

## Bloques de la extensión

- **set [field] to [value]** — configurar un campo.
- **update presence** — enviar los campos a Discord.
- **clear presence** — borrar la actividad.
- **reconnect to bridge** — volver a intentar la conexión.
- **RPC connection status** — consultar el estado y el último error.
- **current value of [field]** — leer el valor actual de un campo.

Las marcas de tiempo usan segundos Unix, no milisegundos. Los campos de imagen utilizan claves de recursos de Discord, no URL de imágenes.

## Solución de problemas

- **Sin conexión:** comprueba que el bridge esté funcionando y que la extensión se haya cargado como unsandboxed.
- **No aparece la actividad:** comprueba Discord Desktop y el Application ID.
- **No aparecen imágenes:** revisa las claves de los recursos Rich Presence.
- **Error de Python:** instala Python 3 o proporciona el bridge compilado.
- Abrir `http://127.0.0.1:32123/` en un navegador no es una prueba válida; el endpoint espera conexiones WebSocket.

## Créditos y uso

Si utilizas, redistribuyes o adaptas este proyecto en tu juego u otro proyecto, **por favor, da crédito a Reqeuss** e incluye un enlace a este repositorio:

- Autor: **Reqeuss**
- Repositorio: https://github.com/reqeuss/discordrpc-turbowarp

Crédito sugerido:

> Integración de Discord RPC basada en [Discord RPC para TurboWarp](https://github.com/reqeuss/discordrpc-turbowarp) por Reqeuss.

Conserva este crédito al redistribuir versiones modificadas. Esta solicitud de atribución no sustituye los términos de las licencias de terceros aplicables.

## Comprobaciones de desarrollo

Ejecuta desde la raíz del repositorio:

```powershell
py -3 -m venv .venv
.venv\Scripts\python.exe -m pip install -r resources/rpc/requirements.txt
.venv\Scripts\python.exe -m py_compile resources/rpc/rpc_bridge.py
.venv\Scripts\python.exe -m unittest discover -s tests -v
node --check extension.js
```

CI comprueba la sintaxis y las pruebas unitarias, pero se recomienda una prueba real con el juego y Discord Desktop.

## Seguridad

El bridge escucha en `127.0.0.1`, solo en el equipo local. No lo expongas a otros dispositivos sin comprender los riesgos.

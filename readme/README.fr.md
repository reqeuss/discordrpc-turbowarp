# Discord Rich Presence pour TurboWarp

Ajoutez le Discord Rich Presence à un jeu TurboWarp grâce à une extension personnalisée et à un bridge local.

**Important :** l'extension doit être intégrée au projet TurboWarp pendant le développement, **avant l'exportation ou la compilation du jeu**. Ce projet ne peut pas injecter le RPC dans un jeu déjà exporté qui n'intégrait pas l'extension.

[🇫🇷 Français](README.fr.md) · [🇬🇧 English](README.en.md) · [🇪🇸 Español](README.es.md)

## Fonctionnalités

- Détails et état personnalisés dans l'activité Discord.
- Horodatages de début et de fin.
- Images Discord, informations de groupe, secrets Join/Spectate et indicateur d'instance.
- Reconnexion automatique au bridge.
- Communication WebSocket locale sur `127.0.0.1:32123`.
- Lancement Windows via `game.bat`.
- Bridge compilé facultatif pour éviter d'exiger Python sur le PC du joueur.

## Fonctionnement

1. Pendant le développement, chargez `extension.js` dans TurboWarp comme extension personnalisée **non sandboxée (unsandboxed)**.
2. Utilisez les blocs de l'extension dans le projet.
3. Exportez ou compilez le jeu avec l'extension intégrée.
4. Configurez l'identifiant de l'application Discord dans le bridge.
5. Copiez le contenu du dossier `ingame/` à côté de l'exécutable du jeu.
6. Lancez le jeu avec `game.bat`.

Si le jeu a été exporté sans l'extension, ajouter les fichiers du bridge après coup ne suffit pas.

## Installation

### 1. Intégrer l'extension avant l'export

Ajoutez `extension.js` à TurboWarp comme extension personnalisée **unsandboxed**. Utilisez les blocs pour renseigner les champs, puis appelez **update presence**. L'extension doit faire partie du projet avant l'exportation ou la compilation.

### 2. Configurer Discord

Dans le [Discord Developer Portal](https://discord.com/developers/applications), créez ou sélectionnez une application, puis copiez son **Application ID** depuis General Information.

Dans `resources/rpc/rpc_bridge.py`, remplacez la valeur :

```python
APP_ID = "YOUR_DISCORD_APPLICATION_ID"
```

Utilisez votre identifiant numérique. Pour les images, configurez les assets Rich Presence dans l'application Discord et utilisez leurs clés. **N'ajoutez jamais de bot token ni de client secret.**

Si vous distribuez `rpc_bridge.exe`, configurez l'identifiant avant de compiler cet exécutable.

### 3. Préparer le dossier du jeu

Copiez le **contenu** de `ingame/` à côté de l'exécutable exporté :

```text
MonJeu/
├── MonJeu.exe
├── game.bat
└── resources/
    └── rpc/
        ├── rpc_bridge.py
        └── requirements.txt
```

**Important :** ouvrez `resources/rpc/rpc_bridge.py` et remplacez `testdiscordrpc.exe` dans `GAME_EXE` par le nom exact du fichier `.exe` compilé de votre jeu, situé à la racine du dossier du jeu (à côté de `game.bat`). Gardez l’extension `.exe` et les guillemets. Par exemple, pour `MonJeu.exe`, utilisez `GAME_EXE = GAME_DIR / "MonJeu.exe"`.

### 4. Lancer le jeu

Double-cliquez sur `game.bat`. Le script cherche d'abord `resources/rpc/rpc_bridge.exe`. S'il n'existe pas, il cherche Python 3 et installe les dépendances dans un environnement `.venv` au premier lancement.

Pour éviter d'exiger Python sur le PC du joueur, placez un bridge compilé et correctement configuré dans `resources/rpc/rpc_bridge.exe`. L'application **Discord Desktop** doit être ouverte et connectée.

## Blocs de l'extension

- **set [field] to [value]** — configurer un champ.
- **update presence** — envoyer les informations à Discord.
- **clear presence** — effacer l'activité.
- **reconnect to bridge** — réessayer la connexion.
- **RPC connection status** — lire l'état de connexion et la dernière erreur.
- **current value of [field]** — lire la valeur d'un champ.

Les timestamps sont en secondes Unix, pas en millisecondes. Les images utilisent les clés d'assets Discord, pas des URL d'images.

## Dépannage

- **Aucune connexion :** vérifiez que le bridge fonctionne et que l'extension est chargée en mode unsandboxed.
- **Aucune activité :** vérifiez Discord Desktop et l'Application ID.
- **Images absentes :** vérifiez les clés des assets Rich Presence.
- **Erreur Python :** installez Python 3 ou fournissez le bridge compilé.
- Ouvrir `http://127.0.0.1:32123/` dans un navigateur ne teste pas le bridge : il attend une connexion WebSocket.

## Crédit et utilisation

Si vous utilisez, redistribuez ou adaptez ce projet dans un jeu ou un autre projet, **merci de créditer Reqeuss** et de créer un lien vers ce dépôt :

- Auteur : **Reqeuss**
- Dépôt : https://github.com/reqeuss/discordrpc-turbowarp

Exemple de crédit :

> Intégration Discord RPC propulsée par [Discord RPC pour TurboWarp](https://github.com/reqeuss/discordrpc-turbowarp) par Reqeuss.

Conservez ce crédit lors de la redistribution de versions modifiées. Cette demande de crédit ne remplace pas les conditions des licences tierces applicables.

## Vérifications de développement

Depuis la racine du dépôt :

```powershell
py -3 -m venv .venv
.venv\Scripts\python.exe -m pip install -r resources/rpc/requirements.txt
.venv\Scripts\python.exe -m py_compile resources/rpc/rpc_bridge.py
.venv\Scripts\python.exe -m unittest discover -s tests -v
node --check extension.js
```

La CI vérifie la syntaxe et les tests unitaires, mais un essai réel avec le jeu et Discord Desktop reste recommandé.

## Sécurité

Le bridge écoute sur `127.0.0.1`, donc uniquement sur la machine locale. Ne l'exposez pas à d'autres appareils sans comprendre les risques.

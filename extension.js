
(function (Scratch) {
    "use strict";

    const WS_URL = "ws://127.0.0.1:32123";

    const FIELDS = {
        details: "",
        state: "",
        startTimestamp: "",
        endTimestamp: "",
        largeImageKey: "",
        largeImageText: "",
        smallImageKey: "",
        smallImageText: "",
        partyId: "",
        partySize: "",
        partyMax: "",
        joinSecret: "",
        spectateSecret: "",
        instance: "true"
    };

    class DiscordRPC {
        constructor() {
            this.socket = null;
            this.pendingMessage = null;
            this.reconnectTimer = null;
            this.stopped = false;
            this.lastStatus = "Connecting";

            this.connect();
        }

        getInfo() {
            return {
                id: "reqeussdiscordrpc",
                name: "Discord Rich Presence",
                color1: "#5865F2",
                color2: "#4752C4",
                color3: "#364099",

                blocks: [
                    {
                        opcode: "setField",
                        blockType: Scratch.BlockType.COMMAND,
                        text: "set [FIELD] to [VALUE]",
                        arguments: {
                            FIELD: {
                                type: Scratch.ArgumentType.STRING,
                                menu: "fields"
                            },
                            VALUE: {
                                type: Scratch.ArgumentType.STRING,
                                defaultValue: "My activity"
                            }
                        }
                    },
                    {
                        opcode: "updatePresence",
                        blockType: Scratch.BlockType.COMMAND,
                        text: "update presence"
                    },
                    {
                        opcode: "clearPresence",
                        blockType: Scratch.BlockType.COMMAND,
                        text: "clear presence"
                    },
                    {
                        opcode: "connectionStatus",
                        blockType: Scratch.BlockType.REPORTER,
                        text: "RPC connection status"
                    }
                ],

                menus: {
                    fields: {
                        acceptReporters: false,
                        items: [
                            { text: "Details", value: "details" },
                            { text: "State", value: "state" },
                            { text: "Start timestamp", value: "startTimestamp" },
                            { text: "End timestamp", value: "endTimestamp" },
                            { text: "Large image key", value: "largeImageKey" },
                            { text: "Large image text", value: "largeImageText" },
                            { text: "Small image key", value: "smallImageKey" },
                            { text: "Small image text", value: "smallImageText" },
                            { text: "Party ID", value: "partyId" },
                            { text: "Party size", value: "partySize" },
                            { text: "Party maximum", value: "partyMax" },
                            { text: "Join secret", value: "joinSecret" },
                            { text: "Spectate secret", value: "spectateSecret" },
                            { text: "Instance (true/false)", value: "instance" }
                        ]
                    }
                }
            };
        }

        connect() {
            if (this.stopped) return;

            if (
                this.socket &&
                (
                    this.socket.readyState === WebSocket.OPEN ||
                    this.socket.readyState === WebSocket.CONNECTING
                )
            ) {
                return;
            }

            this.lastStatus = "Connecting";

            try {
                const ws = new WebSocket(WS_URL);
                this.socket = ws;

                ws.onopen = () => {
                    if (this.socket !== ws) return;

                    this.lastStatus = "Connected";
                    console.log("[Discord RPC] Connected to Python bridge.");

                    if (this.pendingMessage) {
                        const message = this.pendingMessage;
                        this.pendingMessage = null;
                        this.sendRaw(message);
                    }
                };

                ws.onmessage = (event) => {
                    console.log("[Discord RPC] Bridge:", event.data);
                };

                ws.onerror = (error) => {
                    console.error("[Discord RPC] WebSocket error:", error);
                    this.lastStatus = "Connection error";
                };

                ws.onclose = () => {
                    if (this.socket === ws) {
                        this.socket = null;
                    }

                    if (!this.stopped) {
                        this.lastStatus = "Disconnected";

                        if (this.reconnectTimer === null) {
                            this.reconnectTimer = setTimeout(() => {
                                this.reconnectTimer = null;
                                this.connect();
                            }, 2000);
                        }
                    }
                };
            } catch (error) {
                this.lastStatus = "Connection error";
                console.error("[Discord RPC] Cannot connect:", error);

                if (!this.stopped && this.reconnectTimer === null) {
                    this.reconnectTimer = setTimeout(() => {
                        this.reconnectTimer = null;
                        this.connect();
                    }, 2000);
                }
            }
        }

        setField(args) {
            const field = String(args.FIELD || "");
            const value = String(args.VALUE ?? "");

            if (!Object.prototype.hasOwnProperty.call(FIELDS, field)) {
                return;
            }

            FIELDS[field] = value;
        }

        makePayload() {
            const toTimestamp = (value) => {
                if (value.trim() === "") return null;

                const number = Number(value);

                if (!Number.isFinite(number)) return null;

                return Math.trunc(number);
            };

            const toInteger = (value) => {
                if (value.trim() === "") return null;

                const number = Number(value);

                if (!Number.isFinite(number)) return null;

                return Math.trunc(number);
            };

            const clean = (value) => {
                const text = String(value ?? "").trim();
                return text.length ? text : null;
            };

            return {
                action: "update",

                // Activity text
                details: clean(FIELDS.details),
                state: clean(FIELDS.state),

                // Unix timestamps, in seconds
                start: toTimestamp(FIELDS.startTimestamp),
                end: toTimestamp(FIELDS.endTimestamp),

                // Discord Developer Portal asset keys
                largeImage: clean(FIELDS.largeImageKey),
                largeText: clean(FIELDS.largeImageText),
                smallImage: clean(FIELDS.smallImageKey),
                smallText: clean(FIELDS.smallImageText),

                // Party configuration
                partyId: clean(FIELDS.partyId),
                partySize: toInteger(FIELDS.partySize),
                partyMax: toInteger(FIELDS.partyMax),

                // Join / Spectate
                joinSecret: clean(FIELDS.joinSecret),
                spectateSecret: clean(FIELDS.spectateSecret),

                // Boolean, not a string
                instance: FIELDS.instance.trim().toLowerCase() !== "false"
            };
        }

        sendRaw(payload) {
            if (
                this.socket &&
                this.socket.readyState === WebSocket.OPEN
            ) {
                try {
                    this.socket.send(JSON.stringify(payload));
                    this.lastStatus = "Connected";
                    console.log("[Discord RPC] Update sent:", payload);
                    return true;
                } catch (error) {
                    console.error("[Discord RPC] Send failed:", error);
                    this.pendingMessage = payload;
                    this.lastStatus = "Send error";
                    return false;
                }
            }

            this.pendingMessage = payload;
            this.lastStatus = "Waiting for bridge";
            this.connect();

            return false;
        }

        updatePresence() {
            // Every update contains ALL currently configured fields.
            const payload = this.makePayload();

            this.pendingMessage = payload;
            this.connect();

            if (
                this.socket &&
                this.socket.readyState === WebSocket.OPEN
            ) {
                this.pendingMessage = null;
                this.sendRaw(payload);
            }
        }

        clearPresence() {
            this.pendingMessage = null;
            this.sendRaw({ action: "clear" });
        }

        connectionStatus() {
            return this.lastStatus;
        }
    }

    Scratch.extensions.register(new DiscordRPC());
})(Scratch);

import { io, Socket } from "socket.io-client";

class SocketManager {
    private static instance: SocketManager;
    private socket: Socket;

    private constructor() {
        this.socket = io('https://api.dev.io:5000', {
            withCredentials: true,
            transports: ['websocket'],
            reconnection: true,
            reconnectionAttempts: 10,
            reconnectionDelay: 1000,
            reconnectionDelayMax: 5000,
            timeout: 20000 // Maximum time to wait for a connection to establish before giving up.
        });

        this.setupListeners();
    }

    private logEvent(event: string, ...args: any[]): void {
        console.log(`[Socket Event] ${event}`, args);
    }

    private logOperation(operation: string, ...args: any[]): void {
        console.log(`[Socket Operation] ${operation}`, args);
    }

    private setupListeners(): void {
        this.socket.on("connect", () => {
            this.logEvent("connect");
        });

        this.socket.on("disconnect", (reason: string) => {
            this.logEvent("disconnect", reason);
            if (reason === "io server disconnect") {
                this.socket.connect();
            }
        });

        this.socket.on("connect_error", (error: Error) => {
            this.logEvent("connect_error", error);
        });

        this.socket.on("reconnect_attempt", () => {
            this.logEvent("reconnect_attempt");
        });

        this.socket.on("reconnect_failed", () => {
            this.logEvent("reconnect_failed");
            console.error("All reconnection attempts failed. Manual intervention is required.");
            // Potentially send a notification or alert to the monitoring system.
        });

        // Log every operation
        this.socket.onAny((event: string, ...args: any[]) => {
            this.logEvent(event, ...args);
        });

        // Consider handling other Socket.IO events for robustness.
    }

    public static getInstance(): SocketManager {
        if (!SocketManager.instance) {
            SocketManager.instance = new SocketManager();
        }
        return SocketManager.instance;
    }

    public connect(): void {
        if (this.socket && !this.socket.connected) {
            this.socket.connect();
            this.logOperation("connect");
        }
    }

    public disconnect(): void {
        if (this.socket && this.socket.connected) {
            this.socket.disconnect();
            this.logOperation("disconnect");
        }
    }

    public on(event: string, callback: (...args: any[]) => void): void {
        this.socket.on(event, callback);
        this.logOperation("on", event);
    }

    public off(event: string, callback?: (...args: any[]) => void): void {
        this.socket.off(event, callback);
        this.logOperation("off", event);
    }

    public emit(event: string, payload: any): void {
        this.socket.emit(event, payload);
        this.logOperation("emit", event, payload);
    }
}

export default SocketManager;

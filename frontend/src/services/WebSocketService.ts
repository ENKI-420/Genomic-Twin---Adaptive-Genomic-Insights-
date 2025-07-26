class WebSocketService {
  private static instance: WebSocketService | null = null;
  private ws: WebSocket | null = null;
  private url: string;
  private reconnectAttempts: number = 0;
  private maxReconnectAttempts: number = 5;
  private reconnectInterval: number = 3000;

  public onConnect?: () => void;
  public onDisconnect?: () => void;
  public onMessage?: (message: any) => void;
  public onError?: (error: Event) => void;

  constructor(url?: string) {
    this.url = url || `ws://localhost:${process.env.REACT_APP_WEBSOCKET_PORT || 8082}`;
  }

  static getInstance(): WebSocketService | null {
    return WebSocketService.instance;
  }

  connect(): void {
    try {
      this.ws = new WebSocket(this.url);
      WebSocketService.instance = this;

      this.ws.onopen = () => {
        console.log('🔌 WebSocket connected');
        this.reconnectAttempts = 0;
        if (this.onConnect) {
          this.onConnect();
        }
      };

      this.ws.onmessage = (event) => {
        try {
          const message = JSON.parse(event.data);
          if (this.onMessage) {
            this.onMessage(message);
          }
        } catch (error) {
          console.error('Failed to parse WebSocket message:', error);
        }
      };

      this.ws.onclose = () => {
        console.log('🔌 WebSocket disconnected');
        if (this.onDisconnect) {
          this.onDisconnect();
        }
        this.attemptReconnect();
      };

      this.ws.onerror = (error) => {
        console.error('WebSocket error:', error);
        if (this.onError) {
          this.onError(error);
        }
      };

    } catch (error) {
      console.error('Failed to connect to WebSocket:', error);
      this.attemptReconnect();
    }
  }

  private attemptReconnect(): void {
    if (this.reconnectAttempts < this.maxReconnectAttempts) {
      this.reconnectAttempts++;
      console.log(`Attempting to reconnect (${this.reconnectAttempts}/${this.maxReconnectAttempts})...`);
      
      setTimeout(() => {
        this.connect();
      }, this.reconnectInterval);
    } else {
      console.error('Max reconnection attempts reached');
    }
  }

  send(message: any): void {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify(message));
    } else {
      console.warn('WebSocket is not connected');
    }
  }

  disconnect(): void {
    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }
    WebSocketService.instance = null;
  }

  getConnectionState(): number {
    return this.ws ? this.ws.readyState : WebSocket.CLOSED;
  }

  isConnected(): boolean {
    return this.ws?.readyState === WebSocket.OPEN;
  }
}

export default WebSocketService;
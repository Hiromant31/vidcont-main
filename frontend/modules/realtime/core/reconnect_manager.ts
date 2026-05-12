import { eventBus } from './event_bus';
import { RealtimeEvent, ConnectionStatus, ConnectionHealth } from '../types/realtime_types';

interface ReconnectConfig {
  maxRetries: number;
  baseDelay: number;
  maxDelay: number;
}

export class ReconnectManager {
  private retryCount = 0;
  private timeoutId: NodeJS.Timeout | null = null;
  private config: ReconnectConfig;
  private onReconnect: () => void;
  private onFailed: () => void;
  private onStatusChange: (status: ConnectionStatus) => void;

  constructor(
    onReconnect: () => void,
    onFailed: () => void,
    onStatusChange: (status: ConnectionStatus) => void,
    config: ReconnectConfig = { maxRetries: 5, baseDelay: 1000, maxDelay: 30000 }
  ) {
    this.onReconnect = onReconnect;
    this.onFailed = onFailed;
    this.onStatusChange = onStatusChange;
    this.config = config;
  }

  scheduleReconnect(): void {
    if (this.retryCount >= this.config.maxRetries) {
      this.onFailed();
      this.onStatusChange('failed');
      return;
    }

    const delay = Math.min(
      this.config.baseDelay * Math.pow(2, this.retryCount),
      this.config.maxDelay
    );

    this.retryCount++;
    this.onStatusChange('connecting');

    this.timeoutId = setTimeout(() => {
      this.onReconnect();
    }, delay);
  }

  reset(): void {
    this.retryCount = 0;
    if (this.timeoutId) {
      clearTimeout(this.timeoutId);
      this.timeoutId = null;
    }
    this.onStatusChange('connected');
  }

  cancel(): void {
    if (this.timeoutId) {
      clearTimeout(this.timeoutId);
      this.timeoutId = null;
    }
  }

  getRetryCount(): number {
    return this.retryCount;
  }
}

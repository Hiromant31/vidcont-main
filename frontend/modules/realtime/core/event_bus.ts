import { RealtimeEvent, ConnectionStatus } from '../types/realtime_types';

type EventCallback<T = any> = (event: RealtimeEvent<T>) => void;

class EventBus {
  private listeners: Map<string, Set<EventCallback>>;

  constructor() {
    this.listeners = new Map();
  }

  on<T>(eventType: string, callback: EventCallback<T>): () => void {
    if (!this.listeners.has(eventType)) {
      this.listeners.set(eventType, new Set());
    }
    
    const callbacks = this.listeners.get(eventType)!;
    callbacks.add(callback as EventCallback);

    // Return unsubscribe function
    return () => {
      callbacks.delete(callback as EventCallback);
      if (callbacks.size === 0) {
        this.listeners.delete(eventType);
      }
    };
  }

  off<T>(eventType: string, callback?: EventCallback<T>): void {
    if (!callback) {
      this.listeners.delete(eventType);
      return;
    }

    const callbacks = this.listeners.get(eventType);
    if (callbacks) {
      callbacks.delete(callback as EventCallback);
      if (callbacks.size === 0) {
        this.listeners.delete(eventType);
      }
    }
  }

  emit<T>(eventType: string, payload: T, source: string): void {
    const event: RealtimeEvent<T> = {
      type: eventType as any,
      payload,
      timestamp: new Date().toISOString(),
      source: source as any,
    };

    const callbacks = this.listeners.get(eventType);
    if (callbacks) {
      callbacks.forEach((callback) => {
        try {
          callback(event);
        } catch (error) {
          console.error(`Error in event listener for ${eventType}:`, error);
        }
      });
    }

    // Also emit to wildcard listener if exists
    const allCallbacks = this.listeners.get('*');
    if (allCallbacks) {
      allCallbacks.forEach((callback) => {
        try {
          callback(event);
        } catch (error) {
          console.error(`Error in wildcard listener:`, error);
        }
      });
    }
  }

  clear(): void {
    this.listeners.clear();
  }

  getListenerCount(eventType: string): number {
    return this.listeners.get(eventType)?.size || 0;
  }
}

// Singleton instance
export const eventBus = new EventBus();

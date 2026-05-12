import { create } from 'zustand';
import { websocketService } from '@/services/websocket/service';
import type { WebSocketMessage } from '@/types';

interface WebSocketState {
  connected: boolean;
  connecting: boolean;
  error: string | null;
  connect: () => Promise<void>;
  disconnect: () => void;
  sendMessage: (data: any) => void;
}

export const useWebSocketStore = create<WebSocketState>((set, get) => ({
  connected: false,
  connecting: false,
  error: null,

  connect: async () => {
    set({ connecting: true, error: null });
    try {
      await websocketService.connect();
      set({ connected: true, connecting: false });

      websocketService.on('job_progress', (message) => {
        console.log('Job progress:', message);
      });

      websocketService.on('job_completed', (message) => {
        console.log('Job completed:', message);
      });

      websocketService.on('stage_completed', (message) => {
        console.log('Stage completed:', message);
      });

      websocketService.on('stage_failed', (message) => {
        console.log('Stage failed:', message);
      });

      websocketService.on('render_started', (message) => {
        console.log('Render started:', message);
      });

      websocketService.on('render_completed', (message) => {
        console.log('Render completed:', message);
      });

      websocketService.on('logs_updated', (message) => {
        console.log('Logs updated:', message);
      });
    } catch (error) {
      set({
        connected: false,
        connecting: false,
        error: error instanceof Error ? error.message : 'Connection failed',
      });
    }
  },

  disconnect: () => {
    websocketService.disconnect();
    set({ connected: false, connecting: false });
  },

  sendMessage: (data) => {
    websocketService.send(data);
  },
}));

import { create } from 'zustand';
import { ConnectionStatus, ConnectionHealth } from '../types/realtime_types';

interface RealtimeStore {
  status: ConnectionStatus;
  health: ConnectionHealth;
  lastEventTimestamp: string | null;
  
  setStatus: (status: ConnectionStatus) => void;
  setHealth: (health: ConnectionHealth) => void;
  updateLastEvent: (timestamp: string) => void;
  reset: () => void;
}

export const useRealtimeStore = create<RealtimeStore>((set) => ({
  status: 'disconnected',
  health: { status: 'disconnected', retryCount: 0 },
  lastEventTimestamp: null,

  setStatus: (status) => set({ status }),
  
  setHealth: (health) => set({ health }),
  
  updateLastEvent: (timestamp) => set({ lastEventTimestamp: timestamp }),
  
  reset: () => set({
    status: 'disconnected',
    health: { status: 'disconnected', retryCount: 0 },
    lastEventTimestamp: null,
  }),
}));

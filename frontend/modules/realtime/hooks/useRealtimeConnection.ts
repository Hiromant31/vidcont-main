'use client';

import { useEffect, useCallback } from 'react';
import { useRealtimeStore } from '../stores/realtime_store';
import { realtimeClient } from '../core/realtime_client';
import { ConnectionStatus } from '../types/realtime_types';

export function useRealtimeConnection() {
  const status = useRealtimeStore((state) => state.status);
  const setStatus = useRealtimeStore((state) => state.setStatus);

  const connect = useCallback(() => {
    realtimeClient.connect();
  }, []);

  const disconnect = useCallback(() => {
    realtimeClient.disconnect();
  }, []);

  useEffect(() => {
    // Auto-connect on mount if needed
    return () => {
      // Cleanup on unmount optional
      // disconnect();
    };
  }, []);

  return {
    status,
    isConnected: status === 'connected',
    isConnecting: status === 'connecting' || status === 'reconnecting',
    isDisconnected: status === 'disconnected',
    isFailed: status === 'failed',
    connect,
    disconnect,
  };
}

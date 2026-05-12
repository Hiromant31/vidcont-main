'use client';

import { useEffect } from 'react';
import { useWebSocketStore } from '@/stores/websocket_store';

export function WebSocketProvider({ children }: { children: React.ReactNode }) {
  const { connect, disconnect } = useWebSocketStore();

  useEffect(() => {
    connect();

    return () => {
      disconnect();
    };
  }, [connect, disconnect]);

  return <>{children}</>;
}

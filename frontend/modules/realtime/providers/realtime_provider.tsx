'use client';

import { useEffect, useCallback } from 'react';
import { getRealtimeClient } from '../core/realtime_client';
import { eventBus } from '../core/event_bus';
import { useRealtimeStore } from '../stores/realtime_store';
import { RealtimeEvent } from '../types/realtime_types';

interface RealtimeProviderProps {
  children: React.ReactNode;
  wsUrl?: string;
}

export function RealtimeProvider({ children, wsUrl }: RealtimeProviderProps) {
  const setStatus = useRealtimeStore((state) => state.setStatus);
  const setHealth = useRealtimeStore((state) => state.setHealth);
  const updateLastEvent = useRealtimeStore((state) => state.updateLastEvent);

  const handleEvent = useCallback((event: RealtimeEvent) => {
    updateLastEvent(event.timestamp);
    
    // Update store status for connection events
    if (event.type === 'connection_status_changed') {
      const health = event.payload;
      setStatus(health.status);
      setHealth(health);
    }
  }, [updateLastEvent, setStatus, setHealth]);

  useEffect(() => {
    const client = getRealtimeClient(wsUrl);
    client.connect();

    // Subscribe to all events
    const unsubscribe = eventBus.subscribe('*', handleEvent);

    return () => {
      unsubscribe();
      // Do not disconnect client on unmount, keep it alive for SPA navigation
    };
  }, [wsUrl, handleEvent]);

  return <>{children}</>;
}

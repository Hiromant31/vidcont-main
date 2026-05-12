'use client';

import { useEffect } from 'react';
import { eventBus } from '../core/event_bus';
import { RealtimeEvent, EventType } from '../types/realtime_types';

export function useEventSubscription<T = any>(
  eventType: EventType | '*',
  callback: (event: RealtimeEvent<T>) => void
): void {
  useEffect(() => {
    const unsubscribe = eventBus.on(eventType, callback as any);
    return () => {
      unsubscribe();
    };
  }, [eventType, callback]);
}

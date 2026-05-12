'use client';

import { useEffect } from 'react';
import { eventBus } from '../core/event_bus';
import { RealtimeEvent, EventType } from '../types/realtime_types';

export function useRealtimeEvents<T>(
  eventType: EventType | '*',
  handler: (event: RealtimeEvent<T>) => void
) {
  useEffect(() => {
    const unsubscribe = eventBus.on(eventType, handler);

    return () => {
      unsubscribe();
    };
  }, [eventType, handler]);
}

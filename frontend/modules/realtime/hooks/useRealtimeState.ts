'use client';

import { useEffect } from 'react';
import { useEventSubscription } from './useEventSubscription';
import { useRealtimeStore } from '../stores/realtime_store';
import { RealtimeEvent } from '../types/realtime_types';
import { mapEventToStore } from '../utils/event_mapper';
import { throttleEvent } from '../utils/throttle_events';

export const useRealtimeState = () => {
  const updateLastEvent = useRealtimeStore((state) => state.updateLastEvent);

  // Handle all events globally
  useEventSubscription('*', (event: RealtimeEvent) => {
    updateLastEvent(event.timestamp);
    
    // Throttle high-frequency events
    if (event.type === 'job_progress' || event.type === 'log_stream') {
      throttleEvent(
        event.type,
        () => mapEventToStore(event),
        event,
        500 // 500ms throttle for progress/logs
      );
    } else {
      mapEventToStore(event);
    }
  });

  return {
    lastEventTimestamp: useRealtimeStore((state) => state.lastEventTimestamp),
  };
};

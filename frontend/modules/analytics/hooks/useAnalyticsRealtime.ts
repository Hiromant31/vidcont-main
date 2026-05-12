'use client';

import { useEffect } from 'react';
import { useQueryClient } from '@tanstack/react-query';
import { ANALYTICS_KEYS } from '../api/analytics_queries';
import { websocketService } from '@/services/websocket/service';

export const useAnalyticsRealtime = () => {
  const queryClient = useQueryClient();

  useEffect(() => {
    const handleMetricsUpdate = (data: any) => {
      // Invalidate relevant queries based on event type
      if (data.type === 'pipeline') {
        queryClient.invalidateQueries({ queryKey: ANALYTICS_KEYS.pipeline() });
      } else if (data.type === 'jobs') {
        queryClient.invalidateQueries({ queryKey: ANALYTICS_KEYS.jobs() });
      } else if (data.type === 'render') {
        queryClient.invalidateQueries({ queryKey: ANALYTICS_KEYS.render() });
      } else if (data.type === 'system') {
        queryClient.invalidateQueries({ queryKey: ANALYTICS_KEYS.system() });
      } else {
        // Global update
        queryClient.invalidateQueries({ queryKey: ANALYTICS_KEYS.all });
      }
    };

    const handleErrorSpike = (data: any) => {
      console.warn('Error spike detected:', data);
      queryClient.invalidateQueries({ queryKey: ANALYTICS_KEYS.jobs() });
    };

    const unsubscribeMetrics = websocketService.on('metrics_updated', handleMetricsUpdate);
    const unsubscribeErrorSpike = websocketService.on('error_spike_detected', handleErrorSpike);

    return () => {
      unsubscribeMetrics();
      unsubscribeErrorSpike();
    };
  }, [queryClient]);
};

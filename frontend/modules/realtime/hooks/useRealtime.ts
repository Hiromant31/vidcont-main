import { getRealtimeClient } from '../core/realtime_client';
import { eventBus } from '../core/event_bus';

export const useRealtime = () => {
  const client = getRealtimeClient();

  const sendEvent = (type: string, payload: any) => {
    client.send({
      type: type as any,
      payload,
      timestamp: new Date().toISOString(),
      source: 'system',
    });
  };

  return {
    status: client.getStatus(),
    health: client.getHealth(),
    sendEvent,
    isConnected: client.getStatus() === 'connected',
  };
};

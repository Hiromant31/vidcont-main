import { useRealtimeStore } from '../stores/realtime_store';
import { checkConnectionHealth, getHealthColor, getHealthLabel } from '../utils/connection_health';

export const useConnectionStatus = () => {
  const status = useRealtimeStore((state) => state.status);
  const health = useRealtimeStore((state) => state.health);

  const computedStatus = checkConnectionHealth(health);
  const color = getHealthColor(computedStatus);
  const label = getHealthLabel(computedStatus);

  return {
    status: computedStatus,
    originalStatus: status,
    health,
    color,
    label,
    isConnected: computedStatus === 'connected',
    isConnecting: computedStatus === 'connecting',
    isDisconnected: computedStatus === 'disconnected',
    isFailed: computedStatus === 'failed',
    isUnstable: computedStatus === ('unstable' as any),
  };
};

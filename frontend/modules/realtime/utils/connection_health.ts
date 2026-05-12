import { ConnectionHealth, ConnectionStatus } from '../types/realtime_types';

export const checkConnectionHealth = (health: ConnectionHealth): ConnectionStatus => {
  if (health.status === 'connected') {
    // Check if latency is too high
    if (health.latencyMs && health.latencyMs > 1000) {
      return 'unstable' as ConnectionStatus; // Cast to allow custom status
    }
    
    // Check if last ping was too long ago
    if (health.lastPing) {
      const timeSincePing = Date.now() - new Date(health.lastPing).getTime();
      if (timeSincePing > 60000) { // 1 minute
        return 'unstable' as ConnectionStatus;
      }
    }
    
    return 'connected';
  }
  
  return health.status;
};

export const getHealthColor = (status: ConnectionStatus | 'unstable'): string => {
  switch (status) {
    case 'connected':
      return 'bg-green-500';
    case 'connecting':
      return 'bg-yellow-500 animate-pulse';
    case 'disconnected':
      return 'bg-gray-500';
    case 'failed':
      return 'bg-red-500';
    case 'unstable':
      return 'bg-orange-500 animate-pulse';
    default:
      return 'bg-gray-500';
  }
};

export const getHealthLabel = (status: ConnectionStatus | 'unstable'): string => {
  switch (status) {
    case 'connected':
      return 'Connected';
    case 'connecting':
      return 'Connecting...';
    case 'disconnected':
      return 'Disconnected';
    case 'failed':
      return 'Connection Failed';
    case 'unstable':
      return 'Unstable Connection';
    default:
      return 'Unknown';
  }
};

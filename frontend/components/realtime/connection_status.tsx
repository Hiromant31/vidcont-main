'use client';

import { useWebSocketStore } from '@/stores/websocket_store';
import { RealtimeIndicator } from '@/components/realtime/indicator';

export function ConnectionStatus() {
  const { connected } = useWebSocketStore();

  return <RealtimeIndicator connected={connected} />;
}

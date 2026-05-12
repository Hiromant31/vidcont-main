import { RealtimeEvent, EventType } from '../types/realtime_types';

/**
 * Маппинг входящих WebSocket событий в модульную EventBus систему.
 * Принимает событие из WS сервиса ({ type, data, timestamp })
 * и создаёт RealtimeEvent для eventBus.
 */
export const mapIncomingEvent = (wsMessage: { type: string; data: any; timestamp: string }): RealtimeEvent | null => {
  // Проверяем, что тип события известен
  const knownTypes: string[] = [
    'job_started', 'job_progress', 'job_completed', 'job_failed',
    'stage_completed', 'stage_failed',
    'render_started', 'render_completed',
    'logs_updated',
    'metrics_updated', 'error_spike_detected',
    'asset_created', 'asset_updated', 'asset_deleted', 'asset_ready', 'asset_failed',
  ];

  if (!knownTypes.includes(wsMessage.type)) {
    console.warn('[EventMapper] Unknown event type:', wsMessage.type);
    return null;
  }

  const sourceMap: Record<string, string> = {
    job_started: 'jobs', job_progress: 'jobs', job_completed: 'jobs', job_failed: 'jobs',
    stage_completed: 'pipeline', stage_failed: 'pipeline',
    render_started: 'pipeline', render_completed: 'pipeline',
    logs_updated: 'jobs',
    metrics_updated: 'system', error_spike_detected: 'system',
    asset_created: 'system', asset_updated: 'system', asset_deleted: 'system',
    asset_ready: 'system', asset_failed: 'system',
  };

  return {
    type: wsMessage.type as EventType,
    payload: wsMessage.data,
    timestamp: wsMessage.timestamp,
    source: sourceMap[wsMessage.type] as any,
  };
};

export const mapEventToStore = (event: RealtimeEvent): void => {
  // Каждый модуль подписывается на события через eventBus.on()
  // Этот файл — точка расширения для модульной маршрутизации
  switch (event.type) {
    case 'job_progress':
    case 'job_started':
    case 'job_completed':
    case 'job_failed':
      break;
    case 'stage_completed':
    case 'stage_failed':
      break;
    case 'render_started':
    case 'render_completed':
      break;
    case 'metrics_updated':
    case 'error_spike_detected':
      break;
    case 'asset_created':
    case 'asset_updated':
    case 'asset_deleted':
    case 'asset_ready':
    case 'asset_failed':
      break;
    default:
      console.log('[EventMapper] Unhandled event type:', event.type);
  }
};

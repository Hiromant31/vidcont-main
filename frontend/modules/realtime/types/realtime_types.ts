export type EventSource = 'pipeline' | 'jobs' | 'scenes' | 'characters' | 'projects' | 'system';

export type EventType =
  | 'connection_status_changed'
  | 'job_started'
  | 'job_progress'
  | 'job_completed'
  | 'job_failed'
  | 'stage_completed'
  | 'stage_failed'
  | 'render_started'
  | 'render_completed'
  | 'logs_updated'
  | 'metrics_updated'
  | 'error_spike_detected'
  | 'asset_created'
  | 'asset_updated'
  | 'asset_deleted'
  | 'asset_ready'
  | 'asset_failed'
  | 'pipeline_stage_started'
  | 'pipeline_stage_progress'
  | 'project_updated'
  | 'project_created'
  | 'character_updated'
  | 'log_stream'
  | 'system_alert';

export interface RealtimeEvent<T = any> {
  type: EventType;
  payload: T;
  timestamp: string;
  source: EventSource;
}

export type ConnectionStatus = 'connected' | 'connecting' | 'disconnected' | 'reconnecting' | 'failed';

export interface ConnectionHealth {
  status: ConnectionStatus;
  latencyMs?: number;
  lastPing?: string;
  retryCount: number;
}

export interface RetryConfig {
  maxAttempts: number;
  baseDelayMs: number;
  maxDelayMs: number;
  jitterMs: number;
}

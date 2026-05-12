import { PipelineMetrics } from '../types/analytics_types';

export const mapPipelineMetrics = (data: any): PipelineMetrics => ({
  total_runs: data.total_runs || 0,
  success_rate: data.success_rate || 0,
  failure_rate: data.failure_rate || 0,
  avg_duration_sec: data.avg_duration_sec || 0,
  stage_breakdown: data.stage_breakdown || {},
});

export const mapJobMetrics = (data: any) => ({
  total_jobs: data.total_jobs || 0,
  queued: data.queued || 0,
  running: data.running || 0,
  completed: data.completed || 0,
  failed: data.failed || 0,
  avg_processing_time: data.avg_processing_time || 0,
});

export const mapRenderMetrics = (data: any) => ({
  total_renders: data.total_renders || 0,
  success_rate: data.success_rate || 0,
  avg_render_time_sec: data.avg_render_time_sec || 0,
  avg_video_length_sec: data.avg_video_length_sec || 0,
  resolution_distribution: data.resolution_distribution || {},
});

export const mapSystemLoad = (data: any) => ({
  cpu_usage: data.cpu_usage || 0,
  memory_usage: data.memory_usage || 0,
  active_connections: data.active_connections || 0,
  queue_size: data.queue_size || 0,
  throughput_per_min: data.throughput_per_min || 0,
});

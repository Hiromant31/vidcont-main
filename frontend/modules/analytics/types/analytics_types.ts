export interface PipelineMetrics {
  total_runs: number;
  success_rate: number;
  failure_rate: number;
  avg_duration_sec: number;
  stage_breakdown: Record<string, {
    success: number;
    failed: number;
    avg_time: number;
  }>;
}

export interface JobMetrics {
  total_jobs: number;
  queued: number;
  running: number;
  completed: number;
  failed: number;
  avg_processing_time: number;
}

export interface RenderMetrics {
  total_renders: number;
  success_rate: number;
  avg_render_time_sec: number;
  avg_video_length_sec: number;
  resolution_distribution: Record<string, number>;
}

export interface SystemLoadMetrics {
  cpu_usage: number;
  memory_usage: number;
  active_connections: number;
  queue_size: number;
  throughput_per_min: number;
}

export interface AnalyticsOverview {
  total_projects: number;
  total_jobs: number;
  total_renders: number;
  global_success_rate: number;
  total_errors: number;
  estimated_cost_usd: number;
}

export interface TimeSeriesData {
  timestamp: string;
  value: number;
  label?: string;
}

export interface AnalyticsFilters {
  date_from: string;
  date_to: string;
  project_id?: string;
  pipeline_stage?: string;
  status?: 'all' | 'success' | 'failed';
  time_range?: string;
}

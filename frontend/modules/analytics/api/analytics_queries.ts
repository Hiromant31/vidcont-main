import { useQuery } from '@tanstack/react-query';
import { analyticsApi } from './analytics_api';
import { AnalyticsFilters } from '../types/analytics_types';

export const ANALYTICS_KEYS = {
  all: ['analytics'] as const,
  overview: () => [...ANALYTICS_KEYS.all, 'overview'] as const,
  pipeline: () => [...ANALYTICS_KEYS.all, 'pipeline'] as const,
  jobs: () => [...ANALYTICS_KEYS.all, 'jobs'] as const,
  render: () => [...ANALYTICS_KEYS.all, 'render'] as const,
  system: () => [...ANALYTICS_KEYS.all, 'system'] as const,
};

const buildParams = (filters?: AnalyticsFilters): Record<string, string> => {
  const params: Record<string, string> = {};
  if (filters?.date_from) params.from = filters.date_from;
  if (filters?.date_to) params.to = filters.date_to;
  if (filters?.project_id) params.project = filters.project_id;
  if (filters?.pipeline_stage) params.stage = filters.pipeline_stage;
  if (filters?.status && filters.status !== 'all') params.status = filters.status;
  return params;
};

export const useAnalyticsOverview = (filters?: AnalyticsFilters) => {
  const params = buildParams(filters);
  return useQuery({
    queryKey: [...ANALYTICS_KEYS.overview(), params],
    queryFn: () => analyticsApi.getOverview(params),
    refetchInterval: 30000, // 30s
  });
};

export const usePipelineStats = (filters?: AnalyticsFilters) => {
  const params = buildParams(filters);
  return useQuery({
    queryKey: [...ANALYTICS_KEYS.pipeline(), params],
    queryFn: () => analyticsApi.getPipelineStats(params),
    refetchInterval: 10000, // 10s
  });
};

export const useJobsStats = (filters?: AnalyticsFilters) => {
  const params = buildParams(filters);
  return useQuery({
    queryKey: [...ANALYTICS_KEYS.jobs(), params],
    queryFn: () => analyticsApi.getJobsStats(params),
    refetchInterval: 5000, // 5s
  });
};

export const useRenderStats = (filters?: AnalyticsFilters) => {
  const params = buildParams(filters);
  return useQuery({
    queryKey: [...ANALYTICS_KEYS.render(), params],
    queryFn: () => analyticsApi.getRenderStats(params),
    refetchInterval: 10000,
  });
};

export const useSystemLoad = () => {
  return useQuery({
    queryKey: ANALYTICS_KEYS.system(),
    queryFn: analyticsApi.getSystemLoad,
    refetchInterval: 2000, // 2s for real-time feel
  });
};

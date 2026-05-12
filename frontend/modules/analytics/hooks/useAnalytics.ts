import { useAnalyticsOverview, usePipelineStats, useJobsStats, useRenderStats, useSystemLoad } from '../api/analytics_queries';
import { useAnalyticsStore } from '../stores/analytics_store';
import { useAnalyticsRealtime } from './useAnalyticsRealtime';

export const useAnalytics = () => {
  const filters = useAnalyticsStore((state) => state.filters);
  
  // Enable realtime updates
  useAnalyticsRealtime();

  const { data: overview, isLoading: loadingOverview } = useAnalyticsOverview(filters);
  const { data: pipeline, isLoading: loadingPipeline } = usePipelineStats(filters);
  const { data: jobs, isLoading: loadingJobs } = useJobsStats(filters);
  const { data: render, isLoading: loadingRender } = useRenderStats(filters);
  const { data: system, isLoading: loadingSystem } = useSystemLoad();

  const isLoading = loadingOverview || loadingPipeline || loadingJobs || loadingRender || loadingSystem;

  return {
    overview,
    pipeline,
    jobs,
    render,
    system,
    isLoading,
  };
};

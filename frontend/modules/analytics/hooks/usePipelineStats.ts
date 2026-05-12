import { usePipelineStats as usePipelineStatsQuery } from '../api/analytics_queries';

export const usePipelineStats = (filters?: any) => {
  return usePipelineStatsQuery(filters);
};

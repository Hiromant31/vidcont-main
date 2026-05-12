import { useRenderStats as useRenderStatsQuery } from '../api/analytics_queries';

export const useRenderStats = (filters?: any) => {
  return useRenderStatsQuery(filters);
};

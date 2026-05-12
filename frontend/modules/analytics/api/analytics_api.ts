import { apiClient } from '@/services/api/client';
import { AnalyticsOverview, PipelineMetrics, JobMetrics, RenderMetrics, SystemLoadMetrics } from '../types/analytics_types';

export const analyticsApi = {
  getOverview: async (params?: Record<string, string>): Promise<AnalyticsOverview> => {
    const queryParams = new URLSearchParams(params);
    const response = await apiClient.get(`/analytics/overview?${queryParams}`);
    return response.data;
  },

  getPipelineStats: async (params?: Record<string, string>): Promise<PipelineMetrics> => {
    const queryParams = new URLSearchParams(params);
    const response = await apiClient.get(`/analytics/pipeline?${queryParams}`);
    return response.data;
  },

  getJobsStats: async (params?: Record<string, string>): Promise<JobMetrics> => {
    const queryParams = new URLSearchParams(params);
    const response = await apiClient.get(`/analytics/jobs?${queryParams}`);
    return response.data;
  },

  getRenderStats: async (params?: Record<string, string>): Promise<RenderMetrics> => {
    const queryParams = new URLSearchParams(params);
    const response = await apiClient.get(`/analytics/render?${queryParams}`);
    return response.data;
  },

  getSystemLoad: async (): Promise<SystemLoadMetrics> => {
    const response = await apiClient.get('/analytics/system');
    return response.data;
  },
};

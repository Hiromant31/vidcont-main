import { apiClient } from './client';
import type { RenderJob } from '@/types';

export const renderApi = {
  async start(data: { job_id: string }): Promise<RenderJob> {
    const response = await apiClient.post('/render/start', data);
    return response.data;
  },

  async getStatus(id: string): Promise<RenderJob> {
    const response = await apiClient.get(`/render/status/${id}`);
    return response.data;
  },

  async getResult(id: string): Promise<{ video_url: string }> {
    const response = await apiClient.get(`/render/result/${id}`);
    return response.data;
  },
};

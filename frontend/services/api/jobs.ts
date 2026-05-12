import { apiClient } from './client';
import type { Job } from '@/types';

export const jobsApi = {
  async getAll(): Promise<Job[]> {
    const response = await apiClient.get('/jobs');
    return response.data;
  },

  async getById(id: string): Promise<Job> {
    const response = await apiClient.get(`/jobs/${id}`);
    return response.data;
  },

  async start(data: { project_id: string }): Promise<Job> {
    const response = await apiClient.post('/jobs/start', data);
    return response.data;
  },

  async stop(id: string): Promise<void> {
    await apiClient.post(`/jobs/${id}/stop`);
  },

  async retry(id: string): Promise<Job> {
    const response = await apiClient.post(`/jobs/${id}/retry`);
    return response.data;
  },
};

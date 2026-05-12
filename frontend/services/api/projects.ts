import { apiClient } from './client';
import type { Project } from '@/types';

export const projectsApi = {
  async getAll(): Promise<Project[]> {
    const response = await apiClient.get('/projects');
    return response.data;
  },

  async getById(id: string): Promise<Project> {
    const response = await apiClient.get(`/projects/${id}`);
    return response.data;
  },

  async create(data: { name: string; description?: string }): Promise<Project> {
    const response = await apiClient.post('/projects', data);
    return response.data;
  },

  async update(id: string, data: Partial<Project>): Promise<Project> {
    const response = await apiClient.put(`/projects/${id}`, data);
    return response.data;
  },

  async delete(id: string): Promise<void> {
    await apiClient.delete(`/projects/${id}`);
  },
};

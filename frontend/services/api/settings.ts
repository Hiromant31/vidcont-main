import { apiClient } from './client';
import type { Settings, PromptTemplate, RenderJob } from '@/types';

export const settingsApi = {
  async get(): Promise<Settings[]> {
    const response = await apiClient.get('/settings');
    return response.data;
  },

  async getAll(): Promise<Settings[]> {
    const response = await apiClient.get('/settings/all');
    return response.data;
  },

  async getById(id: string): Promise<Settings> {
    const response = await apiClient.get(`/settings/${id}`);
    return response.data;
  },

  async create(data: Partial<Settings>): Promise<Settings> {
    const response = await apiClient.post('/settings/create', data);
    return response.data;
  },

  async update(id: string, data: Partial<Settings>): Promise<Settings> {
    const response = await apiClient.put(`/settings/${id}`, data);
    return response.data;
  },

  async delete(id: string): Promise<void> {
    await apiClient.delete(`/settings/${id}`);
  },
};

export const promptsApi = {
  async getAll(): Promise<PromptTemplate[]> {
    const response = await apiClient.get('/prompts');
    return response.data;
  },

  async getById(id: string): Promise<PromptTemplate> {
    const response = await apiClient.get(`/prompts/${id}`);
    return response.data;
  },

  async create(data: Partial<PromptTemplate>): Promise<PromptTemplate> {
    const response = await apiClient.post('/prompts', data);
    return response.data;
  },

  async update(id: string, data: Partial<PromptTemplate>): Promise<PromptTemplate> {
    const response = await apiClient.put(`/prompts/${id}`, data);
    return response.data;
  },

  async delete(id: string): Promise<void> {
    await apiClient.delete(`/prompts/${id}`);
  },
};

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

export const pipelineApi = {
  async run(data: { project_id: string }): Promise<Job> {
    const response = await apiClient.post('/pipeline/run', data);
    return response.data;
  },

  async runStage(stage: string, jobId: string): Promise<any> {
    const response = await apiClient.post('/pipeline/run-stage', { stage, job_id: jobId });
    return response.data;
  },

  async pause(jobId: string): Promise<void> {
    await apiClient.post('/pipeline/pause', { job_id: jobId });
  },

  async resume(jobId: string): Promise<void> {
    await apiClient.post('/pipeline/resume', { job_id: jobId });
  },
};

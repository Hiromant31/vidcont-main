import { apiClient } from '@/services/api/client';
import { PromptTemplate, PromptVersion, PromptPreviewRequest } from '../types/prompts_types';

export const promptsApi = {
  getAll: async (params?: Record<string, string>): Promise<PromptTemplate[]> => {
    const queryParams = new URLSearchParams(params);
    const response = await apiClient.get(`/prompts?${queryParams}`);
    return response.data;
  },

  getById: async (id: string): Promise<PromptTemplate> => {
    const response = await apiClient.get(`/prompts/${id}`);
    return response.data;
  },

  create: async (data: Omit<PromptTemplate, 'id' | 'version' | 'created_at' | 'updated_at'>): Promise<PromptTemplate> => {
    const response = await apiClient.post('/prompts', data);
    return response.data;
  },

  update: async (id: string, data: Partial<PromptTemplate>): Promise<PromptTemplate> => {
    const response = await apiClient.put(`/prompts/${id}`, data);
    return response.data;
  },

  delete: async (id: string): Promise<void> => {
    await apiClient.delete(`/prompts/${id}`);
  },

  preview: async (request: PromptPreviewRequest): Promise<string> => {
    const response = await apiClient.post('/prompts/preview', request);
    return response.data.rendered_prompt;
  },

  getVersions: async (id: string): Promise<PromptVersion[]> => {
    const response = await apiClient.get(`/prompts/${id}/versions`);
    return response.data;
  },

  rollback: async (templateId: string, version: number): Promise<PromptTemplate> => {
    const response = await apiClient.post(`/prompts/${templateId}/rollback`, { version });
    return response.data;
  },
};

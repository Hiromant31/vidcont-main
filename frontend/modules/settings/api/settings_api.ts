import { apiClient } from '@/services/api/client';
import { AppSettings } from '../types/settings_types';

export const settingsApi = {
  get: async (): Promise<AppSettings> => {
    const response = await apiClient.get('/settings');
    return response.data;
  },

  update: async (settings: Partial<AppSettings>): Promise<AppSettings> => {
    const response = await apiClient.put('/settings', settings);
    return response.data;
  },

  testConnection: async (): Promise<{ success: boolean; message: string; latency_ms?: number }> => {
    const response = await apiClient.post('/settings/test-connection');
    return response.data;
  },

  getAvailableModels: async (provider: string): Promise<string[]> => {
    const response = await apiClient.get(`/settings/models?provider=${provider}`);
    return response.data.models;
  },
};

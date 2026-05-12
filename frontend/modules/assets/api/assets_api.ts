import { apiClient } from '@/services/api/client';
import { Asset, AssetUsage, AssetsFilters } from '../types/assets_types';

export const assetsApi = {
  getAll: async (params?: AssetsFilters): Promise<Asset[]> => {
    const queryParams = new URLSearchParams();
    if (params?.type && params.type !== 'all') queryParams.append('type', params.type);
    if (params?.status && params.status !== 'all') queryParams.append('status', params.status);
    if (params?.search) queryParams.append('search', params.search);
    
    const response = await apiClient.get(`/assets?${queryParams}`);
    return response.data;
  },

  getById: async (id: string): Promise<Asset> => {
    const response = await apiClient.get(`/assets/${id}`);
    return response.data;
  },

  delete: async (id: string): Promise<void> => {
    await apiClient.delete(`/assets/${id}`);
  },

  reuse: async (assetId: string, targetEntity: { type: string; id: string }): Promise<Asset> => {
    const response = await apiClient.post('/assets/reuse', {
      asset_id: assetId,
      target_entity: targetEntity,
    });
    return response.data;
  },

  getUsage: async (id: string): Promise<AssetUsage[]> => {
    const response = await apiClient.get(`/assets/${id}/usage`);
    return response.data;
  },

  download: async (id: string): Promise<Blob> => {
    const response = await apiClient.get(`/assets/${id}/download`, {
      responseType: 'blob',
    });
    return response.data;
  },
};

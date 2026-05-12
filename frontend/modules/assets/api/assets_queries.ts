import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { assetsApi } from './assets_api';
import { AssetsFilters } from '../types/assets_types';

export const ASSET_KEYS = {
  all: ['assets'] as const,
  lists: () => [...ASSET_KEYS.all, 'list'] as const,
  details: () => [...ASSET_KEYS.all, 'detail'] as const,
  detail: (id: string) => [...ASSET_KEYS.details(), id] as const,
  usage: (id: string) => [...ASSET_KEYS.detail(id), 'usage'] as const,
};

export const useAssets = (filters: AssetsFilters) => {
  return useQuery({
    queryKey: [...ASSET_KEYS.lists(), filters],
    queryFn: () => assetsApi.getAll(filters),
    staleTime: 1000 * 60 * 2, // 2 minutes
  });
};

export const useAsset = (id: string | null) => {
  return useQuery({
    queryKey: id ? ASSET_KEYS.detail(id) : [],
    queryFn: () => assetsApi.getById(id!),
    enabled: !!id,
  });
};

export const useDeleteAsset = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: assetsApi.delete,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ASSET_KEYS.lists() });
    },
  });
};

export const useReuseAsset = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ assetId, target }: { assetId: string; target: { type: string; id: string } }) =>
      assetsApi.reuse(assetId, target),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ASSET_KEYS.lists() });
    },
  });
};

export const useAssetUsage = (id: string | null) => {
  return useQuery({
    queryKey: id ? ASSET_KEYS.usage(id) : [],
    queryFn: () => assetsApi.getUsage(id!),
    enabled: !!id,
  });
};

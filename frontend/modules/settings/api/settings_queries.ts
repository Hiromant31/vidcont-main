import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { settingsApi } from './settings_api';

export const SETTINGS_KEYS = {
  all: ['settings'] as const,
  details: () => [...SETTINGS_KEYS.all, 'detail'] as const,
  models: (provider: string) => [...SETTINGS_KEYS.all, 'models', provider] as const,
};

export const useSettings = () => {
  return useQuery({
    queryKey: SETTINGS_KEYS.details(),
    queryFn: settingsApi.get,
    staleTime: 1000 * 60 * 10, // 10 minutes
  });
};

export const useUpdateSettings = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (settings: any) => settingsApi.update(settings),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: SETTINGS_KEYS.details() });
    },
  });
};

export const useTestConnection = () => {
  return useMutation({
    mutationFn: settingsApi.testConnection,
  });
};

export const useAvailableModels = (provider: string) => {
  return useQuery({
    queryKey: SETTINGS_KEYS.models(provider),
    queryFn: () => settingsApi.getAvailableModels(provider),
    enabled: !!provider,
    staleTime: 1000 * 60 * 30,
  });
};

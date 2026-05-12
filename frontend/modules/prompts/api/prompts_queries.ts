import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { promptsApi } from './prompts_api';
import { PromptsFilters } from '../types/prompts_types';

export const PROMPT_KEYS = {
  all: ['prompts'] as const,
  lists: () => [...PROMPT_KEYS.all, 'list'] as const,
  details: () => [...PROMPT_KEYS.all, 'detail'] as const,
  detail: (id: string) => [...PROMPT_KEYS.details(), id] as const,
  versions: (id: string) => [...PROMPT_KEYS.detail(id), 'versions'] as const,
};

export const usePrompts = (filters: PromptsFilters) => {
  const params: Record<string, string> = {};
  if (filters.category && filters.category !== 'all') params.category = filters.category;
  if (filters.genre) params.genre = filters.genre;
  if (filters.channel) params.channel = filters.channel;
  if (filters.active_only) params.active = 'true';
  if (filters.search) params.search = filters.search;

  return useQuery({
    queryKey: [...PROMPT_KEYS.lists(), params],
    queryFn: () => promptsApi.getAll(params),
    staleTime: 1000 * 60 * 5,
  });
};

export const usePrompt = (id: string | null) => {
  return useQuery({
    queryKey: id ? PROMPT_KEYS.detail(id) : [],
    queryFn: () => promptsApi.getById(id!),
    enabled: !!id,
  });
};

export const useCreatePrompt = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: promptsApi.create,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: PROMPT_KEYS.lists() });
    },
  });
};

export const useUpdatePrompt = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ id, data }: { id: string; data: Partial<PromptTemplate> }) => 
      promptsApi.update(id, data),
    onSuccess: (_, vars) => {
      queryClient.invalidateQueries({ queryKey: PROMPT_KEYS.detail(vars.id) });
      queryClient.invalidateQueries({ queryKey: PROMPT_KEYS.lists() });
    },
  });
};

export const useDeletePrompt = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: promptsApi.delete,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: PROMPT_KEYS.lists() });
    },
  });
};

export const usePromptVersions = (id: string | null) => {
  return useQuery({
    queryKey: id ? PROMPT_KEYS.versions(id) : [],
    queryFn: () => promptsApi.getVersions(id!),
    enabled: !!id,
  });
};

export const usePreviewPrompt = () => {
  return useMutation({
    mutationFn: promptsApi.preview,
  });
};

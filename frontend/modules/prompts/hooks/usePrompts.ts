import { usePrompts as usePromptsQuery } from '../api/prompts_queries';
import { usePromptsStore } from '../stores/prompts_store';

export const usePrompts = (filters: any) => {
  const { searchQuery } = usePromptsStore();
  const finalFilters = { ...filters, search: filters.search || searchQuery };
  
  const { data: prompts, isLoading, error } = usePromptsQuery(finalFilters);
  return { prompts: prompts || [], isLoading, error };
};

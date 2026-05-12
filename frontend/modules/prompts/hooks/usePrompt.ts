import { usePrompt as usePromptQuery } from '../api/prompts_queries';

export const usePrompt = (id: string | null) => {
  const { data: prompt, isLoading, error } = usePromptQuery(id);
  return { prompt, isLoading, error };
};

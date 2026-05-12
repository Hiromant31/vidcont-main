import { usePromptVersions as usePromptVersionsQuery } from '../api/prompts_queries';

export const usePromptVersions = (id: string | null) => {
  const { data: versions, isLoading, error } = usePromptVersionsQuery(id);
  return { versions: versions || [], isLoading, error };
};

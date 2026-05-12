import { useAssetUsage as useAssetUsageQuery } from '../api/assets_queries';

export const useAssetUsage = (id: string | null) => {
  const { data: usages, isLoading, error } = useAssetUsageQuery(id);
  return { usages: usages || [], isLoading, error };
};

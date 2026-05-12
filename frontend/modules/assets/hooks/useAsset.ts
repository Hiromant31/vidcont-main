import { useAsset as useAssetQuery } from '../api/assets_queries';

export const useAsset = (id: string | null) => {
  const { data: asset, isLoading, error } = useAssetQuery(id);
  return { asset, isLoading, error };
};

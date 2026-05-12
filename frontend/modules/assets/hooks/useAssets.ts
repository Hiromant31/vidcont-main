import { useMemo } from 'react';
import { useAssets as useAssetsQuery } from '../api/assets_queries';
import { useAssetsStore } from '../stores/assets_store';
import { filterAssets } from '../utils/assets_filter';

export const useAssetsList = () => {
  const filters = useAssetsStore((state) => state.filters);
  const { data: assets, isLoading, error } = useAssetsQuery(filters);

  const filteredAssets = useMemo(() => {
    if (!assets) return [];
    return filterAssets(assets, filters);
  }, [assets, filters]);

  return { assets: filteredAssets, isLoading, error };
};

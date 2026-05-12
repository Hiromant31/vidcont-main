import { Asset, AssetsFilters } from '../types/assets_types';

export const filterAssets = (assets: Asset[], filters: AssetsFilters): Asset[] => {
  return assets.filter((asset) => {
    if (filters.type && filters.type !== 'all' && asset.type !== filters.type) return false;
    if (filters.status && filters.status !== 'all' && asset.status !== filters.status) return false;
    
    if (filters.search) {
      const searchLower = filters.search.toLowerCase();
      const nameMatch = asset.name?.toLowerCase().includes(searchLower);
      const urlMatch = asset.url.toLowerCase().includes(searchLower);
      const metaMatch = asset.metadata 
        ? JSON.stringify(asset.metadata).toLowerCase().includes(searchLower) 
        : false;
      
      if (!nameMatch && !urlMatch && !metaMatch) return false;
    }

    if (filters.date_from) {
      const assetDate = new Date(asset.created_at).getTime();
      const fromDate = new Date(filters.date_from).getTime();
      if (assetDate < fromDate) return false;
    }

    if (filters.date_to) {
      const assetDate = new Date(asset.created_at).getTime();
      const toDate = new Date(filters.date_to).getTime();
      if (assetDate > toDate) return false;
    }

    return true;
  });
};

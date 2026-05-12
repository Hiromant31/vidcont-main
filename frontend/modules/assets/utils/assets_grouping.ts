import { Asset } from '../types/assets_types';

export const groupAssetsByType = (assets: Asset[]): Record<string, Asset[]> => {
  return assets.reduce((acc, asset) => {
    if (!acc[asset.type]) {
      acc[asset.type] = [];
    }
    acc[asset.type].push(asset);
    return acc;
  }, {} as Record<string, Asset[]>);
};

export const groupAssetsByDate = (assets: Asset[]): Record<string, Asset[]> => {
  return assets.reduce((acc, asset) => {
    const date = new Date(asset.created_at).toLocaleDateString();
    if (!acc[date]) {
      acc[date] = [];
    }
    acc[date].push(asset);
    return acc;
  }, {} as Record<string, Asset[]>);
};

'use client';

import { AssetCard } from './AssetCard';
import { EmptyAssetsState } from './EmptyAssetsState';
import { AssetsLoadingState } from './AssetsLoadingState';
import { useAssetsList } from '../hooks/useAssets';
import { useAssetActions } from '../hooks/useAssetActions';
import { useAssetsStore } from '../stores/assets_store';

export function AssetsGrid() {
  const { assets, isLoading } = useAssetsList();
  const { deleteAsset, reuseAsset } = useAssetActions();
  const { setSelectedAsset, togglePreview } = useAssetsStore();

  if (isLoading) return <AssetsLoadingState />;
  if (assets.length === 0) return <EmptyAssetsState />;

  return (
    <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-4">
      {assets.map((asset) => (
        <AssetCard
          key={asset.id}
          asset={asset}
          onSelect={(id) => { setSelectedAsset(id); togglePreview(id); }}
          onDelete={deleteAsset}
          onReuse={reuseAsset}
        />
      ))}
    </div>
  );
}

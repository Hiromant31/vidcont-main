'use client';

import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { useAssetsStore } from '../stores/assets_store';
import { useAsset } from '../hooks/useAsset';
import { AssetDetailsPanel } from './AssetDetailsPanel';
import { Loader2 } from 'lucide-react';

export function AssetPreviewModal() {
  const { selectedAssetId, isPreviewOpen, togglePreview } = useAssetsStore();
  const { asset, isLoading } = useAsset(selectedAssetId);

  if (!asset) return null;

  return (
    <Dialog open={isPreviewOpen} onOpenChange={() => togglePreview(null)}>
      <DialogContent className="max-w-4xl max-h-[90vh] overflow-y-auto bg-gray-900 border-gray-800 text-white">
        <DialogHeader>
          <DialogTitle>{asset.name || asset.type.toUpperCase()}</DialogTitle>
        </DialogHeader>
        
        <div className="mt-4 space-y-6">
          <div className="bg-black rounded-lg overflow-hidden flex items-center justify-center min-h-[300px]">
            {isLoading ? (
              <Loader2 className="h-8 w-8 animate-spin text-blue-500" />
            ) : asset.type === 'image' || asset.type === 'thumbnail' ? (
              <img src={asset.url} alt="Preview" className="max-h-[500px] w-auto object-contain" />
            ) : asset.type === 'video' ? (
              <video controls src={asset.url} className="max-h-[500px] w-auto" />
            ) : asset.type === 'audio' ? (
              <audio controls src={asset.url} className="w-full" />
            ) : (
              <div className="p-4 text-gray-400">Preview not available for this type</div>
            )}
          </div>
          
          <AssetDetailsPanel asset={asset} />
        </div>
      </DialogContent>
    </Dialog>
  );
}

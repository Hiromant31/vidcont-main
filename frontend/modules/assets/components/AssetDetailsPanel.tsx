'use client';

import { Asset } from '../types/assets_types';
import { formatFileSize, formatDuration } from '../utils/assets_mapper';
import { AssetUsageTimeline } from './AssetUsageTimeline';

interface AssetDetailsPanelProps {
  asset: Asset;
}

export function AssetDetailsPanel({ asset }: AssetDetailsPanelProps) {
  return (
    <div className="space-y-4">
      <div className="grid grid-cols-2 gap-4 text-sm">
        <div>
          <span className="text-gray-500 block">ID</span>
          <span className="font-mono text-blue-400">{asset.id}</span>
        </div>
        <div>
          <span className="text-gray-500 block">Size</span>
          <span>{formatFileSize(asset.size_bytes)}</span>
        </div>
        {asset.duration_sec && (
          <div>
            <span className="text-gray-500 block">Duration</span>
            <span>{formatDuration(asset.duration_sec)}</span>
          </div>
        )}
        <div>
          <span className="text-gray-500 block">Created</span>
          <span>{new Date(asset.created_at).toLocaleDateString()}</span>
        </div>
      </div>
      
      {asset.metadata && (
        <div className="bg-gray-950 p-3 rounded border border-gray-800">
          <h4 className="text-xs font-semibold text-gray-500 uppercase mb-2">Metadata</h4>
          <pre className="text-xs text-gray-300 overflow-auto max-h-32">
            {JSON.stringify(asset.metadata, null, 2)}
          </pre>
        </div>
      )}

      <AssetUsageTimeline assetId={asset.id} />
    </div>
  );
}

'use client';

import { useAssetUsage } from '../hooks/useAssetUsage';
import { Badge } from '@/components/ui/badge';

interface AssetUsageTimelineProps {
  assetId: string;
}

export function AssetUsageTimeline({ assetId }: AssetUsageTimelineProps) {
  const { usages, isLoading } = useAssetUsage(assetId);

  if (isLoading) return <div className="text-sm text-gray-500">Loading usage...</div>;
  if (!usages || usages.length === 0) return null;

  return (
    <div>
      <h4 className="text-xs font-semibold text-gray-500 uppercase mb-2">Used In</h4>
      <div className="flex flex-wrap gap-2">
        {usages.map((usage) => (
          <Badge key={usage.id} variant="outline" className="border-gray-700 text-gray-300">
            {usage.entity_type}: {usage.entity_id}
          </Badge>
        ))}
      </div>
    </div>
  );
}

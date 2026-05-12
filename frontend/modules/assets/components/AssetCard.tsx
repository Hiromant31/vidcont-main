'use client';

import { Card, CardContent,  } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Asset } from '../types/assets_types';
import { formatFileSize, formatDuration, getAssetIcon } from '../utils/assets_mapper';
import { Eye, Trash2, Share2 } from 'lucide-react';

interface AssetCardProps {
  asset: Asset;
  onSelect: (id: string) => void;
  onDelete: (id: string) => void;
  onReuse: (id: string) => void;
}

export function AssetCard({ asset, onSelect, onDelete, onReuse }: AssetCardProps) {
  const isProcessing = asset.status === 'processing';

  return (
    <Card 
      className="group relative overflow-hidden bg-gray-900 border-gray-800 hover:border-blue-500 transition-all cursor-pointer"
      onClick={() => onSelect(asset.id)}
    >
      <div className="aspect-square relative bg-black flex items-center justify-center overflow-hidden">
        {asset.thumbnail_url || asset.type === 'image' ? (
          <img 
            src={asset.thumbnail_url || asset.url} 
            alt={asset.name || asset.id}
            className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
          />
        ) : (
          <div className="text-6xl opacity-50">{getAssetIcon(asset.type)}</div>
        )}
        
        {isProcessing && (
          <div className="absolute inset-0 bg-black/70 flex items-center justify-center">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
          </div>
        )}

        <Badge className="absolute top-2 left-2 bg-black/80 text-white border-0">
          {asset.type.toUpperCase()}
        </Badge>
        
        <div className="absolute inset-0 bg-black/60 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center gap-2">
          <Button size="sm" variant="secondary" onClick={(e) => { e.stopPropagation(); onSelect(asset.id); }}>
            <Eye className="h-4 w-4" />
          </Button>
          <Button size="sm" variant="secondary" onClick={(e) => { e.stopPropagation(); onReuse(asset.id); }}>
            <Share2 className="h-4 w-4" />
          </Button>
          <Button size="sm" variant="destructive" onClick={(e) => { e.stopPropagation(); onDelete(asset.id); }}>
            <Trash2 className="h-4 w-4" />
          </Button>
        </div>
      </div>

      <CardContent className="p-3">
        <div className="text-sm font-medium text-white truncate">{asset.name || asset.id}</div>
        <div className="flex justify-between text-xs text-gray-500 mt-1">
          <span>{formatFileSize(asset.size_bytes)}</span>
          {asset.duration_sec && <span>{formatDuration(asset.duration_sec)}</span>}
        </div>
      </CardContent>
    </Card>
  );
}

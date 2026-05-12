'use client';

import { Tabs, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { useAssetsStore } from '../stores/assets_store';
import { AssetType } from '../types/assets_types';

const types: (AssetType | 'all')[] = ['all', 'image', 'video', 'audio', 'subtitle', 'thumbnail'];

export function AssetTypeTabs() {
  const { filters, setFilter } = useAssetsStore();

  return (
    <Tabs value={filters.type} onValueChange={(v) => setFilter('type', v as AssetType | 'all')}>
      <TabsList className="bg-gray-900 border border-gray-800">
        {types.map((t) => (
          <TabsTrigger key={t} value={t} className="capitalize data-[state=active]:bg-blue-600">
            {t}
          </TabsTrigger>
        ))}
      </TabsList>
    </Tabs>
  );
}

'use client';

import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { useAssetsStore } from '../stores/assets_store';
import { AssetStatus } from '../types/assets_types';

export function AssetFilters() {
  const { filters, setFilter } = useAssetsStore();

  return (
    <Select value={filters.status} onValueChange={(v) => setFilter('status', v as AssetStatus | 'all')}>
      <SelectTrigger className="w-[150px] bg-gray-900 border-gray-800 text-white">
        <SelectValue placeholder="Status" />
      </SelectTrigger>
      <SelectContent className="bg-gray-900 border-gray-800">
        <SelectItem value="all">All Status</SelectItem>
        <SelectItem value="ready">Ready</SelectItem>
        <SelectItem value="processing">Processing</SelectItem>
        <SelectItem value="failed">Failed</SelectItem>
      </SelectContent>
    </Select>
  );
}

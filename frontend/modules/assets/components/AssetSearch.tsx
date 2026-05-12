'use client';

import { Input } from '@/components/ui/input';
import { Search } from 'lucide-react';
import { useAssetsStore } from '../stores/assets_store';

export function AssetSearch() {
  const { filters, setFilter } = useAssetsStore();

  return (
    <div className="relative w-full md:w-64">
      <Search className="absolute left-2 top-1/2 -translate-y-1/2 h-4 w-4 text-gray-500" />
      <Input
        placeholder="Search assets..."
        value={filters.search}
        onChange={(e) => setFilter('search', e.target.value)}
        className="pl-8 bg-gray-900 border-gray-800 text-white"
      />
    </div>
  );
}

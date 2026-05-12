import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Button } from '@/components/ui/button';
import { useAnalyticsStore } from '../stores/analytics_store';
import { Calendar } from 'lucide-react';

export function AnalyticsFilters() {
  const { filters, setFilters, resetFilters } = useAnalyticsStore();

  return (
    <div className="flex flex-wrap gap-2 items-center">
      <div className="flex items-center gap-2 bg-gray-900 border border-gray-800 rounded-md px-3 py-1.5">
        <Calendar className="h-4 w-4 text-gray-400" />
        <span className="text-xs text-gray-400">From: {filters.date_from}</span>
        <span className="text-xs text-gray-600">to</span>
        <span className="text-xs text-gray-400">{filters.date_to}</span>
      </div>

      <Select 
        value={filters.time_range} 
        onValueChange={(value) => setFilters({...filters, time_range: value})}
        disabled={false}
      >
        <SelectTrigger className="w-[120px] h-8 bg-gray-900 border-gray-800 text-xs">
          <SelectValue placeholder="Time Range" />
        </SelectTrigger>
        <SelectContent className="bg-gray-900 border-gray-800">
          <SelectItem value="24h">Last 24h</SelectItem>
          <SelectItem value="7d">Last 7d</SelectItem>
          <SelectItem value="30d">Last 30d</SelectItem>
          <SelectItem value="custom">Custom</SelectItem>
        </SelectContent>
      </Select>

      <Button variant="outline" size="sm" onClick={resetFilters} className="h-8 text-xs border-gray-800 hover:bg-gray-800">
        Reset
      </Button>
    </div>
  );
}

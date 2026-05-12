import { Inbox } from 'lucide-react';

export function EmptyAnalyticsState() {
  return (
    <div className="flex flex-col items-center justify-center py-20 text-center">
      <Inbox className="h-12 w-12 text-gray-700 mb-4" />
      <h3 className="text-lg font-medium text-gray-400">No Analytics Data</h3>
      <p className="text-sm text-gray-600 mt-1 max-w-md">
        There is no data available for the selected time range. Try adjusting your filters or wait for new jobs to complete.
      </p>
    </div>
  );
}

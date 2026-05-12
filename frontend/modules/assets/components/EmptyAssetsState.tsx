import { Inbox } from 'lucide-react';

export function EmptyAssetsState() {
  return (
    <div className="flex flex-col items-center justify-center py-20 text-gray-500">
      <Inbox className="h-12 w-12 mb-4 opacity-50" />
      <p className="text-lg font-medium">No assets found</p>
      <p className="text-sm mt-1">Generate content to see it here.</p>
    </div>
  );
}

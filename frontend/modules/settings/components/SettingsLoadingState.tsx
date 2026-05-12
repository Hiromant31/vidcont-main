import { Skeleton } from '@/components/ui/skeleton';

export function SettingsLoadingState() {
  return (
    <div className="space-y-6">
      <Skeleton className="h-10 w-full" />
      
      <div className="grid grid-cols-1 gap-6">
        <CardSkeleton />
        <CardSkeleton />
        <CardSkeleton />
      </div>
    </div>
  );
}

function CardSkeleton() {
  return (
    <div className="border border-gray-800 rounded-lg p-6 bg-gray-900/50">
      <Skeleton className="h-6 w-32 mb-4" />
      <div className="space-y-4">
        <Skeleton className="h-10 w-full" />
        <Skeleton className="h-10 w-full" />
        <Skeleton className="h-10 w-1/2" />
      </div>
    </div>
  );
}

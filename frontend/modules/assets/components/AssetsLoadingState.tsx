import { Skeleton } from '@/components/ui/skeleton';

export function AssetsLoadingState() {
  return (
    <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-4">
      {[...Array(10)].map((_, i) => (
        <div key={i} className="space-y-2">
          <Skeleton className="aspect-square bg-gray-800" />
          <Skeleton className="h-4 w-3/4 bg-gray-800" />
          <Skeleton className="h-3 w-1/2 bg-gray-800" />
        </div>
      ))}
    </div>
  );
}

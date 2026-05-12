import { cn } from '@/utils/cn';

interface RealtimeIndicatorProps {
  connected: boolean;
  className?: string;
}

export function RealtimeIndicator({ connected, className }: RealtimeIndicatorProps) {
  return (
    <div className={cn('flex items-center space-x-2', className)}>
      <span
        className={cn(
          'h-2 w-2 rounded-full',
          connected ? 'bg-green-500' : 'bg-red-500'
        )}
      />
      <span className="text-xs text-muted-foreground">
        {connected ? 'Realtime Connected' : 'Disconnected'}
      </span>
    </div>
  );
}

import { cn } from '@/utils/cn';

interface ConnectionStatusBadgeProps {
  status: 'idle' | 'testing' | 'connected' | 'disconnected' | 'failed';
}

export function ConnectionStatusBadge({ status }: ConnectionStatusBadgeProps) {
  const config = {
    idle: { color: 'bg-gray-500', text: 'Not Tested' },
    testing: { color: 'bg-yellow-500 animate-pulse', text: 'Testing...' },
    connected: { color: 'bg-green-500', text: 'Connected' },
    disconnected: { color: 'bg-red-500', text: 'Disconnected' },
    failed: { color: 'bg-red-500', text: 'Failed' },
  };

  const { color, text } = config[status];

  return (
    <div className="flex items-center gap-2">
      <div className={cn('h-3 w-3 rounded-full', color)} />
      <span className="text-sm font-medium text-gray-300">{text}</span>
    </div>
  );
}

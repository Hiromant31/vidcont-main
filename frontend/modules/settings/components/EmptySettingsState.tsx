import { Inbox } from 'lucide-react';

export function EmptySettingsState() {
  return (
    <div className="flex flex-col items-center justify-center py-12 text-center">
      <div className="p-4 bg-gray-900 rounded-full mb-4">
        <Inbox className="h-8 w-8 text-gray-600" />
      </div>
      <h3 className="text-lg font-medium text-gray-300 mb-1">No Settings Found</h3>
      <p className="text-gray-500 max-w-md">
        Default settings will be loaded automatically. Configure your AI providers and render options below.
      </p>
    </div>
  );
}

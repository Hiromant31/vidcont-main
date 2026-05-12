import { FileCode } from 'lucide-react';
import { Button } from '@/components/ui/button';

interface EmptyPromptsStateProps {
  onCreateClick?: () => void;
}

export function EmptyPromptsState({ onCreateClick }: EmptyPromptsStateProps) {
  return (
    <div className="flex flex-col items-center justify-center py-12 text-center">
      <div className="p-4 bg-gray-900 rounded-full mb-4">
        <FileCode className="h-8 w-8 text-gray-600" />
      </div>
      <h3 className="text-lg font-medium text-gray-300 mb-1">No prompts found</h3>
      <p className="text-gray-500 mb-4 max-w-md">
        Get started by creating your first prompt template. Use {'{{variable}}'} syntax to make your prompts dynamic.
      </p>
      {onCreateClick && (
        <Button onClick={onCreateClick}>
          Create First Prompt
        </Button>
      )}
    </div>
  );
}

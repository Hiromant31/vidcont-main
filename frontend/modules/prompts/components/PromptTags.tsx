import { Badge } from '@/components/ui/badge';
import { X } from 'lucide-react';

interface PromptTagsProps {
  tags: string[];
  onRemove?: (tag: string) => void;
  variant?: 'outline' | 'default' | 'secondary';
}

export function PromptTags({ tags, onRemove, variant = 'outline' }: PromptTagsProps) {
  if (!tags || tags.length === 0) {
    return <div className="text-gray-500 text-sm">No tags</div>;
  }

  return (
    <div className="flex flex-wrap gap-1">
      {tags.map((tag) => (
        <Badge key={tag} variant={variant} className="text-xs">
          {tag}
          {onRemove && (
            <button 
              onClick={() => onRemove(tag)}
              className="ml-1 hover:bg-gray-700 rounded-full p-0.5"
            >
              <X className="h-3 w-3" />
            </button>
          )}
        </Badge>
      ))}
    </div>
  );
}

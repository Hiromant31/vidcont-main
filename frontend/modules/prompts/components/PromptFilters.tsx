import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Badge } from '@/components/ui/badge';
import { X } from 'lucide-react';
import { usePromptsStore } from '../stores/prompts_store';
import { PromptCategory } from '../types/prompts_types';

export function PromptFilters() {
  const { activeCategory, setActiveCategory } = usePromptsStore();

  const clearFilters = () => {
    setActiveCategory('all');
  };

  return (
    <div className="flex items-center gap-2">
      <Select value={activeCategory} onValueChange={(value: PromptCategory | 'all') => setActiveCategory(value)}>
        <SelectTrigger className="w-32 h-8">
          <SelectValue placeholder="All Categories" />
        </SelectTrigger>
        <SelectContent>
          <SelectItem value="all">All Categories</SelectItem>
          <SelectItem value="story">Story</SelectItem>
          <SelectItem value="characters">Characters</SelectItem>
          <SelectItem value="scenes">Scenes</SelectItem>
          <SelectItem value="tts">TTS</SelectItem>
          <SelectItem value="subtitles">Subtitles</SelectItem>
          <SelectItem value="metadata">Metadata</SelectItem>
          <SelectItem value="render">Render</SelectItem>
        </SelectContent>
      </Select>
      
      {(activeCategory !== 'all') && (
        <Badge variant="secondary" className="text-xs flex items-center gap-1">
          {activeCategory}
          <button onClick={clearFilters} className="ml-1">
            <X className="h-3 w-3" />
          </button>
        </Badge>
      )}
    </div>
  );
}

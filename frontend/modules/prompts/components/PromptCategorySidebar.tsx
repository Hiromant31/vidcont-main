import { usePromptsStore } from '../stores/prompts_store';
import { PromptCategory } from '../types/prompts_types';
import { cn } from '@/utils/cn';
import { FileCode, Users, Film, Mic, Subtitles, Tag, Video, List } from 'lucide-react';

const categories: { key: PromptCategory | 'all'; label: string; icon: any }[] = [
  { key: 'all', label: 'All Prompts', icon: List },
  { key: 'story', label: 'Story', icon: FileCode },
  { key: 'characters', label: 'Characters', icon: Users },
  { key: 'scenes', label: 'Scenes', icon: Film },
  { key: 'tts', label: 'TTS', icon: Mic },
  { key: 'subtitles', label: 'Subtitles', icon: Subtitles },
  { key: 'metadata', label: 'Metadata', icon: Tag },
  { key: 'render', label: 'Render', icon: Video },
];

export function PromptCategorySidebar() {
  const { activeCategory, setActiveCategory } = usePromptsStore();

  return (
    <div className="w-full md:w-48 flex-shrink-0 space-y-1 bg-gray-900 p-4 rounded border border-gray-800 h-fit">
      <h3 className="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-3">Categories</h3>
      {categories.map((cat) => {
        const Icon = cat.icon;
        const isActive = activeCategory === cat.key;
        
        return (
          <button
            key={cat.key}
            onClick={() => setActiveCategory(cat.key)}
            className={cn(
              "w-full flex items-center gap-3 px-3 py-2 rounded text-sm transition-colors",
              isActive 
                ? "bg-blue-600 text-white" 
                : "text-gray-400 hover:bg-gray-800 hover:text-white"
            )}
          >
            <Icon className="h-4 w-4" />
            {cat.label}
          </button>
        );
      })}
    </div>
  );
}

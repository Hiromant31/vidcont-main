import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { PromptTemplate } from '../types/prompts_types';
import { cn } from '@/utils/cn';
import { FileCode, Users, Film, Mic, Subtitles, Tag, Video } from 'lucide-react';

const categoryIcons: Record<string, any> = {
  story: FileCode,
  characters: Users,
  scenes: Film,
  tts: Mic,
  subtitles: Subtitles,
  metadata: Tag,
  render: Video,
};

interface PromptCardProps {
  prompt: PromptTemplate;
  isSelected: boolean;
  onClick: () => void;
}

export function PromptCard({ prompt, isSelected, onClick }: PromptCardProps) {
  const Icon = categoryIcons[prompt.category] || FileCode;

  return (
    <Card 
      onClick={onClick}
      className={cn(
        "cursor-pointer transition-all duration-200 hover:shadow-lg border",
        isSelected 
          ? "border-blue-500 bg-blue-900/10 shadow-blue-900/20" 
          : "border-gray-800 bg-gray-900 hover:border-gray-700"
      )}
    >
      <CardHeader className="pb-2">
        <div className="flex justify-between items-start">
          <div className="flex items-center gap-2">
            <div className="p-2 rounded bg-gray-800 text-blue-400">
              <Icon className="h-4 w-4" />
            </div>
            <CardTitle className="text-base font-semibold text-white line-clamp-1">{prompt.name}</CardTitle>
          </div>
          <Badge variant={prompt.is_active ? "default" : "secondary"} className="scale-75">
            v{prompt.version}
          </Badge>
        </div>
      </CardHeader>
      <CardContent className="space-y-3">
        <div className="text-xs text-gray-400 line-clamp-3 font-mono bg-black/30 p-2 rounded">
          {prompt.content}
        </div>
        <div className="flex flex-wrap gap-1">
          <Badge variant="outline" className="text-[10px] border-gray-700 text-gray-400">
            {prompt.category}
          </Badge>
          {prompt.channel_tags.slice(0, 2).map(tag => (
            <Badge key={tag} variant="outline" className="text-[10px] border-gray-700 text-gray-400">
              #{tag}
            </Badge>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}

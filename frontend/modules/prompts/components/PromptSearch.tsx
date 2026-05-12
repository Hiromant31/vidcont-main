import { Search } from 'lucide-react';
import { Input } from '@/components/ui/input';
import { usePromptsStore } from '../stores/prompts_store';

export function PromptSearch() {
  const { searchQuery, setSearchQuery } = usePromptsStore();

  return (
    <div className="relative w-full md:w-80">
      <Search className="absolute left-2 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-500" />
      <Input
        value={searchQuery}
        onChange={(e) => setSearchQuery(e.target.value)}
        placeholder="Search prompts..."
        className="pl-8 h-9"
      />
    </div>
  );
}

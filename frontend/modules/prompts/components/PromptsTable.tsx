import { PromptCard } from './PromptCard';
import { PromptTemplate } from '../types/prompts_types';
import { EmptyPromptsState } from './EmptyPromptsState';
import { PromptsLoadingState } from './PromptsLoadingState';

interface PromptsTableProps {
  prompts: PromptTemplate[];
  selectedId?: string;
  onSelect: (id: string) => void;
  isLoading: boolean;
}

export function PromptsTable({ prompts, selectedId, onSelect, isLoading }: PromptsTableProps) {
  if (isLoading) return <PromptsLoadingState />;
  if (prompts.length === 0) return <EmptyPromptsState />;

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
      {prompts.map((prompt) => (
        <PromptCard
          key={prompt.id}
          prompt={prompt}
          isSelected={selectedId === prompt.id}
          onClick={() => onSelect(prompt.id)}
        />
      ))}
    </div>
  );
}

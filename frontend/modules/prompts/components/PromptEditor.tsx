'use client';

import { Textarea } from '@/components/ui/textarea';
import { usePromptsStore } from '../stores/prompts_store';
import { PromptValidationPanel } from './PromptValidationPanel';
import { PromptVariablesPanel } from './PromptVariablesPanel';
import { PromptPreview } from './PromptPreview';
import { cn } from '@/utils/cn';

interface PromptEditorProps {
  initialContent?: string;
  readOnly?: boolean;
}

export function PromptEditor({ initialContent = '', readOnly = false }: PromptEditorProps) {
  const { editorContent, setEditorContent } = usePromptsStore();

  const handleChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    if (!readOnly) {
      setEditorContent(e.target.value);
    }
  };

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 h-[600px]">
      <div className="flex flex-col gap-4 h-full">
        <div className="flex-1 relative">
          <Textarea
            value={editorContent}
            onChange={handleChange}
            readOnly={readOnly}
            placeholder="Enter your prompt template here. Use {{variable}} for dynamic values."
            className={cn(
              "w-full h-full font-mono text-sm resize-none bg-gray-900 border-gray-700 text-gray-200 focus:border-blue-500",
              readOnly && "opacity-70 cursor-not-allowed"
            )}
          />
        </div>
        <PromptValidationPanel />
        <PromptVariablesPanel />
      </div>
      
      <div className="h-full">
        <PromptPreview />
      </div>
    </div>
  );
}

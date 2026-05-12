import { useMemo } from 'react';
import { usePromptsStore } from '../stores/prompts_store';
import { generatePreview } from '../utils/prompt_renderer';

export const usePromptPreview = (): string => {
  const { editorContent, previewVariables } = usePromptsStore();

  const preview = useMemo(() => {
    if (!editorContent) return '';
    return generatePreview(editorContent, previewVariables);
  }, [editorContent, previewVariables]);

  return preview;
};

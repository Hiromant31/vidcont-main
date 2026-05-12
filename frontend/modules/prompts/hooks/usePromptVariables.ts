import { useMemo } from 'react';
import { usePromptsStore } from '../stores/prompts_store';
import { parseVariables } from '../utils/variables_parser';

export const usePromptVariables = () => {
  const { editorContent, setEditorVariables } = usePromptsStore();

  const variables = useMemo(() => {
    const parsed = parseVariables(editorContent);
    setEditorVariables(parsed);
    return parsed;
  }, [editorContent, setEditorVariables]);

  return variables;
};

import { useMemo } from 'react';
import { usePromptsStore } from '../stores/prompts_store';
import { validatePrompt } from '../utils/prompt_validator';
import { PromptValidationError } from '../types/prompts_types';

export const usePromptValidation = (): PromptValidationError[] => {
  const { editorContent, editorVariables } = usePromptsStore();

  const errors = useMemo(() => {
    const definedKeys = editorVariables.map((v) => v.key);
    return validatePrompt(editorContent, definedKeys);
  }, [editorContent, editorVariables]);

  return errors;
};

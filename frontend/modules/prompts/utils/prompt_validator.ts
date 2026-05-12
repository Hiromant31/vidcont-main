import { PromptValidationError } from '../types/prompts_types';
import { extractVariableKeys } from './variables_parser';

export const validatePrompt = (content: string, providedVariables?: string[]): PromptValidationError[] => {
  const errors: PromptValidationError[] = [];

  if (!content || content.trim().length === 0) {
    errors.push({
      type: 'EMPTY_CONTENT',
      message: 'Prompt content cannot be empty',
    });
    return errors;
  }

  const foundKeys = extractVariableKeys(content);
  const seen = new Set<string>();

  // Check duplicates
  foundKeys.forEach((key) => {
    if (seen.has(key)) {
      errors.push({
        type: 'DUPLICATE_VARIABLE',
        message: `Duplicate variable found: ${key}`,
        variable: key,
      });
    }
    seen.add(key);
  });

  // Check missing provided variables if context is known
  if (providedVariables) {
    foundKeys.forEach((key) => {
      if (!providedVariables.includes(key)) {
        errors.push({
          type: 'MISSING_VARIABLE',
          message: `Variable "${key}" is used but not defined in schema`,
          variable: key,
        });
      }
    });
  }

  // Basic syntax check for broken braces
  const openBraces = (content.match(/\{/g) || []).length;
  const closeBraces = (content.match(/\}/g) || []).length;
  
  if (openBraces !== closeBraces || openBraces % 2 !== 0) {
    errors.push({
      type: 'INVALID_SYNTAX',
      message: 'Unmatched braces detected. Ensure all {{ }} are closed.',
    });
  }

  return errors;
};

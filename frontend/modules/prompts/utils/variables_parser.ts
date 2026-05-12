const VARIABLE_REGEX = /\{\{([^}]+)\}\}/g;

export const parseVariables = (content: string) => {
  const matches = [...content.matchAll(VARIABLE_REGEX)];
  const uniqueKeys = new Set<string>();
  
  return matches.map((match) => {
    const key = match[1].trim();
    if (!uniqueKeys.has(key)) {
      uniqueKeys.add(key);
      return {
        key,
        description: `Value for ${key}`,
        required: true,
        default_value: '',
      };
    }
    return null;
  }).filter(Boolean);
};

export const extractVariableKeys = (content: string): string[] => {
  const matches = [...content.matchAll(VARIABLE_REGEX)];
  return [...new Set(matches.map((m) => m[1].trim()))];
};

export const renderPrompt = (content: string, values: Record<string, string>): string => {
  return content.replace(VARIABLE_REGEX, (match, key) => {
    const trimmedKey = key.trim();
    return values[trimmedKey] !== undefined ? values[trimmedKey] : match;
  });
};

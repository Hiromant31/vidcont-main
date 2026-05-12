import { PromptTemplate, PromptVariable } from '../types/prompts_types';

export const mapPromptToForm = (prompt: PromptTemplate) => ({
  name: prompt.name,
  category: prompt.category,
  content: prompt.content,
  variables: prompt.variables,
  channel_tags: prompt.channel_tags,
  genre_tags: prompt.genre_tags,
  is_active: prompt.is_active,
});

export const mapFormToPrompt = (formData: any, id?: string): PromptTemplate => {
  const now = new Date().toISOString();
  
  return {
    id: id || crypto.randomUUID(),
    name: formData.name,
    category: formData.category,
    content: formData.content,
    variables: formData.variables || [],
    version: 1,
    channel_tags: formData.channel_tags || [],
    genre_tags: formData.genre_tags || [],
    created_at: now,
    updated_at: now,
    is_active: formData.is_active ?? true,
  };
};

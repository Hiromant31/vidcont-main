export type PromptCategory = 
  | 'story' 
  | 'characters' 
  | 'scenes' 
  | 'tts' 
  | 'subtitles' 
  | 'metadata' 
  | 'render';

export interface PromptVariable {
  key: string;
  description: string;
  required: boolean;
  default_value?: string;
}

export interface PromptTemplate {
  id: string;
  name: string;
  category: PromptCategory;
  content: string;
  variables: PromptVariable[];
  version: number;
  channel_tags: string[];
  genre_tags: string[];
  created_at: string;
  updated_at: string;
  is_active: boolean;
}

export interface PromptVersion {
  id: string;
  template_id: string;
  version: number;
  content: string;
  variables: PromptVariable[];
  created_at: string;
  created_by?: string;
  change_summary?: string;
}

export interface PromptPreviewRequest {
  template_id: string;
  variables: Record<string, string>;
}

export interface PromptValidationError {
  type: 'MISSING_VARIABLE' | 'DUPLICATE_VARIABLE' | 'INVALID_SYNTAX' | 'EMPTY_CONTENT' | 'UNSUPPORTED_PLACEHOLDER';
  message: string;
  line?: number;
  variable?: string;
}

export interface PromptsFilters {
  category?: PromptCategory | 'all';
  genre?: string;
  channel?: string;
  active_only?: boolean;
  search?: string;
}

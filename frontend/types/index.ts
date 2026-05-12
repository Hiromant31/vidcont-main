export interface Project {
  project_id: string;
  name: string;
  description?: string;
  created_at: string;
  updated_at: string;
}

export interface Job {
  job_id: string;
  project_id: string;
  status: 'queued' | 'running' | 'paused' | 'completed' | 'failed';
  current_stage?: string;
  progress: number;
  created_at: string;
  updated_at: string;
  logs?: string[];
  errors?: string[];
}

export interface PromptTemplate {
  template_id: string;
  id?: string;
  name: string;
  stage?: string;
  type?: string;
  content?: string;
  variables: string[];
  version: number | string;
  channel_id?: string;
  genre?: string;
  style?: string;
  prompts?: any[];
  created_at?: string;
  updated_at?: string;
}

export interface Scene {
  scene_id: string;
  story_id: string;
  index: number;
  voice_text: string;
  visual_prompt: string;
  characters?: string[];
  mood?: string;
  style?: string;
  camera_motion?: 'static' | 'zoom_in' | 'zoom_out' | 'pan' | 'shake';
  transition?: 'cut' | 'fade' | 'glitch' | 'blur';
  estimated_duration_sec?: number | null;
  subtitle_text?: string;
}

export interface Character {
  character_id: string;
  story_id: string;
  name: string;
  type: 'human' | 'group' | 'creature' | 'object' | 'abstract';
  description: string;
  visual_prompt: string;
  role: 'main' | 'secondary' | 'background';
  consistency_tag: string;
  created_at: string;
}

export interface RenderJob {
  render_job_id: string;
  job_id: string;
  colab_url: string;
  status: 'queued' | 'uploading' | 'running' | 'processing' | 'completed' | 'failed';
  progress: number;
  created_at: string;
  updated_at: string;
  result_video_url?: string | null;
  logs?: string[];
}

export interface Settings {
  settings_id: string;
  ai_provider: 'openai' | 'yandex' | 'other';
  model: string;
  api_key: string;
  folder_id?: string | null;
  default_quality: '240' | '360' | '480' | '720' | '1080';
  auto_continue_pipeline: boolean;
  created_at: string;
  updated_at: string;
}

export interface WebSocketMessage {
  type: 'job_started' | 'job_progress' | 'stage_completed' | 'stage_failed' | 'render_started' | 'render_completed' | 'logs_updated';
  data: any;
  timestamp: string;
}

export interface PipelineStage {
  name: string;
  status: 'pending' | 'running' | 'completed' | 'failed' | 'skipped';
  started_at?: string;
  completed_at?: string;
  progress?: number;
  message?: string;
  error?: string;
}

export interface PipelineStatus {
  job_id: string;
  status: string;
  current_stage: string | null;
  stages: PipelineStage[];
  progress: number;
  created_at: string;
  updated_at: string;
}

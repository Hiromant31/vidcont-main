export type AIProvider = 
  | 'openai' 
  | 'anthropic' 
  | 'google' 
  | 'yandex' 
  | 'openrouter' 
  | 'custom';

export type Resolution = '240p' | '360p' | '480p' | '720p' | '1080p';
export type Orientation = 'vertical' | 'horizontal' | 'square';

export interface AISettings {
  provider: AIProvider;
  model: string;
  api_key: string;
  yandex_folder_id?: string;
  base_url?: string;
}

export interface TTSSettings {
  provider: string;
  voice: string;
  speed: number;
  pitch: number;
  emotion?: string;
}

export interface RenderSettings {
  resolution: Resolution;
  orientation: Orientation;
  fps: number;
  subtitles_enabled: boolean;
  subtitles_style: string;
}

export interface ColabSettings {
  url: string;
  is_connected: boolean;
  last_ping?: string;
}

export interface PipelineDefaults {
  max_concurrent_jobs: number;
  auto_retry_failed: boolean;
  default_duration_sec: number;
}

export interface AppSettings {
  ai: AISettings;
  tts: TTSSettings;
  render: RenderSettings;
  colab: ColabSettings;
  pipeline: PipelineDefaults;
}

export interface SettingsValidationError {
  field: string;
  message: string;
}

export interface ProviderOption {
  id: AIProvider;
  name: string;
  description: string;
  requires_folder_id: boolean;
  supports_custom_url: boolean;
  default_models: string[];
}

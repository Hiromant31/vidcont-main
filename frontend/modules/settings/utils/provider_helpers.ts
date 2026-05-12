import { ProviderOption } from '../types/settings_types';

export const PROVIDERS: ProviderOption[] = [
  {
    id: 'openai',
    name: 'OpenAI',
    description: 'GPT-4, GPT-3.5 Turbo models',
    requires_folder_id: false,
    supports_custom_url: false,
    default_models: ['gpt-4-turbo', 'gpt-4', 'gpt-3.5-turbo'],
  },
  {
    id: 'anthropic',
    name: 'Anthropic',
    description: 'Claude family of models',
    requires_folder_id: false,
    supports_custom_url: false,
    default_models: ['claude-3-opus', 'claude-3-sonnet', 'claude-3-haiku'],
  },
  {
    id: 'google',
    name: 'Google AI',
    description: 'Gemini and PaLM models',
    requires_folder_id: false,
    supports_custom_url: false,
    default_models: ['gemini-pro', 'gemini-ultra'],
  },
  {
    id: 'yandex',
    name: 'Yandex GPT',
    description: 'Yandex foundation models',
    requires_folder_id: true,
    supports_custom_url: false,
    default_models: ['yandexgpt-lite', 'yandexgpt'],
  },
  {
    id: 'openrouter',
    name: 'OpenRouter',
    description: 'Unified API for multiple providers',
    requires_folder_id: false,
    supports_custom_url: true,
    default_models: ['openai/gpt-4-turbo', 'anthropic/claude-3-opus'],
  },
  {
    id: 'custom',
    name: 'Custom Provider',
    description: 'Self-hosted or other compatible APIs',
    requires_folder_id: false,
    supports_custom_url: true,
    default_models: [],
  },
];

export const getProviderById = (id: string): ProviderOption | undefined => {
  return PROVIDERS.find(p => p.id === id);
};

export const getDefaultSettings = () => ({
  ai: {
    provider: 'openai' as const,
    model: 'gpt-4-turbo',
    api_key: '',
    base_url: '',
  },
  tts: {
    provider: 'elevenlabs',
    voice: 'default',
    speed: 1.0,
    pitch: 1.0,
  },
  render: {
    resolution: '720p' as const,
    orientation: 'vertical' as const,
    fps: 30,
    subtitles_enabled: true,
    subtitles_style: 'default',
  },
  colab: {
    url: '',
    is_connected: false,
  },
  pipeline: {
    max_concurrent_jobs: 3,
    auto_retry_failed: true,
    default_duration_sec: 60,
  },
});

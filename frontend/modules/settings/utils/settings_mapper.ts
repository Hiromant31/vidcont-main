import { getDefaultSettings } from './provider_helpers';
import { AppSettings } from '../types/settings_types';

export const mapSettingsToForm = (settings: AppSettings) => ({
  ai: settings.ai,
  tts: settings.tts,
  render: settings.render,
  colab: settings.colab,
  pipeline: settings.pipeline,
});

export const mapFormToSettings = (formData: any): AppSettings => ({
  ai: {
    provider: formData.ai.provider,
    model: formData.ai.model,
    api_key: formData.ai.api_key,
    yandex_folder_id: formData.ai.yandex_folder_id,
    base_url: formData.ai.base_url,
  },
  tts: {
    provider: formData.tts.provider,
    voice: formData.tts.voice,
    speed: formData.tts.speed,
    pitch: formData.tts.pitch,
    emotion: formData.tts.emotion,
  },
  render: {
    resolution: formData.render.resolution,
    orientation: formData.render.orientation,
    fps: formData.render.fps,
    subtitles_enabled: formData.render.subtitles_enabled,
    subtitles_style: formData.render.subtitles_style,
  },
  colab: {
    url: formData.colab.url,
    is_connected: formData.colab.is_connected,
    last_ping: formData.colab.last_ping,
  },
  pipeline: {
    max_concurrent_jobs: formData.pipeline.max_concurrent_jobs,
    auto_retry_failed: formData.pipeline.auto_retry_failed,
    default_duration_sec: formData.pipeline.default_duration_sec,
  },
});

export const getEmptySettings = (): AppSettings => getDefaultSettings();

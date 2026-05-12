import { AppSettings, SettingsValidationError } from '../types/settings_types';

export const validateSettings = (settings: Partial<AppSettings>): SettingsValidationError[] => {
  const errors: SettingsValidationError[] = [];

  // Validate AI settings
  if (settings.ai) {
    if (!settings.ai.api_key || settings.ai.api_key.trim().length === 0) {
      errors.push({
        field: 'ai.api_key',
        message: 'API Key is required',
      });
    }

    if (settings.ai.provider === 'yandex' && !settings.ai.yandex_folder_id) {
      errors.push({
        field: 'ai.yandex_folder_id',
        message: 'Yandex Folder ID is required for Yandex provider',
      });
    }

    if (settings.ai.base_url && !isValidUrl(settings.ai.base_url)) {
      errors.push({
        field: 'ai.base_url',
        message: 'Invalid URL format',
      });
    }
  }

  // Validate Colab settings
  if (settings.colab?.url && !isValidUrl(settings.colab.url)) {
    errors.push({
      field: 'colab.url',
      message: 'Invalid Colab URL format',
    });
  }

  // Validate Render settings
  if (settings.render) {
    const validResolutions = ['240p', '360p', '480p', '720p', '1080p'];
    if (!validResolutions.includes(settings.render.resolution)) {
      errors.push({
        field: 'render.resolution',
        message: 'Invalid resolution',
      });
    }

    const validOrientations = ['vertical', 'horizontal', 'square'];
    if (!validOrientations.includes(settings.render.orientation)) {
      errors.push({
        field: 'render.orientation',
        message: 'Invalid orientation',
      });
    }

    if (settings.render.fps < 15 || settings.render.fps > 60) {
      errors.push({
        field: 'render.fps',
        message: 'FPS must be between 15 and 60',
      });
    }
  }

  // Validate TTS settings
  if (settings.tts) {
    if (settings.tts.speed < 0.5 || settings.tts.speed > 2.0) {
      errors.push({
        field: 'tts.speed',
        message: 'Speed must be between 0.5 and 2.0',
      });
    }

    if (settings.tts.pitch < 0.5 || settings.tts.pitch > 2.0) {
      errors.push({
        field: 'tts.pitch',
        message: 'Pitch must be between 0.5 and 2.0',
      });
    }
  }

  return errors;
};

const isValidUrl = (url: string): boolean => {
  try {
    new URL(url);
    return true;
  } catch {
    return false;
  }
};

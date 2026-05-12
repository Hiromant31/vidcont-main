import { getDefaultSettings } from './provider_helpers';

export const DEFAULTS = {
  ...getDefaultSettings(),
};

export const RESOLUTIONS = ['240p', '360p', '480p', '720p', '1080p'] as const;
export const ORIENTATIONS = ['vertical', 'horizontal', 'square'] as const;
export const FPS_OPTIONS = [24, 25, 30, 48, 50, 60];

export const getResolutionDimensions = (resolution: string) => {
  const dimensions: Record<string, { width: number; height: number }> = {
    '240p': { width: 426, height: 240 },
    '360p': { width: 640, height: 360 },
    '480p': { width: 854, height: 480 },
    '720p': { width: 1280, height: 720 },
    '1080p': { width: 1920, height: 1080 },
  };
  return dimensions[resolution] || dimensions['720p'];
};

export const getOrientationAspect = (orientation: string) => {
  switch (orientation) {
    case 'vertical':
      return '9:16';
    case 'horizontal':
      return '16:9';
    case 'square':
      return '1:1';
    default:
      return '16:9';
  }
};

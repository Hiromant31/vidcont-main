import { renderPrompt } from './variables_parser';

const MOCK_CONTEXT: Record<string, string> = {
  episodes_count: '12',
  video_duration: '60',
  orientation: 'vertical',
  genre: 'Sci-Fi Cyberpunk',
  channel_name: 'Future Vision',
  mood: 'Dark and Atmospheric',
  style: 'Cinematic Realism',
  character_name: 'Alex',
  scene_description: 'Neon-lit street in rain',
};

export const generatePreview = (content: string, customValues?: Record<string, string>): string => {
  const values = customValues ? { ...MOCK_CONTEXT, ...customValues } : MOCK_CONTEXT;
  return renderPrompt(content, values);
};

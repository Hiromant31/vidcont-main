import { useSettings } from '../api/settings_queries';

export const useAIProviders = () => {
  const { data: settings, isLoading } = useSettings();
  
  const currentProvider = settings?.ai.provider;
  
  return {
    currentProvider,
    isLoading,
  };
};

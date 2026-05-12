import { useSettings } from '../api/settings_queries';

export const useSettingsData = () => {
  const { data: settings, isLoading, error, refetch } = useSettings();
  
  return {
    settings,
    isLoading,
    error,
    refetch,
  };
};

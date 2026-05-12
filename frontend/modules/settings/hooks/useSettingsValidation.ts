import { useSettingsStore } from '../stores/settings_store';

export const useSettingsValidation = () => {
  const { hasUnsavedChanges } = useSettingsStore();
  
  return {
    hasUnsavedChanges,
    canSave: !hasUnsavedChanges ? false : true,
  };
};

'use client';

import { useState } from 'react';
import { useUpdateSettings, useTestConnection } from '../api/settings_queries';
import { useSettingsStore } from '../stores/settings_store';
import { validateSettings } from '../utils/settings_validator';
import { AppSettings } from '../types/settings_types';

export const useSaveSettings = () => {
  const updateMutation = useUpdateSettings();
  const testMutation = useTestConnection();
  const { markAsSaved, setConnectionTesting, setConnectionStatus } = useSettingsStore();
  const [validationErrors, setValidationErrors] = useState<any[]>([]);

  const saveSettings = async (settings: Partial<AppSettings>) => {
    // Validate before saving
    const errors = validateSettings(settings);
    if (errors.length > 0) {
      setValidationErrors(errors);
      return { success: false, errors };
    }

    try {
      await updateMutation.mutateAsync(settings);
      markAsSaved();
      setValidationErrors([]);
      return { success: true, errors: [] };
    } catch (error: any) {
      setValidationErrors([{ field: 'general', message: error.message || 'Failed to save settings' }]);
      return { success: false, errors: [{ field: 'general', message: error.message || 'Failed to save settings' }] };
    }
  };

  const testConnection = async () => {
    setConnectionTesting(true);
    setConnectionStatus('testing');
    
    try {
      const result = await testMutation.mutateAsync();
      if (result.success) {
        setConnectionStatus('connected');
      } else {
        setConnectionStatus('failed');
      }
      return result;
    } catch (error: any) {
      setConnectionStatus('failed');
      return { success: false, message: error.message || 'Connection failed' };
    } finally {
      setConnectionTesting(false);
    }
  };

  return {
    saveSettings,
    testConnection,
    isSaving: updateMutation.isPending,
    isTesting: testMutation.isPending,
    validationErrors,
  };
};

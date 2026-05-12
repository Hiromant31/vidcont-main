'use client';

import { useState, useEffect } from 'react';
import { SettingsTabs } from './SettingsTabs';
import { SaveSettingsButton } from './SaveSettingsButton';
import { AIProviderSettings } from './AIProviderSettings';
import { TTSSettingsPanel } from './TTSSettingsPanel';
import { RenderSettingsPanel } from './RenderSettingsPanel';
import { ColabConnectionPanel } from './ColabConnectionPanel';
import { PipelineDefaultsPanel } from './PipelineDefaultsPanel';
import { SettingsDangerZone } from './SettingsDangerZone';
import { useSettingsData } from '../hooks/useSettings';
import { useSettingsStore } from '../stores/settings_store';
import { getDefaultSettings } from '../utils/provider_helpers';
import { SettingsLoadingState } from './SettingsLoadingState';
import { EmptySettingsState } from './EmptySettingsState';

export function SettingsPage() {
  const { settings, isLoading, error } = useSettingsData();
  const { activeTab } = useSettingsStore();
  const [localSettings, setLocalSettings] = useState<any>(null);

  useEffect(() => {
    if (settings) {
      setLocalSettings(settings);
    } else {
      // Use defaults if no settings loaded
      setLocalSettings(getDefaultSettings());
    }
  }, [settings]);

  const handleChange = (field: string, value: any) => {
    if (!localSettings) return;
    
    const [section, key] = field.split('.');
    setLocalSettings((prev: any) => ({
      ...prev,
      [section]: {
        ...prev[section],
        [key]: value,
      },
    }));
  };

  if (isLoading) {
    return <SettingsLoadingState />;
  }

  if (error || !localSettings) {
    return <EmptySettingsState />;
  }

  const renderContent = () => {
    switch (activeTab) {
      case 'ai':
        return <AIProviderSettings settings={localSettings} onChange={handleChange} />;
      case 'tts':
        return <TTSSettingsPanel settings={localSettings} onChange={handleChange} />;
      case 'render':
        return <RenderSettingsPanel settings={localSettings} onChange={handleChange} />;
      case 'colab':
        return <ColabConnectionPanel settings={localSettings} onChange={handleChange} />;
      case 'pipeline':
        return <PipelineDefaultsPanel settings={localSettings} onChange={handleChange} />;
      default:
        return (
          <div className="space-y-6">
            <p className="text-gray-400">Advanced settings coming soon...</p>
            <SettingsDangerZone />
          </div>
        );
    }
  };

  return (
    <div className="space-y-8 max-w-5xl mx-auto">
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <h1 className="text-3xl font-bold text-white mb-2">Settings</h1>
          <p className="text-gray-400">Configure AI providers, render options, and pipeline defaults</p>
        </div>
        <SaveSettingsButton settings={localSettings} />
      </div>

      <SettingsTabs />

      <div className="min-h-[400px]">
        {renderContent()}
      </div>
    </div>
  );
}

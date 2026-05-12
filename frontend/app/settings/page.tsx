'use client';

import { ModelSettingsPanel } from '@/components/settings/model_settings_panel';

export default function SettingsPage() {
  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold">Model Settings</h1>
      <ModelSettingsPanel />
    </div>
  );
}

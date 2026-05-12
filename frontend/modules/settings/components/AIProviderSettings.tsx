import { Card, CardContent } from '@/components/ui/card';
import { Label } from '@/components/ui/label';
import { Input } from '@/components/ui/input';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { PROVIDERS, getProviderById } from '../utils/provider_helpers';
import { useSettingsStore } from '../stores/settings_store';
import { useAvailableModels } from '../api/settings_queries';
import { AIProvider } from '../types/settings_types';

interface AIProviderSettingsProps {
  settings: any;
  onChange: (field: string, value: any) => void;
}

export function AIProviderSettings({ settings, onChange }: AIProviderSettingsProps) {
  const { markAsChanged } = useSettingsStore();
  const provider = getProviderById(settings.ai.provider);
  const { data: models } = useAvailableModels(settings.ai.provider);

  const handleProviderChange = (value: AIProvider) => {
    markAsChanged();
    onChange('ai.provider', value);
    
    // Auto-select default model for new provider
    const newProvider = getProviderById(value);
    if (newProvider?.default_models[0]) {
      onChange('ai.model', newProvider.default_models[0]);
    }
  };

  return (
    <Card className="bg-gray-900 border-gray-800">
      <CardContent className="space-y-6 pt-6">
        <div className="space-y-2">
          <Label htmlFor="provider">AI Provider</Label>
          <Select value={settings.ai.provider} onValueChange={handleProviderChange}>
            <SelectTrigger id="provider" className="bg-gray-950 border-gray-700">
              <SelectValue />
            </SelectTrigger>
            <SelectContent className="bg-gray-950 border-gray-700">
              {PROVIDERS.map((p) => (
                <SelectItem key={p.id} value={p.id}>
                  {p.name} - {p.description}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>

        <div className="space-y-2">
          <Label htmlFor="model">Model</Label>
          <Select 
            value={settings.ai.model} 
            onValueChange={(v) => { markAsChanged(); onChange('ai.model', v); }}
          >
            <SelectTrigger id="model" className="bg-gray-950 border-gray-700">
              <SelectValue />
            </SelectTrigger>
            <SelectContent className="bg-gray-950 border-gray-700">
              {(models || provider?.default_models || []).map((m: string) => (
                <SelectItem key={m} value={m}>{m}</SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>

        <div className="space-y-2">
          <Label htmlFor="api-key">API Key</Label>
          <Input
            id="api-key"
            type="password"
            value={settings.ai.api_key}
            onChange={(e) => { markAsChanged(); onChange('ai.api_key', e.target.value); }}
            placeholder="sk-..."
            className="bg-gray-950 border-gray-700"
          />
        </div>

        {settings.ai.provider === 'yandex' && (
          <div className="space-y-2">
            <Label htmlFor="folder-id">Yandex Folder ID</Label>
            <Input
              id="folder-id"
              value={settings.ai.yandex_folder_id || ''}
              onChange={(e) => { markAsChanged(); onChange('ai.yandex_folder_id', e.target.value); }}
              placeholder="b1g..."
              className="bg-gray-950 border-gray-700"
            />
          </div>
        )}

        {(settings.ai.provider === 'openrouter' || settings.ai.provider === 'custom') && (
          <div className="space-y-2">
            <Label htmlFor="base-url">Base URL (Optional)</Label>
            <Input
              id="base-url"
              value={settings.ai.base_url || ''}
              onChange={(e) => { markAsChanged(); onChange('ai.base_url', e.target.value); }}
              placeholder="https://api.example.com/v1"
              className="bg-gray-950 border-gray-700"
            />
          </div>
        )}
      </CardContent>
    </Card>
  );
}

'use client';

import { useState } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Badge } from '@/components/ui/badge';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { settingsApi } from '@/services/api/settings';
import type { Settings } from '@/types';

export function ModelSettingsPanel() {
  const queryClient = useQueryClient();
  const [selectedSettingsId, setSelectedSettingsId] = useState<string | null>(null);
  const [isCreating, setIsCreating] = useState(false);
  const [formData, setFormData] = useState({
    settings_id: '',
    ai_provider: 'openai' as const,
    model: 'gpt-4-turbo',
    api_key: '',
    folder_id: '',
    default_quality: '720' as const,
    auto_continue_pipeline: true,
  });

  // Загрузка всех настроек
  const { data: settingsList = [], isLoading } = useQuery({
    queryKey: ['settings'],
    queryFn: () => settingsApi.getAll(),
  });

  // Мутация для создания настроек
  const createMutation = useMutation({
    mutationFn: async () => {
      if (!formData.settings_id.trim()) {
        throw new Error('Settings ID is required');
      }
      return await settingsApi.create({
        settings_id: formData.settings_id,
        ai_provider: formData.ai_provider,
        model: formData.model,
        api_key: formData.api_key,
        folder_id: formData.folder_id || undefined,
        default_quality: formData.default_quality,
        auto_continue_pipeline: formData.auto_continue_pipeline,
      });
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['settings'] });
      setIsCreating(false);
      setFormData({
        settings_id: '',
        ai_provider: 'openai',
        model: 'gpt-4-turbo',
        api_key: '',
        folder_id: '',
        default_quality: '720',
        auto_continue_pipeline: true,
      });
      alert('Settings created successfully!');
    },
    onError: (error: any) => {
      alert(`Failed to create settings: ${error.message}`);
    },
  });

  // Мутация для обновления настроек
  const updateMutation = useMutation({
    mutationFn: async (data: Partial<Settings>) => {
      if (!selectedSettingsId) throw new Error('No settings selected');
      return await settingsApi.update(selectedSettingsId, data);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['settings'] });
      alert('Settings updated successfully!');
    },
    onError: (error: any) => {
      alert(`Failed to update settings: ${error.message}`);
    },
  });

  // Мутация для удаления настроек
  const deleteMutation = useMutation({
    mutationFn: async (id: string) => {
      await settingsApi.delete(id);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['settings'] });
      setSelectedSettingsId(null);
      alert('Settings deleted successfully!');
    },
    onError: (error: any) => {
      alert(`Failed to delete settings: ${error.message}`);
    },
  });

  const handleCreate = (e: React.FormEvent) => {
    e.preventDefault();
    createMutation.mutate();
  };

  const handleUpdate = (field: keyof Settings, value: any) => {
    updateMutation.mutate({ [field]: value });
  };

  const handleDelete = (id: string) => {
    if (confirm('Are you sure you want to delete these settings?')) {
      deleteMutation.mutate(id);
    }
  };

  const selectedSettings = settingsList.find(s => s.settings_id === selectedSettingsId);

  if (isLoading) {
    return <Card><CardContent className="p-6">Loading settings...</CardContent></Card>;
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Model Settings</CardTitle>
      </CardHeader>
      <CardContent className="space-y-6">
        {/* Список существующих настроек */}
        <div className="space-y-2">
          <Label>Existing Settings</Label>
          <div className="flex flex-wrap gap-2">
            {settingsList.length === 0 ? (
              <span className="text-sm text-gray-500">No settings found. Create your first settings below.</span>
            ) : (
              settingsList.map((settings) => (
                <Badge
                  key={settings.settings_id}
                  variant={selectedSettingsId === settings.settings_id ? 'default' : 'outline'}
                  className="cursor-pointer"
                  onClick={() => setSelectedSettingsId(settings.settings_id)}
                >
                  {settings.settings_id}
                </Badge>
              ))
            )}
          </div>
        </div>

        {/* Форма создания новых настроек */}
        {!isCreating && !selectedSettingsId && (
          <Button onClick={() => setIsCreating(true)} className="w-full">
            + Create New Settings
          </Button>
        )}

        {isCreating && (
          <form onSubmit={handleCreate} className="space-y-4 p-4 border rounded-lg bg-gray-50">
            <h4 className="font-medium">Create New Settings</h4>
            
            <div className="space-y-2">
              <Label htmlFor="settings_id">Settings ID</Label>
              <Input
                id="settings_id"
                placeholder="e.g., settings_default"
                value={formData.settings_id}
                onChange={(e) => setFormData({ ...formData, settings_id: e.target.value })}
                disabled={createMutation.isPending}
              />
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="ai_provider">AI Provider</Label>
                <Select
                  value={formData.ai_provider}
                  onValueChange={(value: any) => setFormData({ ...formData, ai_provider: value })}
                  disabled={createMutation.isPending}
                >
                  <SelectTrigger id="ai_provider" className="w-full">
                    <SelectValue placeholder="Select provider" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="openai">OpenAI</SelectItem>
                    <SelectItem value="yandex">Yandex</SelectItem>
                    <SelectItem value="other">Other</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <Label htmlFor="model">Model</Label>
                <Input
                  id="model"
                  placeholder="e.g., gpt-4-turbo"
                  value={formData.model}
                  onChange={(e) => setFormData({ ...formData, model: e.target.value })}
                  disabled={createMutation.isPending}
                />
              </div>
            </div>

            <div className="space-y-2">
              <Label htmlFor="api_key">API Key</Label>
              <Input
                id="api_key"
                type="password"
                placeholder="sk-..."
                value={formData.api_key}
                onChange={(e) => setFormData({ ...formData, api_key: e.target.value })}
                disabled={createMutation.isPending}
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="folder_id">Folder ID (Optional)</Label>
              <Input
                id="folder_id"
                placeholder="Yandex folder ID"
                value={formData.folder_id}
                onChange={(e) => setFormData({ ...formData, folder_id: e.target.value })}
                disabled={createMutation.isPending}
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="default_quality">Default Quality</Label>
              <Select
                value={formData.default_quality}
                onValueChange={(value: any) => setFormData({ ...formData, default_quality: value })}
                disabled={createMutation.isPending}
              >
                <SelectTrigger id="default_quality" className="w-full">
                  <SelectValue placeholder="Select quality" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="240">240p</SelectItem>
                  <SelectItem value="360">360p</SelectItem>
                  <SelectItem value="480">480p</SelectItem>
                  <SelectItem value="720">720p HD</SelectItem>
                  <SelectItem value="1080">1080p Full HD</SelectItem>
                </SelectContent>
              </Select>
            </div>

            <div className="flex items-center space-x-2">
              <input
                type="checkbox"
                id="auto_continue"
                checked={formData.auto_continue_pipeline}
                onChange={(e) => setFormData({ ...formData, auto_continue_pipeline: e.target.checked })}
                disabled={createMutation.isPending}
                className="h-4 w-4"
              />
              <Label htmlFor="auto_continue">Auto-continue Pipeline</Label>
            </div>

            <div className="flex gap-2">
              <Button type="submit" disabled={createMutation.isPending} className="flex-1">
                {createMutation.isPending ? 'Creating...' : 'Create Settings'}
              </Button>
              <Button type="button" variant="outline" onClick={() => setIsCreating(false)}>
                Cancel
              </Button>
            </div>
          </form>
        )}

        {/* Просмотр и редактирование выбранных настроек */}
        {selectedSettings && (
          <div className="space-y-4 p-4 border rounded-lg bg-blue-50">
            <div className="flex justify-between items-center">
              <h4 className="font-medium">Editing: {selectedSettings.settings_id}</h4>
              <Button variant="destructive" size="sm" onClick={() => handleDelete(selectedSettings.settings_id)}>
                Delete
              </Button>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label>AI Provider</Label>
                <div className="flex items-center gap-2">
                  <Badge>{selectedSettings.ai_provider}</Badge>
                </div>
              </div>

              <div className="space-y-2">
                <Label>Model</Label>
                <div className="text-sm">{selectedSettings.model}</div>
              </div>

              <div className="space-y-2">
                <Label>API Key</Label>
                <div className="text-sm font-mono">••••••••{selectedSettings.api_key.slice(-4)}</div>
              </div>

              <div className="space-y-2">
                <Label>Folder ID</Label>
                <div className="text-sm">{selectedSettings.folder_id || 'Not set'}</div>
              </div>

              <div className="space-y-2">
                <Label>Default Quality</Label>
                <div className="flex items-center gap-2">
                  <Select
                    value={selectedSettings.default_quality}
                    onValueChange={(value) => handleUpdate('default_quality', value)}
                    disabled={updateMutation.isPending}
                  >
                    <SelectTrigger className="w-[120px]">
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="240">240p</SelectItem>
                      <SelectItem value="360">360p</SelectItem>
                      <SelectItem value="480">480p</SelectItem>
                      <SelectItem value="720">720p</SelectItem>
                      <SelectItem value="1080">1080p</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </div>

              <div className="space-y-2">
                <Label>Auto-continue Pipeline</Label>
                <div className="flex items-center space-x-2">
                  <input
                    type="checkbox"
                    checked={selectedSettings.auto_continue_pipeline}
                    onChange={(e) => handleUpdate('auto_continue_pipeline', e.target.checked)}
                    disabled={updateMutation.isPending}
                    className="h-4 w-4"
                  />
                  <span className="text-sm">{selectedSettings.auto_continue_pipeline ? 'Enabled' : 'Disabled'}</span>
                </div>
              </div>
            </div>

            <div className="text-xs text-gray-500">
              Created: {new Date(selectedSettings.created_at).toLocaleDateString()} | 
              Updated: {new Date(selectedSettings.updated_at).toLocaleDateString()}
            </div>

            <Button variant="outline" onClick={() => setSelectedSettingsId(null)} className="w-full">
              Close
            </Button>
          </div>
        )}
      </CardContent>
    </Card>
  );
}

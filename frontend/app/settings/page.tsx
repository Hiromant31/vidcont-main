'use client';

import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { settingsApi } from '@/services/api/settings';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import type { Settings } from '@/types';

export default function SettingsPage() {
  const queryClient = useQueryClient();

  const { data: settingsList, isLoading, error } = useQuery({
    queryKey: ['settings'],
    queryFn: () => settingsApi.get(),
  });

  const settings = settingsList?.[0] || null;

  const createMutation = useMutation({
    mutationFn: (data: Partial<Settings>) => settingsApi.create(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['settings'] });
      alert('Settings created successfully!');
    },
    onError: (error) => {
      alert(`Failed to create settings: ${error.message}`);
    },
  });

  const updateMutation = useMutation({
    mutationFn: ({ id, data }: { id: string; data: Partial<Settings> }) => 
      settingsApi.update(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['settings'] });
      alert('Settings updated successfully!');
    },
    onError: (error) => {
      alert(`Failed to update settings: ${error.message}`);
    },
  });

  const deleteMutation = useMutation({
    mutationFn: (id: string) => settingsApi.delete(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['settings'] });
      alert('Settings deleted successfully!');
    },
    onError: (error) => {
      alert(`Failed to delete settings: ${error.message}`);
    },
  });

  if (isLoading) return <div>Loading...</div>;
  if (error) return <div>Error loading settings: {error.message}</div>;

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold">Settings</h1>

      {!settings ? (
        <Card>
          <CardHeader>
            <CardTitle>No Settings Found</CardTitle>
          </CardHeader>
          <CardContent>
            <Button 
              onClick={() => createMutation.mutate({
                settings_id: `settings-${Date.now()}`,
                ai_provider: "openai",
                model: "gpt-4",
                api_key: "",
                default_quality: "1080",
                auto_continue_pipeline: true,
              })}
            >
              Create Default Settings
            </Button>
          </CardContent>
        </Card>
      ) : (
        <Card>
          <CardHeader>
            <CardTitle>AI Provider Settings</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div>
              <label className="text-sm font-medium">Provider</label>
              <p className="text-muted-foreground">{settings.ai_provider}</p>
            </div>
            <div>
              <label className="text-sm font-medium">Model</label>
              <p className="text-muted-foreground">{settings.model}</p>
            </div>
            <div>
              <label className="text-sm font-medium">Default Quality</label>
              <p className="text-muted-foreground">{settings.default_quality}p</p>
            </div>
            <div>
              <label className="text-sm font-medium">Auto Continue Pipeline</label>
              <p className="text-muted-foreground">
                {settings.auto_continue_pipeline ? 'Yes' : 'No'}
              </p>
            </div>
            <div className="flex gap-2">
              <Button 
                onClick={() => updateMutation.mutate({ 
                  id: settings.settings_id, 
                  data: { auto_continue_pipeline: !settings.auto_continue_pipeline } 
                })}
              >
                Toggle Auto Continue
              </Button>
              <Button 
                variant="destructive"
                onClick={() => deleteMutation.mutate(settings.settings_id)}
              >
                Delete Settings
              </Button>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
}

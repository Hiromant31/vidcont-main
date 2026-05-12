'use client';

import { useEffect } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { settingsApi } from '@/modules/settings/api/settings_api';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import type { AppSettings } from '@/modules/settings/types/settings_types';

export default function SettingsPage() {
  const queryClient = useQueryClient();

  const { data: appSettings, isLoading, error } = useQuery({
    queryKey: ['app-settings'],
    queryFn: () => settingsApi.get(),
  });

  const updateMutation = useMutation({
    mutationFn: (data: Partial<AppSettings>) => settingsApi.update(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['app-settings'] });
      alert('Settings updated successfully!');
    },
    onError: (error) => {
      alert(`Failed to update settings: ${error.message}`);
    },
  });

  const createMutation = useMutation({
    mutationFn: (data: Partial<AppSettings>) => settingsApi.update(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['app-settings'] });
      alert('Settings created successfully!');
    },
    onError: (error) => {
      alert(`Failed to create settings: ${error.message}`);
    },
  });

  if (isLoading) return <div>Loading...</div>;
  if (error) return <div>Error loading settings: {error.message}</div>;

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold">Settings</h1>

      {!appSettings ? (
        <Card>
          <CardHeader>
            <CardTitle>No Settings Found</CardTitle>
          </CardHeader>
          <CardContent>
            <Button onClick={() => createMutation.mutate({} as any)}>
              Create Default Settings
            </Button>
          </CardContent>
        </Card>
      ) : (
        <div className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>AI Provider</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <label className="text-sm font-medium">Provider</label>
                <p className="text-muted-foreground">{appSettings.ai.provider}</p>
              </div>
              <div>
                <label className="text-sm font-medium">Model</label>
                <p className="text-muted-foreground">{appSettings.ai.model}</p>
              </div>
              <div>
                <label className="text-sm font-medium">API Key</label>
                <p className="text-muted-foreground">••••••••{appSettings.ai.api_key.slice(-4)}</p>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Pipeline Defaults</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <label className="text-sm font-medium">Max Concurrent Jobs</label>
                <p className="text-muted-foreground">{appSettings.pipeline.max_concurrent_jobs}</p>
              </div>
              <div>
                <label className="text-sm font-medium">Auto Retry Failed</label>
                <p className="text-muted-foreground">{appSettings.pipeline.auto_retry_failed ? 'Yes' : 'No'}</p>
              </div>
            </CardContent>
          </Card>

          <Button
            variant="outline"
            onClick={() => updateMutation.mutate({
              pipeline: { ...appSettings.pipeline, auto_retry_failed: !appSettings.pipeline.auto_retry_failed }
            })}
          >
            Toggle Auto Retry
          </Button>
        </div>
      )}
    </div>
  );
}

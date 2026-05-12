import { Card, CardContent } from '@/components/ui/card';
import { Label } from '@/components/ui/label';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { ConnectionStatusBadge } from './ConnectionStatusBadge';
import { useSettingsStore } from '../stores/settings_store';
import { useSaveSettings } from '../hooks/useSaveSettings';

interface ColabConnectionPanelProps {
  settings: any;
  onChange: (field: string, value: any) => void;
}

export function ColabConnectionPanel({ settings, onChange }: ColabConnectionPanelProps) {
  const { markAsChanged } = useSettingsStore();
  const { testConnection } = useSaveSettings();
  const { connectionStatus } = useSettingsStore();

  return (
    <Card className="bg-gray-900 border-gray-800">
      <CardContent className="space-y-6 pt-6">
        <div className="flex items-center justify-between">
          <Label htmlFor="colab-url">Colab Server URL</Label>
          <ConnectionStatusBadge status={connectionStatus} />
        </div>
        
        <div className="space-y-2">
          <Input
            id="colab-url"
            placeholder="https://your-ngrok-url.ngrok.io"
            value={settings.colab.url}
            onChange={(e) => { markAsChanged(); onChange('colab.url', e.target.value); }}
            className="bg-gray-950 border-gray-700 font-mono"
          />
          <p className="text-xs text-gray-500">
            Enter your ngrok or Cloudflare tunnel URL for the Colab render server.
          </p>
        </div>

        <div className="flex gap-3">
          <Button 
            onClick={testConnection}
            variant="outline"
            className="border-blue-600 text-blue-400 hover:bg-blue-950"
          >
            Test Connection
          </Button>
          
          {settings.colab.is_connected && (
            <span className="text-sm text-green-400 flex items-center">
              ✓ Connected
            </span>
          )}
        </div>
      </CardContent>
    </Card>
  );
}

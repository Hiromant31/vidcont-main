import { Card, CardContent } from '@/components/ui/card';
import { Label } from '@/components/ui/label';
import { Input } from '@/components/ui/input';
import { Switch } from '@/components/ui/switch';

interface PipelineDefaultsPanelProps {
  settings: any;
  onChange: (field: string, value: any) => void;
}

export function PipelineDefaultsPanel({ settings, onChange }: PipelineDefaultsPanelProps) {
  return (
    <Card className="bg-gray-900 border-gray-800">
      <CardContent className="space-y-6 pt-6">
        <div className="space-y-2">
          <Label htmlFor="max-jobs">Max Concurrent Jobs</Label>
          <Input
            id="max-jobs"
            type="number"
            min={1}
            max={10}
            value={settings.pipeline.max_concurrent_jobs}
            onChange={(e) => onChange('pipeline.max_concurrent_jobs', parseInt(e.target.value) || 3)}
            className="bg-gray-950 border-gray-700 w-32"
          />
          <p className="text-xs text-gray-500">Maximum number of jobs that can run simultaneously.</p>
        </div>

        <div className="flex items-center justify-between p-4 bg-gray-950 rounded border border-gray-800">
          <div>
            <Label htmlFor="auto-retry" className="text-base font-medium">Auto-Retry Failed Jobs</Label>
            <p className="text-sm text-gray-500">Automatically retry failed stages up to 3 times</p>
          </div>
          <Switch
            id="auto-retry"
            checked={settings.pipeline.auto_retry_failed}
            onCheckedChange={(v) => onChange('pipeline.auto_retry_failed', v)}
          />
        </div>

        <div className="space-y-2">
          <Label htmlFor="default-duration">Default Video Duration (seconds)</Label>
          <Input
            id="default-duration"
            type="number"
            min={15}
            max={300}
            value={settings.pipeline.default_duration_sec}
            onChange={(e) => onChange('pipeline.default_duration_sec', parseInt(e.target.value) || 60)}
            className="bg-gray-950 border-gray-700 w-32"
          />
        </div>
      </CardContent>
    </Card>
  );
}

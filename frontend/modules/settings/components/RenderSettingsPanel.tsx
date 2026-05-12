import { Card, CardContent } from '@/components/ui/card';
import { Label } from '@/components/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Input } from '@/components/ui/input';
import { Switch } from '@/components/ui/switch';

interface RenderSettingsPanelProps {
  settings: any;
  onChange: (field: string, value: any) => void;
}

export function RenderSettingsPanel({ settings, onChange }: RenderSettingsPanelProps) {
  return (
    <Card className="bg-gray-900 border-gray-800">
      <CardContent className="space-y-6 pt-6">
        <div className="grid grid-cols-2 gap-4">
          <div className="space-y-2">
            <Label htmlFor="resolution">Resolution</Label>
            <Select 
              value={settings.render.resolution} 
              onValueChange={(v) => onChange('render.resolution', v)}
            >
              <SelectTrigger id="resolution" className="bg-gray-950 border-gray-700">
                <SelectValue />
              </SelectTrigger>
              <SelectContent className="bg-gray-950 border-gray-700">
                <SelectItem value="240p">240p</SelectItem>
                <SelectItem value="360p">360p</SelectItem>
                <SelectItem value="480p">480p</SelectItem>
                <SelectItem value="720p">720p (HD)</SelectItem>
                <SelectItem value="1080p">1080p (Full HD)</SelectItem>
              </SelectContent>
            </Select>
          </div>

          <div className="space-y-2">
            <Label htmlFor="orientation">Orientation</Label>
            <Select 
              value={settings.render.orientation} 
              onValueChange={(v) => onChange('render.orientation', v)}
            >
              <SelectTrigger id="orientation" className="bg-gray-950 border-gray-700">
                <SelectValue />
              </SelectTrigger>
              <SelectContent className="bg-gray-950 border-gray-700">
                <SelectItem value="vertical">📱 Vertical (9:16)</SelectItem>
                <SelectItem value="horizontal">🖥️ Horizontal (16:9)</SelectItem>
                <SelectItem value="square">📷 Square (1:1)</SelectItem>
              </SelectContent>
            </Select>
          </div>
        </div>

        <div className="space-y-2">
          <Label htmlFor="fps">FPS (Frames Per Second)</Label>
          <Input
            id="fps"
            type="number"
            min={15}
            max={60}
            value={settings.render.fps}
            onChange={(e) => onChange('render.fps', parseInt(e.target.value) || 30)}
            className="bg-gray-950 border-gray-700 w-32"
          />
        </div>

        <div className="flex items-center justify-between p-4 bg-gray-950 rounded border border-gray-800">
          <div>
            <Label htmlFor="subtitles" className="text-base font-medium">Enable Subtitles</Label>
            <p className="text-sm text-gray-500">Automatically generate and burn subtitles</p>
          </div>
          <Switch
            id="subtitles"
            checked={settings.render.subtitles_enabled}
            onCheckedChange={(v) => onChange('render.subtitles_enabled', v)}
          />
        </div>

        {settings.render.subtitles_enabled && (
          <div className="space-y-2">
            <Label htmlFor="subtitle-style">Subtitle Style</Label>
            <Select 
              value={settings.render.subtitles_style} 
              onValueChange={(v) => onChange('render.subtitles_style', v)}
            >
              <SelectTrigger id="subtitle-style" className="bg-gray-950 border-gray-700">
                <SelectValue />
              </SelectTrigger>
              <SelectContent className="bg-gray-950 border-gray-700">
                <SelectItem value="default">Default (White with Black Border)</SelectItem>
                <SelectItem value="minimal">Minimal (Plain White)</SelectItem>
                <SelectItem value="bold">Bold (Large Text)</SelectItem>
                <SelectItem value="cinematic">Cinematic (Bottom Bar)</SelectItem>
              </SelectContent>
            </Select>
          </div>
        )}
      </CardContent>
    </Card>
  );
}

import { Card, CardContent } from '@/components/ui/card';
import { Label } from '@/components/ui/label';
import { Input } from '@/components/ui/input';
import { Slider } from '@/components/ui/slider';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';

interface TTSSettingsPanelProps {
  settings: any;
  onChange: (field: string, value: any) => void;
}

export function TTSSettingsPanel({ settings, onChange }: TTSSettingsPanelProps) {
  return (
    <Card className="bg-gray-900 border-gray-800">
      <CardContent className="space-y-6 pt-6">
        <div className="space-y-2">
          <Label htmlFor="tts-provider">TTS Provider</Label>
          <Select 
            value={settings.tts.provider} 
            onValueChange={(v) => onChange('tts.provider', v)}
          >
            <SelectTrigger id="tts-provider" className="bg-gray-950 border-gray-700">
              <SelectValue />
            </SelectTrigger>
            <SelectContent className="bg-gray-950 border-gray-700">
              <SelectItem value="elevenlabs">ElevenLabs</SelectItem>
              <SelectItem value="openai">OpenAI TTS</SelectItem>
              <SelectItem value="google">Google TTS</SelectItem>
              <SelectItem value="azure">Azure TTS</SelectItem>
            </SelectContent>
          </Select>
        </div>

        <div className="space-y-2">
          <Label htmlFor="voice">Voice</Label>
          <Input
            id="voice"
            value={settings.tts.voice}
            onChange={(e) => onChange('tts.voice', e.target.value)}
            placeholder="Voice ID or name"
            className="bg-gray-950 border-gray-700"
          />
        </div>

        <div className="space-y-4">
          <div>
            <div className="flex justify-between mb-2">
              <Label>Speed</Label>
              <span className="text-sm text-gray-400">{settings.tts.speed}x</span>
            </div>
            <Slider
              value={[settings.tts.speed]}
              onValueChange={([v]) => onChange('tts.speed', v)}
              min={0.5}
              max={2.0}
              step={0.1}
              className="w-full"
            />
          </div>

          <div>
            <div className="flex justify-between mb-2">
              <Label>Pitch</Label>
              <span className="text-sm text-gray-400">{settings.tts.pitch}x</span>
            </div>
            <Slider
              value={[settings.tts.pitch]}
              onValueChange={([v]) => onChange('tts.pitch', v)}
              min={0.5}
              max={2.0}
              step={0.1}
              className="w-full"
            />
          </div>
        </div>

        <div className="space-y-2">
          <Label htmlFor="emotion">Emotion (Optional)</Label>
          <Select 
            value={settings.tts.emotion || 'neutral'} 
            onValueChange={(v) => onChange('tts.emotion', v)}
          >
            <SelectTrigger id="emotion" className="bg-gray-950 border-gray-700">
              <SelectValue />
            </SelectTrigger>
            <SelectContent className="bg-gray-950 border-gray-700">
              <SelectItem value="neutral">Neutral</SelectItem>
              <SelectItem value="happy">Happy</SelectItem>
              <SelectItem value="sad">Sad</SelectItem>
              <SelectItem value="angry">Angry</SelectItem>
              <SelectItem value="excited">Excited</SelectItem>
            </SelectContent>
          </Select>
        </div>
      </CardContent>
    </Card>
  );
}

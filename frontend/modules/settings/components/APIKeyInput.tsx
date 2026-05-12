import { Card, CardContent } from '@/components/ui/card';
import { Label } from '@/components/ui/label';
import { Input } from '@/components/ui/input';

interface APIKeyInputProps {
  value: string;
  onChange: (value: string) => void;
  provider: string;
}

export function APIKeyInput({ value, onChange, provider }: APIKeyInputProps) {
  return (
    <div className="space-y-2">
      <Label htmlFor="api-key-input">API Key for {provider}</Label>
      <Input
        id="api-key-input"
        type="password"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder={`Enter your ${provider} API key`}
        className="bg-gray-950 border-gray-700 font-mono"
      />
    </div>
  );
}

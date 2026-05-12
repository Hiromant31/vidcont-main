import { Card, CardContent } from '@/components/ui/card';
import { Label } from '@/components/ui/label';
import { Input } from '@/components/ui/input';

interface YandexFolderInputProps {
  value: string;
  onChange: (value: string) => void;
}

export function YandexFolderInput({ value, onChange }: YandexFolderInputProps) {
  return (
    <div className="space-y-2">
      <Label htmlFor="yandex-folder">Yandex Folder ID</Label>
      <Input
        id="yandex-folder"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder="b1g..."
        className="bg-gray-950 border-gray-700 font-mono"
      />
      <p className="text-xs text-gray-500">
        Required for Yandex GPT provider. Find your folder ID in Yandex Cloud Console.
      </p>
    </div>
  );
}

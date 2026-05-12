import { Card, CardContent } from '@/components/ui/card';
import { AlertTriangle } from 'lucide-react';

export function SettingsDangerZone() {
  const handleReset = () => {
    if (confirm('Are you sure you want to reset all settings to defaults? This cannot be undone.')) {
      // Reset logic would go here
      console.log('Resetting settings...');
    }
  };

  return (
    <Card className="bg-red-950/10 border-red-900/50">
      <CardContent className="pt-6">
        <div className="flex items-start gap-4">
          <AlertTriangle className="h-6 w-6 text-red-500 shrink-0" />
          <div className="space-y-2 flex-1">
            <h3 className="text-lg font-semibold text-red-400">Danger Zone</h3>
            <p className="text-sm text-gray-400">
              These actions are irreversible. Please proceed with caution.
            </p>
            <button
              onClick={handleReset}
              className="px-4 py-2 bg-red-900/30 hover:bg-red-900/50 text-red-400 border border-red-900 rounded-md text-sm transition-colors"
            >
              Reset All Settings to Defaults
            </button>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}

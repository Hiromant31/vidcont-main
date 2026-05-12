import { Button } from '@/components/ui/button';
import { useSettingsStore } from '../stores/settings_store';
import { useSaveSettings } from '../hooks/useSaveSettings';
import { cn } from '@/utils/cn';

interface SaveSettingsButtonProps {
  settings: any;
}

export function SaveSettingsButton({ settings }: SaveSettingsButtonProps) {
  const { hasUnsavedChanges } = useSettingsStore();
  const { saveSettings, isSaving } = useSaveSettings();

  const handleSave = async () => {
    await saveSettings(settings);
  };

  return (
    <div className="flex items-center gap-4">
      <Button
        onClick={handleSave}
        disabled={!hasUnsavedChanges || isSaving}
        className={cn(
          "transition-all",
          hasUnsavedChanges && !isSaving && "bg-blue-600 hover:bg-blue-700"
        )}
      >
        {isSaving ? 'Saving...' : 'Save Changes'}
      </Button>
      
      {hasUnsavedChanges && (
        <span className="text-sm text-yellow-500">You have unsaved changes</span>
      )}
    </div>
  );
}

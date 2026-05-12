import { Tabs, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { useSettingsStore } from '../stores/settings_store';

const tabs = [
  { id: 'ai', label: 'AI Provider' },
  { id: 'tts', label: 'TTS' },
  { id: 'render', label: 'Render' },
  { id: 'colab', label: 'Colab' },
  { id: 'pipeline', label: 'Pipeline' },
  { id: 'advanced', label: 'Advanced' },
];

export function SettingsTabs() {
  const { activeTab, setActiveTab } = useSettingsStore();

  return (
    <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
      <TabsList className="grid grid-cols-2 md:grid-cols-6 bg-gray-900 border border-gray-800">
        {tabs.map((tab) => (
          <TabsTrigger
            key={tab.id}
            value={tab.id}
            className="data-[state=active]:bg-blue-600 data-[state=active]:text-white text-gray-400"
          >
            {tab.label}
          </TabsTrigger>
        ))}
      </TabsList>
    </Tabs>
  );
}

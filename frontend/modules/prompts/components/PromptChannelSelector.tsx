import { MultiSelect } from '@/components/ui/multi-select';

interface PromptChannelSelectorProps {
  value: string[];
  onChange: (channels: string[]) => void;
  availableChannels?: string[];
}

export function PromptChannelSelector({ value, onChange, availableChannels = [] }: PromptChannelSelectorProps) {
  const channels = availableChannels.length > 0 
    ? availableChannels 
    : ['Entertainment', 'Education', 'Gaming', 'Tech', 'News', 'Lifestyle'];

  return (
    <MultiSelect
      options={channels.map(channel => ({ value: channel, label: channel }))}
      value={value}
      onChange={onChange}
      placeholder="Select channels..."
    />
  );
}

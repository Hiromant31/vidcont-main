import { MultiSelect } from '@/components/ui/multi-select';

interface PromptGenreSelectorProps {
  value: string[];
  onChange: (genres: string[]) => void;
  availableGenres?: string[];
}

export function PromptGenreSelector({ value, onChange, availableGenres = [] }: PromptGenreSelectorProps) {
  const genres = availableGenres.length > 0 
    ? availableGenres 
    : ['Action', 'Comedy', 'Drama', 'Horror', 'Sci-Fi', 'Romance', 'Documentary', 'Animation'];

  return (
    <MultiSelect
      options={genres.map(genre => ({ value: genre, label: genre }))}
      value={value}
      onChange={onChange}
      placeholder="Select genres..."
    />
  );
}

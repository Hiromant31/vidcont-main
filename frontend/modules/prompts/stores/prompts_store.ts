import { create } from 'zustand';
import { PromptCategory, PromptTemplate, PromptVariable } from '../types/prompts_types';

interface PromptsStore {
  selectedPromptId: string | null;
  activeCategory: PromptCategory | 'all';
  editorContent: string;
  editorVariables: PromptVariable[];
  previewVariables: Record<string, string>;
  isPreviewOpen: boolean;
  searchQuery: string;

  setSelectedPrompt: (id: string | null) => void;
  setActiveCategory: (category: PromptCategory | 'all') => void;
  setEditorContent: (content: string) => void;
  setEditorVariables: (vars: PromptVariable[]) => void;
  updatePreviewVariable: (key: string, value: string) => void;
  togglePreview: () => void;
  setSearchQuery: (query: string) => void;
  resetEditor: () => void;
}

export const usePromptsStore = create<PromptsStore>((set) => ({
  selectedPromptId: null,
  activeCategory: 'all',
  editorContent: '',
  editorVariables: [],
  previewVariables: {},
  isPreviewOpen: false,
  searchQuery: '',

  setSelectedPrompt: (id) => set({ selectedPromptId: id }),
  
  setActiveCategory: (category) => set({ activeCategory: category }),
  
  setEditorContent: (content) => set({ editorContent: content }),
  
  setEditorVariables: (vars) => set({ editorVariables: vars }),
  
  updatePreviewVariable: (key, value) =>
    set((state) => ({
      previewVariables: { ...state.previewVariables, [key]: value },
    })),
  
  togglePreview: () => set((state) => ({ isPreviewOpen: !state.isPreviewOpen })),
  
  setSearchQuery: (query) => set({ searchQuery: query }),
  
  resetEditor: () => set({
    editorContent: '',
    editorVariables: [],
    previewVariables: {},
    selectedPromptId: null,
  }),
}));

import { create } from 'zustand';
import { AssetType, AssetStatus } from '../types/assets_types';

interface AssetsStore {
  selectedAssetId: string | null;
  isPreviewOpen: boolean;
  filters: {
    type: AssetType | 'all';
    status: AssetStatus | 'all';
    search: string;
  };
  
  setSelectedAsset: (id: string | null) => void;
  togglePreview: (id?: string | null) => void;
  setFilter: <K extends keyof AssetsStore['filters']>(key: K, value: AssetsStore['filters'][K]) => void;
  resetFilters: () => void;
}

export const useAssetsStore = create<AssetsStore>((set) => ({
  selectedAssetId: null,
  isPreviewOpen: false,
  filters: {
    type: 'all',
    status: 'all',
    search: '',
  },

  setSelectedAsset: (id) => set({ selectedAssetId: id }),
  
  togglePreview: (id) => set((state) => ({
    isPreviewOpen: id !== null && id !== undefined ? true : !state.isPreviewOpen,
    selectedAssetId: id !== null && id !== undefined ? id : state.selectedAssetId,
  })),

  setFilter: (key, value) =>
    set((state) => ({
      filters: { ...state.filters, [key]: value },
    })),

  resetFilters: () =>
    set({
      filters: {
        type: 'all',
        status: 'all',
        search: '',
      },
    }),
}));

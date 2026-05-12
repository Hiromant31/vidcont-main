import { create } from 'zustand';
import { AnalyticsFilters } from '../types/analytics_types';

interface AnalyticsStore {
  filters: AnalyticsFilters;
  selectedTab: 'overview' | 'pipeline' | 'jobs' | 'render' | 'system';
  isRealtimeEnabled: boolean;

  setFilters: (filters: Partial<AnalyticsFilters>) => void;
  setSelectedTab: (tab: AnalyticsStore['selectedTab']) => void;
  toggleRealtime: () => void;
  resetFilters: () => void;
}

const defaultFilters: AnalyticsFilters = {
  date_from: new Date(Date.now() - 7 * 24 * 60 * 60 * 1000).toISOString().split('T')[0], // 7 days ago
  date_to: new Date().toISOString().split('T')[0],
  time_range: "7d",
};

export const useAnalyticsStore = create<AnalyticsStore>((set) => ({
  filters: defaultFilters,
  selectedTab: 'overview',
  isRealtimeEnabled: true,

  setFilters: (newFilters) =>
    set((state) => ({
      filters: { ...state.filters, ...newFilters },
    })),

  setSelectedTab: (tab) => set({ selectedTab: tab }),

  toggleRealtime: () => set((state) => ({ isRealtimeEnabled: !state.isRealtimeEnabled })),

  resetFilters: () => set({ filters: defaultFilters }),
}));

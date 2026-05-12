import { create } from 'zustand';
import { AppSettings, AIProvider } from '../types/settings_types';

interface SettingsStore {
  activeTab: string;
  hasUnsavedChanges: boolean;
  connectionTesting: boolean;
  connectionStatus: 'idle' | 'testing' | 'connected' | 'disconnected' | 'failed';
  
  setActiveTab: (tab: string) => void;
  markAsChanged: () => void;
  markAsSaved: () => void;
  setConnectionTesting: (testing: boolean) => void;
  setConnectionStatus: (status: 'idle' | 'testing' | 'connected' | 'disconnected' | 'failed') => void;
}

export const useSettingsStore = create<SettingsStore>((set) => ({
  activeTab: 'ai',
  hasUnsavedChanges: false,
  connectionTesting: false,
  connectionStatus: 'idle',

  setActiveTab: (tab) => set({ activeTab: tab }),
  
  markAsChanged: () => set({ hasUnsavedChanges: true }),
  
  markAsSaved: () => set({ hasUnsavedChanges: false }),
  
  setConnectionTesting: (testing) => set({ connectionTesting: testing }),
  
  setConnectionStatus: (status) => set({ connectionStatus: status }),
}));

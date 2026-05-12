'use client';

import { useState, useEffect } from 'react';
import { useSettingsStore } from '../stores/settings_store';

export const useConnectionStatus = () => {
  const { connectionStatus, setConnectionStatus, connectionTesting } = useSettingsStore();
  
  return {
    status: connectionStatus,
    isTesting: connectionTesting,
    isConnected: connectionStatus === 'connected',
    isDisconnected: connectionStatus === 'disconnected' || connectionStatus === 'failed',
  };
};

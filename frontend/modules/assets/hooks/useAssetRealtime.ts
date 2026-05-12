'use client';

import { useEffect } from 'react';
import { webSocketService } from '@/services/websocket/service';
import { useQueryClient } from '@tanstack/react-query';
import { ASSET_KEYS } from '../api/assets_queries';

export const useAssetRealtime = () => {
  const queryClient = useQueryClient();

  useEffect(() => {
    const handleAssetUpdate = (data: any) => {
      queryClient.invalidateQueries({ queryKey: ASSET_KEYS.lists() });
      if (data.asset_id) {
        queryClient.invalidateQueries({ queryKey: ASSET_KEYS.detail(data.asset_id) });
      }
    };

    webSocketService.on('asset_created', handleAssetUpdate);
    webSocketService.on('asset_updated', handleAssetUpdate);
    webSocketService.on('asset_deleted', handleAssetUpdate);
    webSocketService.on('asset_ready', handleAssetUpdate);
    webSocketService.on('asset_failed', handleAssetUpdate);

    return () => {
      webSocketService.off('asset_created', handleAssetUpdate);
      webSocketService.off('asset_updated', handleAssetUpdate);
      webSocketService.off('asset_deleted', handleAssetUpdate);
      webSocketService.off('asset_ready', handleAssetUpdate);
      webSocketService.off('asset_failed', handleAssetUpdate);
    };
  }, [queryClient]);
};

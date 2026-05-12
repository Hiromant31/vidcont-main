'use client';

import { Button } from '@/components/ui/button';
import { Trash2 } from 'lucide-react';
import { useAssetActions } from '../hooks/useAssetActions';

interface AssetDeleteButtonProps {
  assetId: string;
}

export function AssetDeleteButton({ assetId }: AssetDeleteButtonProps) {
  const { deleteAsset, isDeleting } = useAssetActions();

  const handleDelete = () => {
    if (window.confirm('Are you sure you want to delete this asset? This action cannot be undone.')) {
      deleteAsset(assetId);
    }
  };

  return (
    <Button 
      size="sm" 
      variant="destructive" 
      onClick={handleDelete}
      disabled={isDeleting}
    >
      {isDeleting ? 'Deleting...' : 'Delete'}
      <Trash2 className="mr-2 h-4 w-4" />
    </Button>
  );
}

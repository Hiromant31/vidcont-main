'use client';

import { Button } from '@/components/ui/button';
import { Share2 } from 'lucide-react';
import { useAssetActions } from '../hooks/useAssetActions';
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from '@/components/ui/dialog';
import { useState } from 'react';

interface AssetReuseButtonProps {
  assetId: string;
}

export function AssetReuseButton({ assetId }: AssetReuseButtonProps) {
  const { reuseAsset, isReusing } = useAssetActions();
  const [open, setOpen] = useState(false);
  const [targetType, setTargetType] = useState('scene');
  const [targetId, setTargetId] = useState('');

  const handleReuse = async () => {
    if (!targetId) return;
    await reuseAsset(assetId, targetType, targetId);
    setOpen(false);
  };

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        <Button size="sm" variant="outline" className="border-gray-700 text-gray-300 hover:bg-gray-800">
          <Share2 className="h-4 w-4 mr-2" />
          Reuse
        </Button>
      </DialogTrigger>
      <DialogContent className="bg-gray-900 border-gray-800 text-white">
        <DialogHeader>
          <DialogTitle>Reuse Asset</DialogTitle>
        </DialogHeader>
        <div className="space-y-4 py-4">
          <div className="space-y-2">
            <label className="text-sm text-gray-400">Target Type</label>
            <select 
              value={targetType}
              onChange={(e) => setTargetType(e.target.value)}
              className="w-full bg-gray-800 border border-gray-700 rounded p-2 text-white"
            >
              <option value="scene">Scene</option>
              <option value="job">Job</option>
              <option value="project">Project</option>
            </select>
          </div>
          <div className="space-y-2">
            <label className="text-sm text-gray-400">Target ID</label>
            <input
              type="text"
              value={targetId}
              onChange={(e) => setTargetId(e.target.value)}
              placeholder="Enter target ID"
              className="w-full bg-gray-800 border border-gray-700 rounded p-2 text-white"
            />
          </div>
          <Button 
            onClick={handleReuse} 
            disabled={isReusing || !targetId}
            className="w-full bg-blue-600 hover:bg-blue-700"
          >
            {isReusing ? 'Reusing...' : 'Reuse Asset'}
          </Button>
        </div>
      </DialogContent>
    </Dialog>
  );
}

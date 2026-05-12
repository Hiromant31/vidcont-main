'use client';

import { Button } from '@/components/ui/button';
import { Download } from 'lucide-react';

interface AssetDownloadButtonProps {
  assetId: string;
  url: string;
}

export function AssetDownloadButton({ assetId, url }: AssetDownloadButtonProps) {
  const handleDownload = () => {
    window.open(url, '_blank');
  };

  return (
    <Button size="sm" variant="outline" onClick={handleDownload} className="border-gray-700 text-gray-300 hover:bg-gray-800">
      <Download className="h-4 w-4 mr-2" />
      Download
    </Button>
  );
}

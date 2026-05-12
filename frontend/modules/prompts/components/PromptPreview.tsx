'use client';

import { Copy, Check } from 'lucide-react';
import { useState } from 'react';
import { usePromptPreview } from '../hooks/usePromptPreview';
import { Button } from '@/components/ui/button';
import { ScrollArea } from '@/components/ui/scroll-area';
import { cn } from '@/utils/cn';

export function PromptPreview() {
  const previewText = usePromptPreview();
  const [copied, setCopied] = useState(false);

  const handleCopy = async () => {
    await navigator.clipboard.writeText(previewText);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="flex flex-col h-full bg-black rounded border border-gray-800 overflow-hidden">
      <div className="flex justify-between items-center p-3 border-b border-gray-800 bg-gray-900/50">
        <h3 className="text-sm font-semibold text-white">Live Preview</h3>
        <Button size="sm" variant="ghost" onClick={handleCopy} className="h-8 text-xs">
          {copied ? <Check className="h-3 w-3 text-green-500" /> : <Copy className="h-3 w-3" />}
          {copied ? 'Copied' : 'Copy'}
        </Button>
      </div>
      <ScrollArea className="flex-1 p-4">
        <pre className={cn(
          "whitespace-pre-wrap font-mono text-sm leading-relaxed",
          previewText ? "text-gray-300" : "text-gray-600 italic"
        )}>
          {previewText || 'Start typing to see preview...'}
        </pre>
      </ScrollArea>
    </div>
  );
}
